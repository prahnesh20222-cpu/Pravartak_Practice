---
document_id: document_corpus_strategy_v2
source_file:
source_type: AI_Chat
session_type: ChatGPT
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-24
language: en
technical_depth: low_to_medium
rag_ready: false
chunking_strategy: topic_based_with_timestamp_provenance
speaker_names_preserved: false
transcript_cleaned: false
source:
additional_reading: "[[document_corpus_strategy_v1]]"
impl_example1:
imple_example2:
topics: RAG, corpus, metadata_enrichment
---
# RAG Document Processing Strategy

## Objective

Convert heterogeneous source documents into a consistent, semantically enriched Markdown corpus suitable for RAG.

## Processing Architecture

### 1. Source Extraction

- **Zoom transcripts:** Parse speaker, timestamp, and transcript content.
- **PDFs:** Use Marker to extract document structure into Markdown/structured output.
- **Markdown/text:** Preserve existing structure.
- **DOCX/slides/other formats:** Use an appropriate structure-preserving parser.

### 2. Semantic Enrichment with Qwen

Use Qwen3 4B as the semantic transformation layer.

For each source:

- Identify topics and subtopics.
- Map content to controlled terms from the project glossary.
- Identify key concepts and entities.
- Extract decisions and conclusions.
- Extract action items where applicable.
- Preserve important speaker and timestamp provenance for transcripts.
- Produce consistent, structured Markdown.
- Do not invent glossary terms; use the supplied glossary as the controlled vocabulary.

For long documents, process them in logically coherent sections and use hierarchical processing where the document exceeds the practical context limit.

### 3. Canonical Markdown

Produce a consistent Markdown representation containing, where applicable:

- Document metadata
- Source/provenance
- Topics
- Glossary terms
- Sections
- Key points
- Decisions
- Action items
- Relevant speaker/timestamp information
- Original factual content

### 4. RAG Preparation

After semantic enrichment:

1. Split Markdown into semantically coherent chunks.
2. Attach chunk-level metadata.
3. Generate embeddings.
4. Store chunks, embeddings, and metadata in the vector store.

Recommended metadata includes:

- source
- document ID
- document type
- topic
- glossary terms
- section
- speaker
- timestamp
- provenance

### Design Principle

Use the LLM for **semantic understanding and enrichment**.

Use deterministic Python processing for **parsing, chunking, metadata handling, validation, and storage**.

The common target for all source types is:

**Source → Structure Extraction → Qwen Semantic Enrichment → Canonical Markdown → Semantic Chunks + Metadata → Embeddings → Vector DB**
