---
document_id: document_corpus_strategy_v3
source_type: strategy
session_date: 2026-09-05
language: en
technical_depth: low_to_medium
rag_ready: false
version: 3
topics: [RAG, corpus, document_processing, metadata_enrichment, glossary]
---

# RAG Document Processing Strategy

## Objective

Convert heterogeneous source documents into a consistent, semantically enriched Markdown corpus suitable for RAG.

## Processing Architecture

### 1. Source Extraction

Use a source-appropriate extraction method while preserving document structure and provenance.

- **Zoom transcripts:** Parse speaker, timestamp, and transcript content. Use an LLM to transform the conversation into structured Markdown and classify content against the controlled glossary.
- **PDFs:** Use Marker to extract document structure into Markdown/structured output.
- **Webpages:** Extract the main content from HTML, remove navigation/ads/boilerplate, preserve headings, lists, tables and other useful structure, and convert to Markdown. Retain the original URL and retrieval date as provenance.
- **Markdown/text:** Preserve existing structure.
- **DOCX/slides/other formats:** Use an appropriate structure-preserving parser.

Extraction and semantic enrichment are separate operations. Extraction preserves source content and structure; semantic enrichment adds interpretation and controlled metadata.

### 2. Semantic Enrichment with Qwen

Use Qwen3 4B as the semantic transformation layer for bounded, non-real-time enrichment tasks.

For each source, where applicable:

- Identify topics and subtopics.
- Map content to controlled terms from the project glossary.
- Identify key concepts and entities.
- Extract decisions and conclusions.
- Extract action items.
- Preserve important speaker and timestamp provenance for transcripts.
- Produce consistent, structured Markdown.
- Do not invent glossary terms; use the supplied glossary as the controlled vocabulary.
- Preserve original factual content rather than replacing it with an LLM-generated summary.

For long documents, process logically coherent sections and use hierarchical processing when the document exceeds the practical context limit.

### 3. Canonical Markdown

Produce a consistent Markdown representation containing, where applicable:

- Document metadata
- Source/provenance
- Original source URL
- Retrieval date for webpages
- Topics
- Glossary terms
- Sections and headings
- Key points
- Decisions
- Action items
- Relevant speaker/timestamp information
- Original factual content

Example front matter:

```yaml
---
title: "..."
source_type: "webpage"
source_url: "..."
retrieved_at: "YYYY-MM-DD"
---
```

### 4. RAG Preparation

After semantic enrichment:

1. Parse the Markdown structure.
2. Split content into semantically coherent chunks.
3. Use token limits as a constraint, not as the primary basis for chunk boundaries.
4. Attach chunk-level metadata.
5. Generate embeddings.
6. Store chunks, embeddings, and metadata in the vector store.

Initial chunking should be evaluated experimentally, with approximately 1K–4K tokens as a starting range for Qwen-based classification, while preserving semantic boundaries.

Recommended metadata includes:

- source
- document ID
- document type
- topic
- glossary terms
- section
- speaker
- timestamp
- source URL
- retrieval date
- provenance
- chunk ID

### 5. Model and Processing Strategy

Use the local Qwen3 4B model for constrained, asynchronous enrichment tasks where high-end reasoning is unnecessary.

Suitable tasks include:

- Glossary classification
- Topic tagging
- Metadata enrichment
- Entity extraction
- Bounded summarization

Do not use the local model for unrestricted reasoning or authoritative decisions.

Use confidence thresholds, schema/output validation and escalation paths for ambiguous cases.

A production pattern can be:

```text
Document
    ↓
Structure extraction
    ↓
Local Qwen 4B
    ↓
Classification / enrichment
    ↓
Validation + confidence checks
    ├── accepted → RAG corpus
    └── ambiguous/failed → review or stronger model
```

Because enrichment is generally asynchronous, processing can be governed, batched and monitored rather than requiring real-time inference.

### Design Principles

1. **Use the LLM for semantic understanding and enrichment.**
2. **Use deterministic Python processing for parsing, chunking, metadata handling, validation and storage.**
3. **Use controlled vocabularies for classification wherever possible.**
4. **Preserve source content and provenance; enrichment should not destroy the original evidence.**
5. **Treat model context capacity as a processing constraint, not as the target RAG chunk size.**
6. **Use small local models for bounded tasks and escalate uncertain or complex cases.**
7. **Make webpage ingestion snapshot-based and provenance-aware because webpage content can change.**

## Common Target Pipeline

**Source → Structure Extraction → Qwen Semantic Enrichment → Canonical Markdown → Semantic Chunks + Metadata → Embeddings → Vector DB**
