# SOP — Data Quality for a RAG Corpus

## 1. Purpose

Ensure that **any document admitted to the RAG corpus**, regardless of its original format, is:

- sufficiently complete
- accurately extracted
- structurally usable
- semantically coherent
- appropriately classified
- traceable to its source
- sufficiently current
- suitable for chunking and retrieval

The SOP applies to the **logical document/content representation**, not to a particular file format.

```text
PDF ────────┐
DOCX ───────┤
PPTX ───────┤
Markdown ───┤
TXT ────────┤
HTML ───────┤──→ Format-specific extraction
Transcript ─┘              ↓
                    Extracted content
                           ↓
                     DQ validation
                           ↓
                    Semantic enrichment
                           ↓
                      Chunking
                           ↓
                      Embedding
                           ↓
                        Vector DB
```

---

## 2. Core Principle: Separate Source Format from Corpus Content

The important abstraction is not:

> "Everything must become Markdown."

It is:

> **"Every source must be transformed into a machine-processable representation that preserves the information needed for retrieval and provenance."**

For example:

| Source | Possible processing representation |
|---|---|
| Markdown | Markdown directly |
| TXT | Plain text |
| HTML/webpage | Cleaned HTML / Markdown / structured text |
| PDF | Extracted text + layout/structure |
| DOCX | Paragraphs + headings + tables |
| PPTX | Slides + text + notes + tables |
| Transcript | Speaker + timestamp + utterance |
| Scanned PDF | OCR + layout |
| Image document | OCR + visual/layout metadata |

The **file itself remains the source of truth**.

The extracted representation is the material being evaluated and subsequently chunked.

---

## 3. DQ Stages

Structure the SOP into **six universal stages**:

```text
1. Source Registration
        ↓
2. Format-Specific Extraction
        ↓
3. Extraction DQ
        ↓
4. Semantic / Metadata DQ
        ↓
5. Chunk DQ
        ↓
6. Retrieval / Lifecycle DQ
```

Only stages 2 and parts of stage 3 need to vary significantly by file type.

---

## 4. Stage 1 — Source Registration

Every source gets a `document_id`.

Minimum metadata:

```yaml
document_id:
source_type:
source_name:
source_location:
source_owner:
version:
created_at:
retrieved_at:
classification:
```

For webpages:

```yaml
source_url:
retrieved_at:
```

For files:

```yaml
file_name:
file_format:
file_size:
file_hash:
```

The hash is particularly useful because it lets the pipeline determine whether a supposedly unchanged document has actually changed.

---

## 5. Stage 2 — Format-Specific Extraction

This is where the SOP branches.

### 5.1 Markdown

Markdown is the **baseline case** because it is already structurally useful.

Validate:

- headings
- paragraphs
- lists
- tables
- links
- code blocks
- metadata/front matter

Then proceed to semantic enrichment/chunking.

Markdown becomes the **reference implementation** for the SOP because it has relatively few extraction uncertainties.

---

### 5.2 PDF

PDF requires additional controls because **visual appearance does not necessarily correspond to logical document structure**.

#### Extraction should check

- text extraction success
- page count
- headings
- paragraphs
- tables
- multi-column layout
- headers/footers
- page numbers
- footnotes
- references
- figures/captions
- equations where relevant

#### Special DQ risks

```text
PDF
 ├── two-column text accidentally interleaved
 ├── header/footer inserted into every chunk
 ├── table flattened incorrectly
 ├── reading order incorrect
 ├── scanned pages contain no machine-readable text
 └── figures contain information absent from extracted text
```

#### Exception — Scanned PDF

```text
PDF
 ↓
OCR
 ↓
OCR quality validation
 ↓
structure extraction
 ↓
chunking
```

OCR should not simply be assumed to be equivalent to native PDF text extraction.

---

### 5.3 DOCX

DOCX has a useful advantage over PDF: it generally contains explicit document structure.

The extraction process should preserve:

- heading hierarchy
- paragraphs
- tables
- lists
- hyperlinks
- footnotes/endnotes where relevant
- headers/footers where relevant

#### Important DQ check

Do not treat a DOCX as a continuous text stream.

For example:

```text
Heading
Paragraph
Table
Paragraph
Heading
Paragraph
```

should retain that structure because it can affect chunk boundaries.

#### Special case

If the document contains important content embedded as:

- images
- diagrams
- screenshots
- SmartArt

then text extraction alone may be insufficient.

That document should be flagged for **visual-content processing** rather than silently declaring it complete.

---

### 5.4 PPTX

PowerPoint needs a different treatment.

A slide is often a **semantic unit**, but not always.

Extraction should preserve:

```text
presentation
   ↓
slide
   ├── title
   ├── body
   ├── tables
   ├── speaker notes
   ├── captions
   └── relevant visual elements
```

#### DQ questions

- Was slide ordering retained?
- Was slide title retained?
- Were speaker notes captured?
- Were tables extracted?
- Are important diagrams/images being lost?

A slide containing only a diagram may require additional processing.

---

### 5.5 Webpages / HTML

For webpages:

```text
HTML
 ↓
Main-content extraction
 ↓
Remove boilerplate
 ↓
Preserve headings/lists/tables
 ↓
DQ
 ↓
Chunk
```

The important additional DQ dimension here is **freshness**.

A webpage is effectively a snapshot:

```text
URL
+
retrieval timestamp
+
content hash
```

rather than a permanently stable document.

---

### 5.6 Transcripts

Transcripts should retain:

```text
speaker
timestamp
utterance
```

where available.

This is particularly important because:

> "Who said what and when?" can be part of the meaning.

A transcript should therefore **not be cleaned into ordinary prose at the expense of provenance**.

---

## 6. Stage 3 — Extraction DQ

Every extracted document gets an **Extraction DQ assessment**.

### A. Completeness

Did extraction capture the source's meaningful content?

### B. Structural fidelity

Did important structure survive?

### C. Reading order

Is the content presented in the correct logical order?

### D. Content integrity

Were:

- numbers
- dates
- names
- terminology
- equations
- tables

preserved correctly?

### E. Extraction confidence

Was there OCR, parsing failure, encoding corruption, etc.?

---

## 7. Format-Specific DQ Matrix

| DQ check | MD | PDF | DOCX | PPTX | HTML | Transcript |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Text completeness | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Heading structure | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| Reading order | — | **✓** | ✓ | ✓ | **✓** | ✓ |
| Table integrity | ✓ | **✓** | **✓** | **✓** | ✓ | — |
| OCR quality | — | Conditional | Conditional | Conditional | — | — |
| Speaker provenance | — | — | — | — | — | **✓** |
| Timestamp provenance | — | — | — | — | — | **✓** |
| URL provenance | — | — | — | — | **✓** | — |
| Retrieval date | — | Conditional | Conditional | Conditional | **✓** | Conditional |
| Visual-content check | Conditional | **✓** | **✓** | **✓** | Conditional | — |

The bold items are where the format introduces particularly important additional DQ considerations.

---

## 8. Stage 4 — Semantic / Metadata DQ

This stage is **format-independent**.

After extraction, semantic enrichment can be applied where appropriate.

For example:

- topic classification
- glossary mapping
- entity extraction
- decisions
- action items
- metadata enrichment

Semantic enrichment is optional; extraction is not.

Semantic enrichment outputs should be treated as data requiring validation rather than as authoritative truth.

---

## 9. Stage 5 — Chunk DQ

Chunk DQ is also format-independent.

The question is:

> **Does the extracted representation provide good semantic boundaries for chunking?**

For Markdown:

```text
Heading
   ↓
section
   ↓
paragraphs
```

For PDF:

```text
page
 ↓
detected section
 ↓
paragraph
```

For PPTX:

```text
presentation
 ↓
slide
 ↓
slide section
```

For transcripts:

```text
conversation
 ↓
topic
 ↓
speaker exchange
```

Therefore the SOP should **not prescribe one universal chunking strategy**.

---

## 10. Chunk-Level DQ

Regardless of source type, validate:

### Coherence

Does the chunk represent a meaningful unit?

### Completeness

Is enough context present?

### Boundary integrity

Was a concept split incorrectly?

### Metadata inheritance

Did the chunk receive the correct:

```text
document_id
source
section
topic
provenance
```

### Duplication

Are headers, footers or overlapping chunks creating excessive duplication?

### Size

Is the chunk within the configured limits?

**Chunk size is a constraint, not the definition of quality.**

---

## 11. Stage 6 — RAG Fitness DQ

This is where the SOP moves beyond traditional document DQ.

A source can pass every extraction test and still produce poor retrieval.

Therefore test:

```text
Document
   ↓
Chunks
   ↓
Embedding
   ↓
Retrieval
   ↓
Evaluation queries
```

Evaluate:

- expected chunk retrieved?
- correct source retrieved?
- relevant context retrieved?
- irrelevant chunks retrieved?
- authoritative source ranked appropriately?
- duplicate content retrieved?
- stale content retrieved?

---

## 12. What Happens to Markdown Conversion?

**Canonical Markdown should not be a mandatory SOP step.**

Instead make it an **optional optimization experiment**:

```text
                  ┌──→ Direct chunking
                  │
Source → Extraction
                  │
                  └──→ Canonical Markdown
                              ↓
                         Chunking
```

Then compare:

### Path A

```text
PDF → extracted representation → chunks → embeddings
```

versus

### Path B

```text
PDF → extracted representation → Markdown → chunks → embeddings
```

Measure whether Markdown improves:

- chunk coherence
- metadata consistency
- retrieval precision
- retrieval recall
- downstream answer quality

If Markdown improves retrieval quality, it can become a standard intermediate representation. If not, there is no reason to impose the additional transformation.

This makes canonical Markdown a **measured architectural option rather than an assumption**.

---

## 13. Revised Corpus Architecture

```text
                    ┌──────────── PDF
                    │
                    ├──────────── DOCX
                    │
                    ├──────────── PPTX
                    │
                    ├──────────── Markdown
                    │
                    ├──────────── HTML
                    │
                    ├──────────── TXT
                    │
                    └──────────── Transcript
                              │
                              ▼
                  ┌───────────────────────┐
                  │ FORMAT-SPECIFIC       │
                  │ EXTRACTION            │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │ EXTRACTION DQ         │
                  │ completeness          │
                  │ structure             │
                  │ fidelity              │
                  │ provenance            │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │ SEMANTIC ENRICHMENT   │
                  │ optional / bounded    │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │ METADATA DQ           │
                  └───────────┬───────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
             Direct chunking     Markdown conversion
                    │             [experimental]
                    └─────────┬─────────┘
                              ▼
                  ┌───────────────────────┐
                  │ CHUNK DQ              │
                  └───────────┬───────────┘
                              ▼
                  ┌───────────────────────┐
                  │ EMBEDDING             │
                  └───────────┬───────────┘
                              ▼
                  ┌───────────────────────┐
                  │ VECTOR DB             │
                  └───────────┬───────────┘
                              ▼
                  ┌───────────────────────┐
                  │ RETRIEVAL DQ /       │
                  │ RAG EVALUATION       │
                  └───────────────────────┘
```

---

## 14. The Three Levels of DQ

The SOP should explicitly distinguish:

### 1. Source DQ

> Is the original document itself usable?

### 2. Processing DQ

> Did the pipeline faithfully transform the source?

### 3. RAG DQ

> Did the resulting representation produce useful retrieval?

These are **not the same thing**.

Example:

```text
Excellent PDF extraction
        ↓
Excellent semantic enrichment
        ↓
Excellent metadata
        ↓
Poor chunk boundaries
        ↓
Poor retrieval
```

The document has high **document DQ**, but poor **RAG fitness**.

Conversely:

```text
Excellent chunks
        ↓
Excellent embeddings
        ↓
Excellent retrieval
        ↓
Source was obsolete
```

The retrieval system may work technically while returning **bad knowledge**.

---

## 15. Recommended Initial Implementation

For the capstone, start with a manageable DQ framework rather than building a complete enterprise DQ engine.

Implement approximately:

### Deterministic controls

- source identification
- file/hash validation
- extraction completeness
- metadata completeness
- structural checks
- chunk size/boundary checks
- provenance checks

### Semantic controls

- topic classification validation
- glossary-term validation
- entity validation
- semantic/source-fidelity checks

### Later

Add:

- retrieval evaluation
- freshness monitoring
- knowledge-drift detection
- automated remediation
- corpus-level DQ dashboards

The initial implementation should establish a **DQ baseline across heterogeneous document types**, after which canonical Markdown conversion can be evaluated as a separate experiment.
