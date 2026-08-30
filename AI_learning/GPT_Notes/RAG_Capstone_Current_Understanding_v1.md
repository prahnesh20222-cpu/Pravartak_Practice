---
document_id: Capstone_Current_Understanding_v1
source_file:
source_type: AI_Chat
session_type: ChatGPT
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-22
language: en
technical_depth: low_to_medium
rag_ready: false
chunking_strategy: topic_based_with_timestamp_provenance
speaker_names_preserved: 
transcript_cleaned: 
source:
additional_reading:
impl_example1:
imple_example2:
---

# RAG Capstone — Current Understanding
## Prompt used


## The capstone aims to build

A governed, heterogeneous knowledge-base RAG application that turns personal and learning material into searchable, contextual knowledge and provides grounded answers, while serving as an experimental platform for understanding what improves RAG quality, usability, provenance, and retrieval.

## It has these features

- Ingests heterogeneous sources:
  - Session transcripts in Markdown with YAML metadata
  - Relevant ChatGPT conversations
  - Personal notes, including code snippets
  - PDFs from personal reading
  - Slides from live course sessions
- Uses document- and section-level metadata to describe source material.
- Chunks and embeds the corpus for semantic retrieval.
- Keeps source types distinguishable at retrieval time.
- Experiments with chunk-level metadata where it provides measurable retrieval value.
- Provides grounded answers based on retrieved evidence.
- Keeps source/provenance information available for traceability.
- Uses DataHub as the governance/catalog layer for knowledge assets.
- Separates retrieval-oriented metadata from broader governance/context metadata.
- Provides a baseline for controlled retrieval experiments.

## It uses this strategy

- Start with one source type, probably session transcripts.
- Build the simplest useful RAG pipeline first: parse → chunk → embed → retrieve → generate.
- Add other source types incrementally and test source-aware retrieval.
- Use a normalized representation between document enrichment and vectorization.
- Enrich metadata selectively and measure whether it improves retrieval.
- Compare retrieval quality, latency, usability, and complexity as capabilities are added.
- Persist stable/document-level governance metadata in the catalog and retrieval-oriented metadata with chunks/vector representations.
- Evaluate highly contextual or transient evidence information at query time rather than unnecessarily persisting it at chunk level.
- Use DataHub early to learn how a real governance/catalog platform fits around RAG.
- Do not introduce a separate graph database unless a concrete graph-reasoning requirement emerges.
- Reuse mature components for specialized capabilities such as code intelligence rather than rebuilding them unnecessarily.

## It can expand in the future to incorporate these features

- Agentic retrieval that can reformulate queries, retrieve again, or evaluate evidence.
- Multi-agent workflows for retrieval, evidence evaluation, synthesis, and specialized tasks.
- Code intelligence as a distinct retrieval capability.
- Integration with structured data through DataHub/catalog discovery and deterministic SQL/tool calls.
- Hybrid retrieval across unstructured RAG, governed catalog metadata, structured databases, and operational tools.
- Data-platform support using catalog metadata, documentation, code, logs, and runbooks.
- Diagnostic agents that produce evidence-backed remediation recommendations.
- Controlled remediation agents that invoke operational tools subject to governance and approval.
- Graph-based reasoning or a dedicated graph database if justified by actual requirements.
- More sophisticated evaluation of source authority, evidence sufficiency, retrieval quality, agentic behaviour, latency, and cost.

## Learning objectives achieved from this activity

- Understand the practical mechanics of building and evaluating a RAG system.
- Learn how document curation and metadata enrichment affect retrieval quality.
- Understand the boundary between document, retrieval, and governance metadata.
- Gain practical experience using DataHub as a knowledge/catalog governance layer.
- Understand why semantic retrieval is appropriate for unstructured knowledge but does not replace deterministic querying of structured data.
- Learn when vector retrieval, metadata filtering, reranking, graph traversal, SQL, or tool calls are appropriate.
- Understand how heterogeneous knowledge sources can be normalized while retaining source distinctions and provenance.
- Learn how agents can orchestrate multiple knowledge and tool interfaces.
- Learn to evaluate whether additional architectural complexity actually improves quality, usability, latency, or cost.
- Develop transferable judgement about what to build, what to govern, and what to consume as an existing platform capability.
- Understand how governed enterprise context can support future AI-driven data-platform support and remediation.
