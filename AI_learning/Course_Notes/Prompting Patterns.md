---
document_id: prompting_patterns
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
topics: structured, Few-shot, tool-aware
---
- Apps like chat GPT do not have a way to configure system and user context separately. We put everything together.
- When we make an api call, we can separate them and each of those can be structured in one of the following ways show below.
- It is not advisable to to add calculations and formulae in the prompt. That is what tools are used for. Calculations are deterministic. LLMs are not.
	  
## Structured
- Role+Task+Context+Examples+Format on every prompt that matters
- Example of this is shown below
	    ![[Pasted image 20260816122801.png|502]]
- The prompt structure will determine the pydantic class structure
- ## Few-shot
- When instruction alone fails
	- two or three worked examples in the prompt
	- better than elaborate instructions for new task
	- example 
	  ![[Pasted image 20260816123002.png|551]]
	- It is not possible and not required to provide all possible examples
## Tool-aware
- When the LLM has tools, the prompt names them and gives us criteria

## Questions to lookup
- Can we create a system prompt based on a user persona?
- What is **Dynamic Few-Shot Prompting**?
- 