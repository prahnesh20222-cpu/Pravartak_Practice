#!/usr/bin/env python3
"""
markdown_chunker.py

Deterministic Markdown chunking pipeline for the RAG corpus.

The pipeline deliberately separates responsibilities:

    MarkdownLoader
        -> reads the raw Markdown asynchronously

    MarkdownParser
        -> extracts and validates YAML front matter
        -> separates document metadata from Markdown body
        -> identifies Markdown sections

    MarkdownChunker
        -> creates section-aware chunks
        -> splits sections into paragraphs
        -> combines paragraphs from the same section up to a character threshold
        -> never crosses a section boundary

    JSONL writer
        -> writes validated Chunk objects for downstream embedding/vector storage

Pydantic is used for the data contracts so that malformed metadata/chunks are
caught early rather than propagating silently into the RAG pipeline.

Example:

    python markdown_chunker.py ./corpus ./output/chunks.jsonl

Optional:

    python markdown_chunker.py ./corpus ./output/chunks.jsonl \
        --min-tokens 500 \
        --target-tokens 1500 \
        --max-tokens 2000
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Pydantic data models
# ---------------------------------------------------------------------------

class DocumentMetadata(BaseModel):
    """
    Metadata extracted from the YAML front matter of a Markdown document.

    The corpus strategy deliberately allows different source types to carry
    different metadata. Therefore extra fields are preserved rather than
    rejected. Known fields are typed and validated by Pydantic.
    """

    model_config = ConfigDict(extra="allow")

    document_id: str | None = None
    source: str | None = None
    source_type: str | None = None
    document_type: str | None = None

    session_type: str | None = None
    session_date: str | None = None
    language: str | None = None
    technical_depth: str | None = None

    rag_ready: bool | None = None
    chunking_strategy: str | None = None

    topics: list[str] = Field(default_factory=list)
    glossary_terms: list[str] = Field(default_factory=list)

    source_url: str | None = None
    retrieved_at: str | None = None
    provenance: str | None = None

    speaker_names_preserved: bool | None = None
    transcript_cleaned: bool | None = None


class MarkdownDocument(BaseModel):
    """
    Parsed representation of one Markdown source document.
    """

    model_config = ConfigDict(extra="forbid")

    path: str
    metadata: DocumentMetadata
    body: str


class MarkdownSection(BaseModel):
    """
    A heading-aware section of a Markdown document.

    heading_path preserves the hierarchy, e.g.

        ["RAG", "Retrieval", "Hybrid Retrieval"]
    """

    model_config = ConfigDict(extra="forbid")

    level: int = Field(ge=1, le=6)
    title: str
    heading_path: list[str]
    content: str


class ChunkMetadata(BaseModel):
    """
    Metadata attached to every chunk.

    This is intentionally explicit because these fields are expected to become
    retrieval/filtering metadata later in the pipeline.
    """

    model_config = ConfigDict(extra="allow")

    document_id: str
    document_type: str
    source: str

    section: str
    section_path: list[str]

    token_count: int = Field(ge=0)
    character_count: int = Field(ge=0)

    topic: str | None = None
    topics: list[str] = Field(default_factory=list)
    glossary_terms: list[str] = Field(default_factory=list)

    speaker: str | None = None
    timestamp: str | None = None

    source_url: str | None = None
    retrieved_at: str | None = None
    provenance: str | None = None


class DocumentChunk(BaseModel):
    """
    Final validated RAG chunk.

    The text is kept separate from metadata because downstream embedding
    pipelines normally embed `text` while using `metadata` for filtering,
    tracing and provenance.
    """

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    text: str = Field(min_length=1)
    metadata: ChunkMetadata


class ChunkingConfig(BaseModel):
    """
    Runtime configuration for section-aware paragraph chunking.

    `max_chunk_chars` is the maximum size used when PACKING paragraphs.
    It is not a command to split a paragraph.

    Therefore, if one paragraph is already larger than max_chunk_chars, that
    paragraph remains intact as one chunk. This deliberately preserves the
    semantic integrity of the paragraph.
    """

    max_chunk_chars: int = Field(default=500, ge=1)


# ---------------------------------------------------------------------------
# Markdown loader
# ---------------------------------------------------------------------------

class BaseDocumentLoader(ABC):
    """
    Base class for source-specific document loaders.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)

    @abstractmethod
    async def load(self) -> str:
        pass


class MarkdownLoader(BaseDocumentLoader):
    """
    Loads Markdown files (.md).

    This loader deliberately returns raw Markdown. Parsing YAML front matter
    and interpreting Markdown structure are separate responsibilities.
    """

    async def load(self) -> str:
        logger.info("Loading markdown file: %s", self.path.name)

        if not self.path.exists():
            logger.error("File not found: %s", self.path)
            raise FileNotFoundError(f"File not found: {self.path}")

        if self.path.suffix.lower() != ".md":
            raise ValueError(f"Expected a Markdown file: {self.path}")

        loop = asyncio.get_running_loop()

        def _read_file() -> str:
            try:
                with self.path.open("r", encoding="utf-8") as file:
                    return file.read()
            except Exception:
                logger.exception("Error reading markdown file: %s", self.path)
                raise

        return await loop.run_in_executor(None, _read_file)


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

class MarkdownParser:
    """
    Parses raw Markdown into a validated MarkdownDocument.

    Expected document structure:

        ---
        document_id: ...
        source_type: ...
        topics:
          - RAG
          - chunking
        ---
        # Heading
        ...

    YAML front matter is treated as document metadata, not as chunk content.
    """

    FRONT_MATTER_START = "---"
    FRONT_MATTER_END_MARKERS = {"---", "..."}

    def parse(
        self,
        raw_markdown: str,
        path: str | Path,
    ) -> MarkdownDocument:
        metadata_dict, body = self._split_front_matter(raw_markdown)

        try:
            metadata = DocumentMetadata.model_validate(metadata_dict)
            return MarkdownDocument(
                path=str(path),
                metadata=metadata,
                body=body,
            )
        except ValidationError:
            logger.exception("Invalid document metadata: %s", path)
            raise

    def _split_front_matter(
        self,
        raw_markdown: str,
    ) -> tuple[dict[str, Any], str]:
        """
        Extract YAML front matter.

        If a Markdown file has no YAML front matter, return an empty metadata
        dictionary and treat the complete file as the Markdown body.
        """

        lines = raw_markdown.splitlines()

        if not lines or lines[0].strip() != self.FRONT_MATTER_START:
            logger.warning("No YAML front matter found")
            return {}, raw_markdown.strip()

        closing_index = None

        for index in range(1, len(lines)):
            if lines[index].strip() in self.FRONT_MATTER_END_MARKERS:
                closing_index = index
                break

        if closing_index is None:
            raise ValueError(
                "Markdown starts with YAML front matter marker '---', "
                "but no closing YAML marker was found."
            )

        yaml_text = "\n".join(lines[1:closing_index])

        try:
            metadata = yaml.safe_load(yaml_text) or {}
        except yaml.YAMLError as exc:
            raise ValueError(
                f"Invalid YAML front matter: {exc}"
            ) from exc

        if not isinstance(metadata, dict):
            raise ValueError(
                "YAML front matter must contain a mapping of metadata fields."
            )

        body = "\n".join(lines[closing_index + 1:]).strip()

        return metadata, body

    def parse_sections(
        self,
        document: MarkdownDocument,
    ) -> list[MarkdownSection]:
        """
        Convert the Markdown body into heading-aware sections.

        We retain the heading hierarchy because section context is valuable
        retrieval metadata.
        """

        lines = document.body.splitlines()

        sections: list[MarkdownSection] = []

        heading_path: list[str] = []
        current_level = 1
        current_title = "Document"
        current_lines: list[str] = []

        def flush() -> None:
            nonlocal current_lines

            content = "\n".join(current_lines).strip()

            if content:
                sections.append(
                    MarkdownSection(
                        level=current_level,
                        title=current_title,
                        heading_path=heading_path.copy(),
                        content=content,
                    )
                )

            current_lines = []

        for line in lines:
            match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)

            if match:
                flush()

                current_level = len(match.group(1))
                current_title = match.group(2).strip()

                # Maintain the heading hierarchy.
                heading_path[:] = heading_path[: current_level - 1]
                heading_path.append(current_title)
            else:
                current_lines.append(line)

        flush()

        return sections


# ---------------------------------------------------------------------------
# Token counting
# ---------------------------------------------------------------------------

class TokenCounter:
    """
    Token counter abstraction.

    For the first implementation we keep the dependency optional. If
    tiktoken is installed, it is used. Otherwise a whitespace estimate is
    used.

    IMPORTANT:
    A production implementation should eventually use the tokenizer
    corresponding to the embedding/chunking model being evaluated rather than
    assuming that a generic tokenizer is identical to the model tokenizer.
    """

    def __init__(self) -> None:
        self._encoder = None

        try:
            import tiktoken

            self._encoder = tiktoken.get_encoding("cl100k_base")
            logger.info("Using tiktoken cl100k_base for token estimates")
        except ImportError:
            logger.warning(
                "tiktoken is not installed; using whitespace token estimates"
            )
        except Exception:
            logger.exception("Could not initialize tiktoken")
            self._encoder = None

    def count(self, text: str) -> int:
        if self._encoder is not None:
            return len(self._encoder.encode(text))

        # Fallback only. This is an estimate, not model-tokenizer output.
        return len(re.findall(r"\S+", text))


# ---------------------------------------------------------------------------
# Chunker
# ---------------------------------------------------------------------------

class MarkdownChunker:
    """
    Section-aware, paragraph-preserving Markdown chunker.

    Chunking hierarchy:

        Markdown document
              ↓
        Markdown sections
              ↓
        paragraphs within each section
              ↓
        combine adjacent paragraphs from the SAME section
              ↓
        ~500-character chunks

    The important constraint is that a chunk never crosses a section boundary.

    This is deliberately different from token-window chunking. The Markdown
    structure determines the primary semantic boundary, while character count
    is only used to decide how many paragraphs should be packed together.
    """

    def __init__(self, config: ChunkingConfig):
        self.config = config

    def chunk(
        self,
        document: MarkdownDocument,
        sections: list[MarkdownSection],
    ) -> list[DocumentChunk]:
        """
        Create validated RAG chunks section by section.

        Each section is processed independently. Paragraphs within that
        section are packed together until adding the next paragraph would
        exceed the target character threshold.

        We intentionally do NOT split an individual paragraph. A paragraph
        longer than 500 characters remains intact.
        """

        document_id = self._document_id(document)

        document_type = (
            document.metadata.source_type
            or document.metadata.document_type
            or "markdown"
        )

        chunks: list[DocumentChunk] = []

        for section in sections:
            # A section without actual content should not produce a chunk.
            if not section.content.strip():
                continue

            paragraphs = self._split_paragraphs(section.content)

            section_chunks = self._chunk_section(
                section=section,
                paragraphs=paragraphs,
            )

            for text in section_chunks:
                chunk_index = len(chunks)

                metadata = ChunkMetadata(
                    document_id=document_id,
                    document_type=document_type,
                    source=(
                        document.metadata.source
                        or Path(document.path).name
                    ),
                    section=section.title,
                    section_path=section.heading_path,

                    # Character count controls chunking. Token count is
                    # retained as useful downstream metadata, but is NOT used
                    # to determine chunk boundaries.
                    token_count=self._estimate_token_count(text),
                    character_count=len(text),

                    topics=document.metadata.topics,
                    glossary_terms=document.metadata.glossary_terms,
                    source_url=document.metadata.source_url,
                    retrieved_at=document.metadata.retrieved_at,
                    provenance=document.metadata.provenance,
                )

                chunk_id = self._chunk_id(
                    document_id=document_id,
                    index=chunk_index,
                    text=text,
                )

                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        text=text,
                        metadata=metadata,
                    )
                )

        return chunks

    def _chunk_section(
        self,
        section: MarkdownSection,
        paragraphs: list[str],
    ) -> list[str]:
        """
        Pack paragraphs within one section.

        Example with max_chunk_chars = 500:

            Paragraph A = 250 chars
            Paragraph B = 180 chars
            Paragraph C = 220 chars

        Result:

            Chunk 1 = A + B       (~430 chars)
            Chunk 2 = C            (~220 chars)

        We never combine C with A/B once the character threshold would be
        exceeded. More importantly, paragraphs are never split. If C itself
        is larger than the configured maximum, C remains one intact chunk.
        """

        chunks: list[str] = []
        current_paragraphs: list[str] = []
        current_size = 0

        for paragraph in paragraphs:
            paragraph_size = len(paragraph)

            if not current_paragraphs:
                current_paragraphs = [paragraph]
                current_size = paragraph_size
                continue

            candidate_size = (
                current_size
                + 2  # "\n\n" separator
                + paragraph_size
            )

            if candidate_size > self.config.max_chunk_chars:
                # Flush the current group before starting the next one.
                chunks.append("\n\n".join(current_paragraphs))

                current_paragraphs = [paragraph]
                current_size = paragraph_size
            else:
                # The paragraph fits within the target, so keep it with
                # the preceding paragraphs from the same section.
                current_paragraphs.append(paragraph)
                current_size = candidate_size

        if current_paragraphs:
            chunks.append("\n\n".join(current_paragraphs))

        return chunks

    @staticmethod
    def _split_paragraphs(text: str) -> list[str]:
        """
        Split section content on blank lines.

        Markdown paragraphs are retained as complete units. This also means
        that lists, code blocks and other Markdown constructs are not
        arbitrarily split merely because they cross the character threshold.

        Specialised handling for tables/code blocks can be added later if
        corpus inspection shows that it is necessary.
        """

        return [
            paragraph.strip()
            for paragraph in re.split(r"\n\s*\n", text.strip())
            if paragraph.strip()
        ]

    @staticmethod
    def _estimate_token_count(text: str) -> int:
        """
        Lightweight whitespace-based token estimate.

        This value is retained as metadata for downstream analysis. It is
        deliberately NOT used to decide chunk boundaries; character length
        and paragraph boundaries control chunking in this version.
        """
        return len(re.findall(r"\S+", text))

    @staticmethod
    def _document_id(document: MarkdownDocument) -> str:
        """
        Prefer the document_id supplied by YAML.

        If it is absent, generate a stable ID from the file path.
        """

        if document.metadata.document_id:
            return document.metadata.document_id

        path_bytes = str(Path(document.path).resolve()).encode("utf-8")
        return hashlib.sha1(path_bytes).hexdigest()[:16]

    @staticmethod
    def _chunk_id(
        document_id: str,
        index: int,
        text: str,
    ) -> str:
        """
        Generate a deterministic chunk identifier.

        The content hash helps make the ID stable and traceable while the
        sequence number preserves document order.
        """

        digest = hashlib.sha1(
            text.encode("utf-8")
        ).hexdigest()[:10]

        return (
            f"{document_id}-chunk-{index:04d}-{digest}"
        )


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

async def process_file(
    path: Path,
    parser: MarkdownParser,
    chunker: MarkdownChunker,
) -> list[DocumentChunk]:
    """
    Process one Markdown document from raw file to validated chunks.
    """

    loader = MarkdownLoader(path)

    raw_markdown = await loader.load()

    document = parser.parse(
        raw_markdown=raw_markdown,
        path=path,
    )

    sections = parser.parse_sections(document)

    chunks = chunker.chunk(
        document=document,
        sections=sections,
    )

    logger.info(
        "Processed %s -> %d chunks",
        path.name,
        len(chunks),
    )

    return chunks


async def process_directory(
    input_dir: Path,
    output_file: Path,
    config: ChunkingConfig,
) -> None:
    """
    Process all Markdown files recursively and write one JSON object per line.

    JSONL is useful here because each chunk becomes an independent record that
    can later be sent to an embedding/vector-store pipeline.
    """

    markdown_files = sorted(input_dir.rglob("*.md"))

    if not markdown_files:
        raise FileNotFoundError(
            f"No Markdown files found under: {input_dir}"
        )

    parser = MarkdownParser()
    chunker = MarkdownChunker(config=config)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    total_chunks = 0

    with output_file.open("w", encoding="utf-8") as output:
        for path in markdown_files:
            try:
                chunks = await process_file(
                    path=path,
                    parser=parser,
                    chunker=chunker,
                )

                for chunk in chunks:
                    # model_dump() ensures the output comes from the
                    # validated Pydantic model rather than raw dictionaries.
                    output.write(
                        json.dumps(
                            chunk.model_dump(mode="json"),
                            ensure_ascii=False,
                        )
                        + "\n"
                    )

                total_chunks += len(chunks)

            except (ValueError, ValidationError, FileNotFoundError):
                logger.exception(
                    "Skipping invalid document: %s",
                    path,
                )

    logger.info(
        "Completed. %d chunks written to %s",
        total_chunks,
        output_file,
    )


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create validated RAG chunks from Markdown files."
    )

    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing Markdown files",
    )

    parser.add_argument(
        "output_file",
        type=Path,
        help="Output JSONL file",
    )

    parser.add_argument(
        "--max-chars",
        type=int,
        default=500,
        help=(
            "Maximum character size used to pack paragraphs. "
            "Paragraphs are never split to satisfy this value "
            "(default: 500)"
        ),
    )

    args = parser.parse_args()

    config = ChunkingConfig(
        max_chunk_chars=args.max_chars,
    )

    asyncio.run(
        process_directory(
            input_dir=args.input_dir,
            output_file=args.output_file,
            config=config,
        )
    )


if __name__ == "__main__":
    main()
