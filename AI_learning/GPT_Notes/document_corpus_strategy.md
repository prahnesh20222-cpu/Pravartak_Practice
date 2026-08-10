---
document_id: document-corpus-strategy
document_type: architecture-guidance
source_type: derived-from-design-discussion
language: en
rag_ready: true
chunking_strategy: topic_based
metadata_strategy: controlled_taxonomy_plus_typed_relations
---

# Document Corpus Strategy for RAG

## chunk_001 — Overall corpus architecture

```yaml
chunk_id: chunk_001
topic: Overall corpus architecture
content_type: architecture
technical_depth: medium
tags:
  - rag
  - document-ingestion
  - chunking
  - metadata
  - embeddings
relations:
  - type: defines
    target: metadata-enrichment
  - type: precedes
    target: embedding
```

The corpus should be built as an ingestion pipeline rather than by manually preparing individual documents.

The recommended flow is:

**Files → extraction → chunking → metadata enrichment → normalized intermediate representation → embedding → vector DB**

The important design decision is to make the **normalized chunk representation** the contract between document processing and vector storage.

The vector database should be introduced only after the extraction, chunking, metadata, and relationship strategy has been tested and optimized.

---

## chunk_002 — Supporting multiple source file types

```yaml
chunk_id: chunk_002
topic: Multi-format document ingestion
content_type: architecture
technical_depth: medium
tags:
  - document-ingestion
  - pdf
  - docx
  - markdown
  - transcript
relations:
  - type: produces
    target: normalized-chunks
```

The corpus can contain Markdown, PDF, Word, PowerPoint, transcripts, and other document types.

The source format should not determine the downstream RAG representation.

Each source type should first be converted into a normalized representation containing extracted content, structural information where available, and provenance.

---

## chunk_003 — Markdown documents

```yaml
chunk_id: chunk_003
topic: Markdown processing
content_type: technical-guidance
technical_depth: medium
tags:
  - markdown
  - metadata
  - chunking
  - rag
relations:
  - type: uses
    target: yaml-metadata
```

Regular Markdown files can be processed directly.

Markdown is particularly useful as a human-readable intermediate and corpus format because it can contain YAML front matter for document-level metadata, headings for structural boundaries, chunk-level metadata, tags, typed relationships, and the actual source content.

Relationships should not normally be inserted as ordinary links into the prose. Instead, they should be represented in structured metadata associated with the relevant chunk.

---

## chunk_004 — Transcript conversion

```yaml
chunk_id: chunk_004
topic: Transcript conversion
content_type: technical-guidance
technical_depth: medium
tags:
  - transcript
  - markdown
  - chunking
  - metadata
  - provenance
relations:
  - type: produces
    target: rag-ready-markdown
```

Zoom or other transcripts can first be converted into RAG-ready Markdown.

The recommended transcript process is:

1. Remove transcript artifacts and unnecessary conversational noise.
2. Preserve timestamps for provenance.
3. Chunk by meaningful topic rather than by speaker turn.
4. Preserve chronological order.
5. Apply canonical tags from the controlled taxonomy.
6. Add typed relationships where they are known.
7. Identify genuinely new concepts as proposed tags rather than silently creating new canonical tags.

If a topic is revisited later, create a new chunk in its original location and apply the same canonical tags. Do not merge or move non-contiguous discussions merely because they share a topic.

**Chunking organizes the transcript; tagging connects related chunks.**

---

## chunk_005 — PDF and other non-Markdown files

```yaml
chunk_id: chunk_005
topic: Non-Markdown document processing
content_type: technical-guidance
technical_depth: medium
tags:
  - pdf
  - document-ingestion
  - chunking
  - provenance
relations:
  - type: feeds
    target: metadata-enrichment
```

PDF, DOCX, PPTX, and similar files generally contain only minimal metadata relevant to the knowledge model.

Do not manually annotate every file.

Instead:

**Source file → parser/extractor → text + structural metadata → chunking → enrichment**

Deterministic metadata should be extracted where available, such as PDF page number, DOCX heading, PPTX slide number, source filename, section title, and document identifier.

Semantic metadata is added later through the enrichment stage.

---

## chunk_006 — Controlled taxonomy

```yaml
chunk_id: chunk_006
topic: Controlled taxonomy and canonical tags
content_type: architecture
technical_depth: high
tags:
  - taxonomy
  - canonical-tags
  - glossary
  - metadata
relations:
  - type: controls
    target: tag-assignment
  - type: evolves_into
    target: enterprise-glossary
```

The corpus should maintain a controlled taxonomy as the source of truth for tags.

The taxonomy should support canonical terms, parent-child relationships, and aliases/synonyms.

For example:

```yaml
taxonomy:
  python:
    children:
      asyncio:
        aliases:
          - async-python
          - asynchronous-python

      pydantic:
        aliases:
          - pydantic-models

  rag:
    children:
      embeddings:
        aliases:
          - embedding

      vector-database:
        aliases:
          - vector-db
          - vector-store
```

A chunk should normally receive the specific canonical tag, rather than every ancestor tag. The taxonomy already establishes that `asyncio` belongs under `python`.

This prevents tag drift across documents processed over many months.

---

## chunk_007 — Metadata enrichment

```yaml
chunk_id: chunk_007
topic: Metadata enrichment pipeline
content_type: architecture
technical_depth: high
tags:
  - metadata-enrichment
  - taxonomy
  - canonical-tags
  - glossary
  - relations
relations:
  - type: uses
    target: controlled-taxonomy
  - type: precedes
    target: embedding
```

Metadata enrichment should be a distinct stage after extraction and chunking.

A chunk can be enriched with canonical tags, glossary terms, content type, technical depth, source provenance, typed relationships, and page, section, or timestamp information.

Some metadata is deterministic and should be extracted by code. Other metadata is semantic and may require LLM-assisted enrichment.

The LLM should not independently invent tags for every document. It should select existing canonical terms whenever possible.

---

## chunk_008 — Proposed new tags and approval

```yaml
chunk_id: chunk_008
topic: Taxonomy evolution and human approval
content_type: governance
technical_depth: high
tags:
  - taxonomy
  - canonical-tags
  - metadata-enrichment
  - human-in-the-loop
relations:
  - type: governs
    target: proposed-tags
```

When enrichment encounters a concept that genuinely does not exist in the taxonomy, it should propose a new tag.

The proposed tag should identify the proposed canonical term, why the existing taxonomy is insufficient, and which chunks would use the proposed term.

The proposed term should not become canonical until it is approved.

After approval:

1. Add the canonical term to the taxonomy.
2. Define its parent where appropriate.
3. Define aliases where appropriate.
4. Regenerate or update the affected chunk metadata.
5. Use the new canonical term for future documents.

This creates a controlled human-in-the-loop taxonomy evolution process.

---

## chunk_009 — Typed relationships

```yaml
chunk_id: chunk_009
topic: Typed relationships between knowledge objects
content_type: architecture
technical_depth: high
tags:
  - relations
  - glossary
  - metadata
  - knowledge-graph
relations:
  - type: connects
    target: code
  - type: connects
    target: glossary
```

Relationships should be represented explicitly rather than as ordinary Markdown links embedded in prose.

Useful relationship types can include `discusses`, `implements`, `example_of`, `prerequisite_for`, and `extends`.

For example:

```yaml
relations:
  - type: discusses
    target_type: glossary_term
    target_id: retry

  - type: implements
    target_type: code
    target_id: src/pipeline/pipeline.py#ask_llm_with_retry
```

Relationships are normally most useful at the chunk level because a specific section can discuss or implement a specific concept.

These relationships can initially remain structured metadata. They can later be transformed into graph edges if a graph-based retrieval architecture is introduced.

---

## chunk_010 — Normalized intermediate representation

```yaml
chunk_id: chunk_010
topic: Normalized chunk representation
content_type: architecture
technical_depth: high
tags:
  - normalized-chunks
  - metadata
  - document-ingestion
  - rag
relations:
  - type: precedes
    target: embedding
  - type: feeds
    target: vector-database
```

Before embedding, each source document should produce a set of normalized chunks.

For example:

```json
{
  "chunk_id": "week2_007",
  "document_id": "week2",
  "content": "The retry logic uses exponential backoff...",
  "source": {
    "file": "week2.pdf",
    "page_start": 12,
    "page_end": 13
  },
  "tags": ["asyncio", "retry"],
  "relations": [
    {
      "type": "implements",
      "target": "src/pipeline/pipeline.py#ask_llm_with_retry"
    }
  ]
}
```

This normalized representation should be persisted as JSON, SQLite records, or another suitable intermediate store.

The exact vector database should not be part of this stage.

---

## chunk_011 — Optimize before embedding

```yaml
chunk_id: chunk_011
topic: Pre-embedding validation and optimization
content_type: architecture
technical_depth: high
tags:
  - chunking
  - metadata-enrichment
  - rag-evaluation
  - embeddings
relations:
  - type: precedes
    target: embedding
```

The extraction, chunking, and enrichment stages should be tested and optimized before embeddings are generated.

Important questions include:

- Are chunks sufficiently self-contained?
- Are topic boundaries appropriate?
- Is chronology preserved where it matters?
- Are canonical tags consistent?
- Are relationships meaningful?
- Is source provenance preserved?
- Are irrelevant tags being added?
- Is the taxonomy stable?

The vector database should not be used to hide problems in the corpus.

A good normalized corpus should be understandable and inspectable before vectorization.

---

## chunk_012 — Embedding and vector database

```yaml
chunk_id: chunk_012
topic: Embedding and vector storage
content_type: architecture
technical_depth: medium
tags:
  - embeddings
  - vector-database
  - metadata
  - rag
relations:
  - type: consumes
    target: normalized-chunks
```

Once the normalized chunks and metadata are satisfactory, each chunk can be embedded.

The unit sent to the vector database is conceptually:

**chunk content + embedding + chunk metadata**

Metadata from unrelated files is not attached to each chunk. Each vector record carries metadata relevant to that chunk, with selected document-level metadata copied down where useful.

---

## chunk_013 — Markdown as an inspection format

```yaml
chunk_id: chunk_013
topic: Markdown as a corpus representation
content_type: technical-guidance
technical_depth: medium
tags:
  - markdown
  - normalized-chunks
  - metadata
relations:
  - type: represents
    target: normalized-chunks
```

Markdown is a convenient format for inspecting and reviewing enrichment output because humans can easily see the content, chunk boundaries, tags, relationships, and provenance.

However, the long-term machine-to-machine contract should be the normalized chunk representation rather than Markdown itself.

Markdown can therefore be used for regular source documents, converted transcripts, human review of enriched documents, and documentation of the corpus strategy.

---

## chunk_014 — Recommended corpus structure

```yaml
chunk_id: chunk_014
topic: Corpus directory structure
content_type: architecture
technical_depth: medium
tags:
  - document-ingestion
  - normalized-chunks
  - taxonomy
  - metadata
relations:
  - type: organizes
    target: corpus
```

A practical development structure is:

```text
corpus/
├── taxonomy.yaml
├── source/
│   ├── pdf/
│   ├── docx/
│   ├── markdown/
│   └── transcripts/
├── processed/
│   ├── week01.json
│   ├── week02.json
│   └── ...
└── rag-ready/
    ├── week01.md
    ├── week02.md
    └── ...
```

`taxonomy.yaml` is the controlled vocabulary.

`source/` contains original files.

`processed/` contains normalized, enriched chunks.

`rag-ready/` contains human-readable Markdown representations where useful.

Embedding can consume the normalized processed representation rather than requiring Markdown as an intermediate dependency.

---

## chunk_015 — Future enterprise architecture

```yaml
chunk_id: chunk_015
topic: Future enterprise metadata architecture
content_type: architecture
technical_depth: medium
tags:
  - metadata
  - taxonomy
  - glossary
  - knowledge-graph
  - rag
relations:
  - type: evolves_into
    target: enterprise-metadata-platform
```

The initial implementation does not require DataHub, Neo4j, or another separate graph platform.

The immediate goal is to establish:

1. A controlled taxonomy.
2. Consistent canonical tags.
3. Reliable chunking.
4. Explicit typed relationships.
5. A normalized chunk-level metadata model.
6. A validated ingestion pipeline.

Later, the same metadata and relationships can be mapped into an enterprise catalog, graph database, or hybrid retrieval architecture.

The important point is to establish the metadata model first rather than choosing a platform before understanding what the corpus actually requires.


---

## chunk_016 — Chunk IDs are identifiers, not chunking instructions

```yaml
chunk_id: chunk_016
topic: Chunk IDs and chunking algorithms
content_type: technical-guidance
technical_depth: high
tags:
  - chunking
  - chunk-id
  - normalized-chunks
  - metadata
relations:
  - type: precedes
    target: metadata-enrichment
```

A `chunk_id` identifies an already-created chunk. It does not, by itself, tell a chunking algorithm where to split a document.

The general pipeline is:

```text
Source document
      ↓
Chunking algorithm
      ↓
Actual chunks
      ↓
Assign chunk_id
      ↓
Metadata enrichment
      ↓
Embedding
```

For example, a chunker may split a document using headings, token/character limits, semantic boundaries, and overlap. The resulting chunks are then assigned stable identifiers.

There are two useful approaches:

**General documents:** let the ingestion/chunking pipeline determine the initial boundaries, then assign IDs and enrich the chunks.

**Already curated Markdown/transcripts:** the Markdown can contain explicit semantic sections such as `## chunk_001 — Retry with exponential backoff`. A parser can intentionally treat those sections as pre-defined boundaries.

The important distinction is:

**The chunking stage creates the chunks; the metadata stage identifies and enriches them.**

---

## chunk_017 — Enterprise metadata enrichment and stewardship

```yaml
chunk_id: chunk_017
topic: Enterprise metadata enrichment and stewardship
content_type: governance
technical_depth: high
tags:
  - metadata-enrichment
  - llm
  - stewardship
  - taxonomy
  - glossary
relations:
  - type: governs
    target: metadata-enrichment
  - type: uses
    target: controlled-taxonomy
```

In a mature enterprise implementation, chunk metadata enrichment can combine deterministic extraction, LLM-assisted enrichment, rules, and human stewardship.

A useful division is:

| Metadata | Typical approach |
|---|---|
| Page, section, timestamp, filename | Deterministic extraction |
| Chunk boundaries | Parsing/chunking algorithms; sometimes LLM-assisted |
| Topics / canonical tags | LLM + controlled taxonomy |
| Glossary-term mapping | LLM + glossary + validation |
| Relationships | LLM-assisted + rules + stewardship |
| New glossary terms | LLM proposes → steward approves |
| Sensitive/critical classifications | Rules + human approval |
| Provenance | System-generated |

Stewardship should not mean manually tagging every chunk. The LLM can perform the high-volume enrichment while stewards provide governance and quality control, especially for the controlled vocabulary and important relationships.

The resulting enterprise pattern is:

```text
Enterprise taxonomy / glossary
             ↓
Document → Extract → Chunk → LLM enrichment
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
             Existing terms       New concepts
                    ↓                   ↓
              Auto-accept        Steward review
                                        ↓
                                 Approve / reject
                                        ↓
                                Enriched metadata
                                        ↓
                                   RAG / Search
```

---

## chunk_018 — Recommended chunking and metadata prompt

```yaml
chunk_id: chunk_018
topic: Chunking and metadata enrichment prompt
content_type: prompt-template
technical_depth: high
tags:
  - chunking
  - metadata-enrichment
  - canonical-tags
  - taxonomy
  - stewardship
  - rag
relations:
  - type: operationalizes
    target: controlled-taxonomy
  - type: produces
    target: normalized-chunks
```

The following prompt can be used when creating RAG-ready Markdown from transcripts or other source material. It is designed to make chunk boundaries and metadata explicit while preserving source content.

### Prompt

```text
Convert the supplied source material into RAG-ready Markdown using the supplied taxonomy.yaml as the controlled vocabulary.

Goals:
1. Preserve the meaning and important context of the source.
2. Preserve chronological order where the source is a transcript.
3. Create semantically coherent chunks rather than arbitrary fixed-size chunks.
4. Give every chunk a stable chunk_id.
5. Add structured metadata to every chunk.
6. Use only canonical tags from taxonomy.yaml whenever an appropriate term already exists.
7. Do not create synonyms or alternate spellings of existing canonical tags.
8. Preserve provenance such as page numbers, section names, or transcript timestamps when available.
9. Represent relationships as structured metadata rather than ordinary links inserted into the prose.

For each chunk, use this structure:

## chunk_NNN — <descriptive section title>

```yaml
chunk_id: chunk_NNN
topic: <primary topic>
content_type: <type>
technical_depth: <low|medium|high>
tags:
  - <canonical-tag>

relations:
  - type: <relationship-type>
    target_type: <target-type>
    target_id: <canonical target identifier>

source:
  file: <source file>
  page_start: <page if available>
  page_end: <page if available>
  timestamp_start: <timestamp if available>
  timestamp_end: <timestamp if available>
```

Then place the actual source content below the metadata.

Important chunking rules:
- A chunk must be understandable in isolation as far as practical.
- Do not merge distant sections merely because they discuss the same topic.
- If a topic is revisited later, create a new chunk at its original location and apply the same canonical tag(s).
- Do not move or reorder content to group related topics.
- Do not alter the source meaning merely to make chunks cleaner.
- Preserve examples and technical details that are necessary to understand the section.
- Use headings and natural topic boundaries as preferred chunk boundaries.
- For transcripts, preserve timestamps and chronological order.

Metadata rules:
- Assign specific canonical tags where possible.
- Parent tags do not need to be repeated when a more specific canonical child tag represents the concept.
- Use typed relationships such as discusses, implements, example_of, prerequisite_for, or extends when supported by the source.
- Do not invent a relationship merely because two concepts are semantically related.
- Do not silently modify taxonomy.yaml.

New-tag workflow:
- If a genuinely new concept is present and no existing canonical tag is appropriate, do not create a new canonical tag immediately.
- Add a `Proposed New Tags` section at the end of the document.
- For each proposed tag, give:
  * proposed canonical name
  * proposed parent
  * aliases, if applicable
  * reason the existing taxonomy is insufficient
  * chunk_ids that would use the proposed tag
- Do not use a proposed tag as a canonical tag until it is approved.

After the user approves proposed tags:
1. Update taxonomy.yaml with the approved canonical terms.
2. Define their parent-child relationships and aliases.
3. Regenerate or update the affected chunk metadata.
4. Produce the final RAG-ready Markdown with only approved canonical tags.

Do not treat chunk_id values as instructions to a chunking library. They identify chunks after the boundaries have been determined. For pre-curated Markdown, explicit chunk headings may be used as intentional chunk boundaries; for other formats, the ingestion pipeline should determine the initial boundaries before metadata enrichment.

The final Markdown should contain:
- document-level YAML front matter
- semantically coherent chunks
- chunk-level YAML metadata
- source content
- a `Proposed New Tags` section when required
```

This prompt is intended to produce a **human-reviewable intermediate corpus**, not to replace the later automated extraction, chunking, normalization, and embedding pipeline.

---

## End-to-end strategy

```text
                         CONTROLLED TAXONOMY
                                 │
                                 ▼
Files → Extract → Chunk → Enrich → Validate
(PDF,      │        │        │         │
DOCX,      │        │        │         │
MD, PPT,   │        │        │         │
transcript)          │        │         │
                     └────────┴─────────┘
                              │
                              ▼
                   Normalized chunk JSON
                              │
                              ▼
                         Human review
                              │
                              ▼
                           Embedding
                              │
                              ▼
                          Vector DB
```

The central design principle is:

**Build and validate the corpus before vectorizing it.**

The vector database is the final retrieval layer, not the place where document understanding, chunking, taxonomy design, and relationship modeling should first be figured out.
