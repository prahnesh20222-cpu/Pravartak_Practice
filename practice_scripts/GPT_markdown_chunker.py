#!/usr/bin/env python3
"""
markdown_chunker.py

Deterministic Markdown chunker for RAG preparation.

Design goals:
- Preserve Markdown structure and YAML front matter.
- Prefer semantic boundaries (headings and paragraphs) over token boundaries.
- Use token count as a constraint, not the primary chunking strategy.
- Preserve document-level metadata on every chunk.
- Emit JSONL suitable for embedding/vector-store ingestion.

Typical usage:
    python markdown_chunker.py ./corpus ./chunks.jsonl

Optional:
    python markdown_chunker.py ./corpus ./chunks.jsonl --min-tokens 500 --target-tokens 1500 --max-tokens 2000
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

try:
    import tiktoken
except ImportError:
    tiktoken = None


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass
class Section:
    level: int
    title: str
    heading_path: list[str]
    content: str


def load_markdown(path: Path) -> tuple[dict[str, Any], str]:
    """Read Markdown and split YAML front matter from the document body."""
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, text

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() in {"---", "..."}:
            end = i
            break

    if end is None:
        return {}, text

    front_matter_text = "\n".join(lines[1:end])

    if yaml:
        metadata = yaml.safe_load(front_matter_text) or {}
        if not isinstance(metadata, dict):
            metadata = {}
    else:
        # Small fallback for simple key: value front matter.
        metadata = {}
        for line in front_matter_text.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().strip('"').strip("'")

    body = "\n".join(lines[end + 1:]).strip()
    return metadata, body


def count_tokens(text: str, encoder=None) -> int:
    """Count tokens using tiktoken when available; otherwise use a rough fallback."""
    if encoder is not None:
        return len(encoder.encode(text))

    # Deliberately conservative fallback. Install tiktoken for production runs.
    return len(re.findall(r"\S+", text))


def parse_sections(markdown: str) -> list[Section]:
    """
    Parse Markdown into heading-aware sections.

    A section contains the content belonging to one heading, including nested
    headings in the same structural block. We later split oversized blocks.
    """
    lines = markdown.splitlines()
    sections: list[Section] = []

    heading_path: list[str] = []
    current_level = 0
    current_title = "Document"
    current_lines: list[str] = []

    def flush():
        nonlocal current_lines
        content = "\n".join(current_lines).strip()
        if content:
            sections.append(
                Section(
                    level=current_level,
                    title=current_title,
                    heading_path=heading_path.copy(),
                    content=content,
                )
            )
        current_lines = []

    for line in lines:
        match = HEADING_RE.match(line)

        if match:
            flush()

            level = len(match.group(1))
            title = match.group(2).strip()

            # Remove deeper headings when moving back up the hierarchy.
            heading_path[:] = heading_path[: level - 1]
            heading_path.append(title)

            current_level = level
            current_title = title
        else:
            current_lines.append(line)

    flush()
    return sections


def split_paragraphs(text: str) -> list[str]:
    """Split content at blank lines while retaining paragraphs as units."""
    blocks = re.split(r"\n\s*\n", text.strip())
    return [b.strip() for b in blocks if b.strip()]


def split_oversized_text(
    text: str,
    max_tokens: int,
    encoder=None,
) -> list[str]:
    """
    Split an oversized section while trying to preserve Markdown blocks.

    First split on paragraphs. If one paragraph itself exceeds the limit,
    split by lines. As a final fallback, split by words.
    """
    if count_tokens(text, encoder) <= max_tokens:
        return [text.strip()]

    blocks = split_paragraphs(text)
    pieces: list[str] = []
    current: list[str] = []
    current_tokens = 0

    for block in blocks:
        block_tokens = count_tokens(block, encoder)

        if block_tokens > max_tokens:
            if current:
                pieces.append("\n\n".join(current))
                current = []
                current_tokens = 0

            # Try line-level splitting first.
            lines = block.splitlines()
            line_group: list[str] = []
            line_tokens = 0

            for line in lines:
                line_count = count_tokens(line, encoder)

                if line_group and line_tokens + line_count > max_tokens:
                    pieces.append("\n".join(line_group))
                    line_group = []
                    line_tokens = 0

                if line_count > max_tokens:
                    words = line.split()
                    word_group: list[str] = []
                    word_tokens = 0

                    for word in words:
                        wc = count_tokens(word, encoder)
                        if word_group and word_tokens + wc > max_tokens:
                            pieces.append(" ".join(word_group))
                            word_group = []
                            word_tokens = 0
                        word_group.append(word)
                        word_tokens += wc

                    if word_group:
                        pieces.append(" ".join(word_group))
                else:
                    line_group.append(line)
                    line_tokens += line_count

            if line_group:
                pieces.append("\n".join(line_group))

            continue

        if current and current_tokens + block_tokens > max_tokens:
            pieces.append("\n\n".join(current))
            current = []
            current_tokens = 0

        current.append(block)
        current_tokens += block_tokens

    if current:
        pieces.append("\n\n".join(current))

    return [p.strip() for p in pieces if p.strip()]


def merge_small_chunks(
    chunks: list[dict[str, Any]],
    min_tokens: int,
    max_tokens: int,
    encoder=None,
) -> list[dict[str, Any]]:
    """
    Merge adjacent small chunks when the combined content stays within max_tokens.

    This prevents tiny fragments from becoming individual vector records.
    """
    if not chunks:
        return []

    merged: list[dict[str, Any]] = []

    for chunk in chunks:
        if not merged:
            merged.append(chunk)
            continue

        previous = merged[-1]
        combined_text = previous["text"].rstrip() + "\n\n" + chunk["text"].lstrip()
        combined_tokens = count_tokens(combined_text, encoder)

        if (
            previous["token_count"] < min_tokens
            and combined_tokens <= max_tokens
            and previous["section_path"][:-1] == chunk["section_path"][:-1]
        ):
            previous["text"] = combined_text
            previous["token_count"] = combined_tokens
            previous["section"] = (
                previous["section"] + " | " + chunk["section"]
                if previous["section"] != chunk["section"]
                else previous["section"]
            )
        else:
            merged.append(chunk)

    return merged


def make_document_id(path: Path, metadata: dict[str, Any]) -> str:
    """Use supplied document_id; otherwise create a stable ID from the path."""
    if metadata.get("document_id"):
        return str(metadata["document_id"])

    normalized = str(path.resolve()).encode("utf-8")
    return hashlib.sha1(normalized).hexdigest()[:16]


def make_chunk_id(document_id: str, index: int, text: str) -> str:
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    return f"{document_id}-chunk-{index:04d}-{digest}"


def build_chunks(
    path: Path,
    metadata: dict[str, Any],
    sections: list[Section],
    min_tokens: int,
    target_tokens: int,
    max_tokens: int,
    encoder=None,
) -> list[dict[str, Any]]:
    document_id = make_document_id(path, metadata)
    document_type = metadata.get("source_type") or metadata.get("document_type") or "markdown"

    raw_chunks: list[dict[str, Any]] = []

    for section in sections:
        # target_tokens is used as the preferred packing point, while
        # max_tokens is the hard constraint.
        section_pieces = split_oversized_text(
            section.content,
            max_tokens=max_tokens,
            encoder=encoder,
        )

        current_piece: list[str] = []
        current_tokens = 0

        for piece in section_pieces:
            piece_tokens = count_tokens(piece, encoder)

            if (
                current_piece
                and current_tokens + piece_tokens > target_tokens
            ):
                text = "\n\n".join(current_piece).strip()
                raw_chunks.append(
                    {
                        "document_id": document_id,
                        "source": str(metadata.get("source") or path.name),
                        "document_type": document_type,
                        "section": section.title,
                        "section_path": section.heading_path,
                        "text": text,
                        "token_count": count_tokens(text, encoder),
                    }
                )
                current_piece = []
                current_tokens = 0

            current_piece.append(piece)
            current_tokens += piece_tokens

        if current_piece:
            text = "\n\n".join(current_piece).strip()
            raw_chunks.append(
                {
                    "document_id": document_id,
                    "source": str(metadata.get("source") or path.name),
                    "document_type": document_type,
                    "section": section.title,
                    "section_path": section.heading_path,
                    "text": text,
                    "token_count": count_tokens(text, encoder),
                }
            )

    raw_chunks = merge_small_chunks(
        raw_chunks,
        min_tokens=min_tokens,
        max_tokens=max_tokens,
        encoder=encoder,
    )

    final_chunks = []
    for index, chunk in enumerate(raw_chunks):
        enriched = dict(chunk)
        enriched["chunk_id"] = make_chunk_id(
            document_id,
            index,
            chunk["text"],
        )

        # Carry document-level metadata down to the chunk.
        for key in (
            "topic",
            "topics",
            "glossary_terms",
            "speaker",
            "timestamp",
            "source_url",
            "retrieved_at",
            "provenance",
        ):
            if key in metadata:
                enriched[key] = metadata[key]

        enriched["metadata"] = {
            "document_id": enriched["document_id"],
            "document_type": enriched["document_type"],
            "source": enriched["source"],
            "section": enriched["section"],
            "section_path": enriched["section_path"],
            "topic": enriched.get("topic"),
            "topics": enriched.get("topics"),
            "glossary_terms": enriched.get("glossary_terms"),
            "speaker": enriched.get("speaker"),
            "timestamp": enriched.get("timestamp"),
            "source_url": enriched.get("source_url"),
            "retrieved_at": enriched.get("retrieved_at"),
            "provenance": enriched.get("provenance"),
        }

        final_chunks.append(enriched)

    return final_chunks


def process_directory(
    input_dir: Path,
    output_file: Path,
    min_tokens: int,
    target_tokens: int,
    max_tokens: int,
):
    encoder = None
    if tiktoken:
        try:
            encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:
            encoder = None

    markdown_files = sorted(input_dir.rglob("*.md"))

    if not markdown_files:
        raise SystemExit(f"No .md files found under: {input_dir}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    total_chunks = 0

    with output_file.open("w", encoding="utf-8") as out:
        for path in markdown_files:
            metadata, body = load_markdown(path)
            sections = parse_sections(body)

            chunks = build_chunks(
                path=path,
                metadata=metadata,
                sections=sections,
                min_tokens=min_tokens,
                target_tokens=target_tokens,
                max_tokens=max_tokens,
                encoder=encoder,
            )

            for chunk in chunks:
                out.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                total_chunks += 1

            print(f"{path.name}: {len(chunks)} chunks")

    counter_type = "tiktoken" if encoder else "whitespace fallback"
    print(f"\nCreated {total_chunks} chunks")
    print(f"Token counter: {counter_type}")
    print(f"Output: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Chunk Markdown documents for RAG."
    )
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_file", type=Path)
    parser.add_argument("--min-tokens", type=int, default=500)
    parser.add_argument("--target-tokens", type=int, default=1500)
    parser.add_argument("--max-tokens", type=int, default=2000)

    args = parser.parse_args()

    if args.min_tokens >= args.max_tokens:
        parser.error("--min-tokens must be smaller than --max-tokens")

    if args.target_tokens > args.max_tokens:
        parser.error("--target-tokens cannot exceed --max-tokens")

    process_directory(
        input_dir=args.input_dir,
        output_file=args.output_file,
        min_tokens=args.min_tokens,
        target_tokens=args.target_tokens,
        max_tokens=args.max_tokens,
    )


if __name__ == "__main__":
    main()
