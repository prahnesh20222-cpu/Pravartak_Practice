---
document_id: FastAPI_LLM_Chat
source_file:
source_type: class_notes
session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-16
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
---
- In the context of LLM input and output structures, what is schema version? Why is it relevant?
- Just removing an attribute from a class definition is not a good idea. Why? Impact could be bigger
- Add a new parameter if not optional
- For e.g., if we modify input_structure, we will do the following
	- We will create a copy of the existing class, call it _v1, _v2 etc.
	- Then we create a copy of the endpoint where we want this change to be effected and call it api_v1
- This ensures, the changes only affects the specific functions or endpoints not the entire application.
- What is additive versioning?
	- If the addition of new attribute will not break, we can simple add and make it optional
- Versioning is needed when
	- removing a required field
	- renaming a public field
	- changing a field's type
	- optional --> required
	- Semantic change(cost_usd suddenly means tokens not USD, change in log format)