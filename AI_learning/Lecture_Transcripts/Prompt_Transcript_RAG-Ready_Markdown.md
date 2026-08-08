# Convert Course Transcript to RAG-Ready Markdown

Convert the uploaded transcript into a RAG-ready Markdown document.

## 1. Primary source

Use the uploaded transcript as the authoritative source.

Do not introduce technical facts that are not supported by the transcript.

You may reorganize, clean, and lightly normalize the transcript for readability, but do not silently add external explanations or correct the instructor's content.

Preserve:
- Important terminology used by the instructor
- Speaker attribution where useful
- Timestamps for provenance
- The meaning and context of the discussion

Remove:
- WEBVTT headers
- Cue numbers
- Duplicate transcript fragments
- Obvious transcription artifacts
- Unnecessary conversational noise

## 2. Metadata taxonomy

The attached `taxonomy.yaml` is the authoritative controlled vocabulary for tags.

### Tag rules

1. Use canonical tags from `taxonomy.yaml`.
2. Never invent a new tag when an existing canonical tag or alias applies.
3. If the transcript uses an alias, map it to the canonical tag.
4. Do not create semantically equivalent variations of existing tags.
5. Use the same canonical tag across all sessions whenever the concept is the same.
6. Only create a new tag when the concept genuinely does not exist in the taxonomy.
7. If a genuinely new concept is identified, list it separately under `PROPOSED NEW TAGS` rather than silently adding it to the document's canonical tags.
8. Prefer specific existing tags over broad ones when appropriate.
9. Do not tag concepts merely because they are mentioned in passing. A tag should represent a meaningful topic in that chunk.

## 3. Chunking

Divide the transcript into meaningful topic-level chunks.

Do not create one chunk per speaker turn.

Create a new chunk when there is a meaningful change in:
- Topic
- Concept
- Technical subject
- Question being discussed
- Learning objective

Prefer approximately 5–15 meaningful chunks for a normal session, but let the content determine the actual number.

Avoid splitting a single explanation across multiple chunks unless necessary.

Each chunk should be independently understandable enough to be useful as a retrieval result.

## 4. Chunk metadata

Every chunk must contain:

```yaml
chunk_id:
topic:
timestamp_start:
timestamp_end:
content_type:
technical_depth:
tags:
source:
```

Use these controlled values where applicable:

### content_type

- concept
- explanation
- example
- demonstration
- discussion
- question-answer
- technical-overview
- technical-guidance
- programme-logistics
- platform-walkthrough

### technical_depth

- low
- medium
- high

## 5. Document metadata

Start the Markdown document with YAML front matter:

```yaml
---
document_id:
source_file:
source_type: zoom_transcript
session_type:
course:
session_date:
language: en
technical_depth:
rag_ready: true
chunking_strategy: topic_based_with_timestamp_provenance
speaker_names_preserved: true
transcript_cleaned: true
---
```

Use information from the transcript/file metadata where available. Do not invent missing values.

## 6. Chunk format

Use this structure:

```markdown
## CHUNK_ID — Topic

```yaml
chunk_id:
topic:
timestamp_start:
timestamp_end:
content_type:
technical_depth:
tags:
  - canonical-tag
  - canonical-tag
source:
```

### Transcript

[Cleaned transcript content]
```

Do not place uncontrolled synonyms in the `tags` field.

## 7. Retrieval quality

Optimize chunks for semantic retrieval without turning the transcript into a textbook.

Each chunk should:
- Have a clear topic
- Preserve enough surrounding context
- Contain the terminology used in the session
- Have consistent canonical tags
- Retain timestamp provenance
- Avoid unnecessary conversational material

Do not add summaries that introduce information not present in the transcript.

A short retrieval description may be included when it can be derived directly from the transcript.

## 8. Taxonomy evolution

At the end of the output, include:

```markdown
## Proposed New Tags

- `new-tag`: reason this concept is not adequately represented by an existing canonical tag
```

If no new tags are necessary, write:

```markdown
## Proposed New Tags

None.
```

Do not modify the taxonomy automatically.

## 9. Final validation

Before producing the file, check:

- Are all tags canonical?
- Did any alias get used instead of its canonical tag?
- Did you accidentally create synonyms of existing tags?
- Are the chunks topic-based rather than speaker-turn based?
- Does every chunk contain the required metadata?
- Are timestamps preserved?
- Is the source transcript still represented faithfully?
- Did you introduce any information that is not supported by the transcript?

Return the completed `.md` file.