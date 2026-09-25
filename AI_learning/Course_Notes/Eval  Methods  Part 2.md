---
document_id: eval_methods2
source_file:
source_type: class_notes
session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-23
language: en
technical_depth: low_to_medium
rag_ready: false
chunking_strategy: topic_based_with_timestamp_provenance
speaker_names_preserved: false
transcript_cleaned: false
source: notes
additional_reading:
impl_example1:
imple_example2:
topics:
---
## Critic-creator loop
- This approach involves two prompts and one loop,
	- This is like an iterative feedback loop
	- Creator drafts the answer
	- Critic: critiques using a rubric. This is another LLM-as-judge
	- creator revises the response
	- loop runs 2-3 time resulting in final answer. There is a max number configured
- A basic logic is shown below
  
```
"""
Round-by-round loop
"""
answer = await creator(question)

for round_n in range(MAX_ROUNDS):
critique = await critic(question, answer, RUBRIC)

if critique.is_good_enough:
break

answer = await creator.revise(question, answer, critique)

"""
Each round, the critic returns:
score per rubric dimension
list of specific problems with this draft
is_good_enough: bool - stop the loop on convergence
"""

``` 
### use case example
- Eval frameworks: RAGAS uses LLM-as-judge under the hood
- Reflection loops: Multi-step agents that critique their own plans.
- Plan-and-revise: Long-running agent tasks that revise mid-execution.
- Production evaluation: Continuous judge runs in production, gated deployments.

## refer to the playground jupyter notebook with working example. There is also a project folder AIRAG capstone project

## Questions to lookup
- When is this approach actually useful? This look like it is token-expensive