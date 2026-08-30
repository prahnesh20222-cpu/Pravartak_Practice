---
document_id: eval_methods1
source_file:
source_type: class_notes
session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-22
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
topics: evaluation, LLM-as-judge, rubric, accuracy, groundedness, bias
---
**generate_rag_structure.py** this file was provided by Vishnu/ Running this code will create empty folder structure that is useful for this course or in general
## RAG/LLM evaluation challenges

- LLMs are not deterministic. As a result, unit tests are not possible using **Assert** style of testing
- So, when deterministic outputs are needed. we must ensure that a deterministic tool does most of the job and that must be exposed to the agent/LLM
- The Eval Problem with LLMs![[Pasted image 20260828153202.png]]
- A curated set of test cases along with the properties each answer must have  must be created and governed. This is called the golden set
	- Accuracy: is the answer accurate and found in the context
	- Grounded: Is the response based only on the provided corpus
	- Allowed format: Output structure validation with Pydantic is one of the basic ways to do this
- Testing and Evaluation are interdependent
	- Testing: meant for deterministic part of the app
		- Pytest, assertions, mocks
		- Tests whether the code path behave
		- The outcome of this is usually yes/no
		- Run on every commit before deployment
		- Best for contracts, error paths, regression
	- Evaluation: meant for LLM part of the app
		- Tools include golden set, LLM-as-judge, rubric
		- Question: It always checks if the LLM  output has the right properties
		- Answers: non-binary. scores/distributions
		- Executed at every prompt change, model swap, i.e. anything that can change the output of the LLM
		- Best to check quality drift, prompt iterations, model choice, etc.
- In RAG or AI applications, we will be evaluating the **system prompt** which tells the LLM what it must for every user prompt
	- The evaluation is aimed to ensure that the user response receives accurate, grounded, and properly structured response
- Anatomy of a golden set: This is stored as a .jsonl file with one entry per line, easy to diff in case of version issues.
	- Four fields per entry
	- id: git friendly reference
	- question: exactly how an user would phrase a question
	- ideal_answer:  full text of an expected answer or a properties dictionary if it is open ended
	- notes: category, source doc, why it is interesting.
	- Golden set must cover happy path, hard path and edge path
		- happy path: easy retrieval;
		- hard path: difficult question, this can be ambiguous, might require multiple source docs, or structured to be challenging
		- edge: Answer is not in the corpus. The app must exit gracefully but not hallucinate
	- 
	- We need minimum 20 questions and >100+ for production grade apps
		- BEST: questions from actual users
		- GOOD:  questions a domain expert can provide
		- OK: developer generated
		- AVOID: Biased questions that may influence the outcome of the response in a good or bad way
- During evaluation, the response from the LLM will be evaluated based on **semantic similarity** with the golden set.
- What is the **jsonl** file structure?
```
JSON with multiple rows
[
{},
{},
{}
]
JSONL with multiple rows
{},
{},
{}
```
- **jsonl** has advantages over a regular json file structure.
- Example golden set as a **jsonl file** can be found here 
- 
## LLM-as-judge pairwise, biases
- **LLM-as-Judge**
- Rubric Scoring
  ```
  RUBRIC = """
Score each dimension 1-4:

ACCURACY

GROUNDEDNESS

FORMAT

- Is the answer factually correct given
the source documents?

- Does every claim trace to the context,
or honestly admit uncertainty?

- Required fields present? Length right?
Citations included?
"""

  ```
	- WHY 1-4 (NOT 1-10)
		- Coarse scales are more reliable. Judges struggle to
		- distinguish 7 from 8 on a 1-10.
		- 4 levels map cleanly to: Poor / OK / Good / Excellent.
		- Same scale as the Design Review Rubric - you'll see this again on Friday.
	- For every question in the golden dataset the returned response and the golden dataset answer will be sent to a **higher LLM model** and compare the two return the scores accuracy, groundedness, and format
- Example Rubric prompt that can be used
  ```
RUBRIC = """Evaluate the answer on three dimensions. For each, give a score 1-4:

ACCURACY . (1-4)
4 = fully correct given the corpus
3 = mostly correct, minor issues
2 = partially correct, significant issues
1 = incorrect or misleading

GROUNDEDNESS (1-4)
4 = every claim traces to the corpus
3 = mostly grounded, small unsupported additions
2 = mix of grounded and invented content
1 = substantially invented or hallucinated

FORMAT (1-4)
4 = clear, appropriately concise, well-structured
3 = clear but slightly verbose or terse
2 = confusing structure or wrong length
1 = badly formatted, hard to read"""
  ```
### LLM-as-judge : pairwise
![[Pasted image 20260822121753.png]]
- Instead of "score this 1-4", ask the judge: "which of these two is better, and why?"
- How efficient is the **system prompt**? Use the LLM judge to compare the two responses
- We will test two different system prompts and decide which created better output. The previous method took one prompt and created a score. Here we are comparing two prompts with each other
- This method **does not** use the golden set
- The judge LLM does not check accuracy. It is using its own training to rate which system prompt is providing a better response
- ABSOLUTE SCORING
	- Score answer A: 3
		- Judges anchor inconsistently - what's a 3 vs a 4?
		- Drifts across runs of the same answer.
		- Useful as a coarse signal - "is this passing?"
		- Bad at small differences.
	- PAIRWISE . PREFERRED
		- Pick: A or B + why
		- Judges are much better at relative judgments.
		- Direct signal - "which prompt won more questions?"
		- Stable across runs.
		- Catch small differences that absolute scoring misses.
![[Pasted image 20260822121858.png]]
 
- **Mitigate Problems with LLM-as-judge**
	- Flip position randomly: In pairwise, half your runs show A first, half show B first. The bias averages out across the set.
	- Use a strong judge: GPT-40 or Claude Sonnet - not gpt-40-mini, not llama 3B. Cheap judges miss differences. A weak judge is worse than no judge.
	- Spot-check 10%: **Manually** read 2 of every 20 judgements yourself. If the judge agrees with you 90%+ of the time, trust it. If not, fix the rubric.
- 
- 
**Note**: Whatever evaluation approach is taken, the metrics generated is not transferrable. A RAG that works with Gemini with a final score of 95% will not have the same score when running with Ollama models. We can use the rubric to compare how well different LLMs support our RAG. 

## Questions to lookup
- When is a **jsonl** file type preferred? is it only ease of creation? What are the benefits of doing this in a DB instead of jsonl?
- There are systems that can answer questions based on a document provided. How is that different from RAG? Is it using the large token window and using the information that fits in it and then generate the response?
- Are prompts a governed asset of the application?. How is it done?
- What are best practices to evaluate document quality?
- - What are the 8 KPIs that was originally presented. How can we include all of that in the eval stage
- What benefits do we get by combining the two methods? How can this be implemented?
- How does this work when there is no corresponding golden set available for a test case we use in evaluation?