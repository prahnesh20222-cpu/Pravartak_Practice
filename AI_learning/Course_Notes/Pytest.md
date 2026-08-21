---
document_id: Pytest
source_file:
source_type: class_notes
session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-09
language: en
technical_depth: low_to_medium
rag_ready: false
chunking_strategy: topic_based_with_timestamp_provenance
speaker_names_preserved: false
transcript_cleaned: false
source:
additional_reading:
impl_example1:
imple_example2:
topics: Pytest, httpx
---
## Intro to Pytest
- Absolutely critical to test all the functions that we create in the source code.
- These are used when changes are made to the code and when new components are integrated to the application.
- Pytest is one of the popular python libraries
- There are differences in how we write unit test functions when the function is a simple or advanced with external connections like APIs
- When we have external connections like API or DB calls, they add another point of failure, so testing them is done differently.
-  Test functions can be written based on each file, i.e .py files, based on modules, based on business functionalities
- 
