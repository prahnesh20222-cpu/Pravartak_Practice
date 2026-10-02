# Corpus Markdown — File-Level Metadata Specification v1

This specification defines the file-level metadata to be persisted in every canonical Markdown document in the corpus.

## File-Level Metadata

| Metadata field             | Allowed values / format                                                                                                                                                                                                                                 | Mandatory?  |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `document_id`              | Unique, stable identifier for the document. Recommended format: lowercase `kebab-case`. Must not change when the document title changes.                                                                                                                | Yes         |
| `title`                    | Human-readable document title. Free text.                                                                                                                                                                                                               | Yes         |
| `document_version`         | Positive integer: `1`, `2`, `3`, ...                                                                                                                                                                                                                    | Yes         |
| `source_type`              | Controlled vocabulary describing the type of source material. Examples: `class_notes`, `practice_lab`, `transcript`, `pdf`, `webpage`, `chat`, `personal_notes`, `slides`, `docx`. Extend the controlled vocabulary as new source types are introduced. | Yes         |
| `source_file`              | Original source filename/path, where applicable. Free text. Empty/null when there is no separate source file.                                                                                                                                           | Conditional |
| `source`                   | Controlled description of the source/origin, such as `personal_notes`, `transcript`, `pdf`, `webpage`, `chatgpt`.                                                                                                                                       | Yes         |
| `session_type`             | Examples: `live_session`, `recorded_session`, `practice`,`self_study`, `none`. Use only when applicable.                                                                                                                                                | Conditional |
| `course`                   | Course/programme name. Free text. Required for course-derived material; otherwise empty/null.                                                                                                                                                           | Conditional |
| `session_date`             | ISO 8601 date: `YYYY-MM-DD`.                                                                                                                                                                                                                            | Conditional |
| `additional_session_dates` | YAML list of ISO 8601 dates: `YYYY-MM-DD`. Empty list if not applicable.                                                                                                                                                                                | Conditional |
| `language`                 | ISO 639-1 language code where possible, e.g. `en`, `ta`, `hi`.                                                                                                                                                                                          | Yes         |
| `technical_depth`          | Controlled vocabulary: `introductory`, `low`, `low_to_medium`, `medium`, `medium_to_high`, `high`, `advanced`.                                                                                                                                          | Yes         |
| `topics`                   | YAML list of controlled topic terms. Example: `- RAG` / `- embeddings` / `- chunking`.                                                                                                                                                                  | Yes         |
| `rag_ready`                | Boolean: `true` or `false`. Indicates whether the document has passed the required preparation/validation steps for RAG ingestion.                                                                                                                      | Yes         |
| `source_url`               | Fully qualified URL. Required when the source is a webpage or other externally retrieved online source; otherwise empty/null.                                                                                                                           | Conditional |
| `retrieved_at`             | ISO 8601 date/time, preferably with timezone, e.g. `2026-09-05T18:30:00+05:30`. Required when content was retrieved from an external online source.                                                                                                     | Conditional |
| `speaker_names_preserved`  | Boolean: `true` or `false`. Applicable primarily to transcript-derived documents.                                                                                                                                                                       | Conditional |
| `transcript_cleaned`       | Boolean: `true` or `false`. Applicable primarily to transcript-derived documents.                                                                                                                                                                       | Conditional |

### Example

```yaml
---
document_id: naive-rag_scratch
title: "Naive RAG – Scratch Notes"
document_version: 1

source_type: class_notes
source_file:
source: personal_notes

session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-29
additional_session_dates:
  - 2026-08-30
  - 2026-09-05

language: en
technical_depth: low_to_medium
topics:
  - RAG
  - embeddings
  - chunking
  - long-context

rag_ready: false

source_url:
retrieved_at:

speaker_names_preserved: false
transcript_cleaned: false
---
```

### Design Rule

File-level metadata describes the **document, its source, provenance, semantic classification, and RAG lifecycle status**.

It should not contain downstream implementation metadata such as:

- `chunking_strategy`
- `chunk_id`
- embedding model
- vector database
- similarity score
- retrieval information

Those belong to downstream RAG-processing metadata rather than the canonical document's file-level metadata.

### Conditional Metadata Rule

A conditional field should be included when applicable to the document type. It may otherwise be empty/null. This keeps the schema consistent across heterogeneous sources without forcing irrelevant metadata into every document.

## Section-metadata
|Field|Required?|Applies to|Description|Example|
|---|---|---|---|---|
|`source_reference`|Conditional|Any source where a precise source locator is useful|Reference to the original location of the section in the source material. Use the most appropriate locator for the source type.|`Page 12`, `Slide 8`, `Section 3.2`, `00:14:32`|
|`speaker_names`|Conditional|Transcripts / sessions|Names of speakers associated with the section, when speaker attribution is relevant and available.|`[Instructor]`, `[John, Jane]`|
|`timestamp_start`|Conditional|Transcripts / recorded sessions|Start timestamp of the section in the original recording/transcript.|`00:14:32`|
|`timestamp_end`|Conditional|Transcripts / recorded sessions|End timestamp of the section in the original recording/transcript.|`00:21:47`|

**Important:** The Markdown heading itself provides the section title and hierarchy. Therefore, fields such as `section_id`, `section_title`, `section_level`, and `parent_section_id` do **not** need to be manually maintained; they can be derived deterministically during parsing. Likewise, `topics`, `glossary_terms`, `key_points`, and other semantic metadata should be generated during enrichment rather than added to the canonical Markdown.
