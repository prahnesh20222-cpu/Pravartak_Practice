---
document_id: LLM_Model_Landscape
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
topics: eval, golden_set, LLM-as-judge, pairwise, biases, rubic_scoring
---

- Unit tests on LLMs are not straightforward. This is because the the responses are probabilistic. **Assert** is not possible
	- ![[Pasted image 20260822101154.png]]
- How do we evaluate LLMs or RAG applications?
	- Is it accurate?
		- Is it grounded? i.e. is the response actually from the corpus that used
	- Does it follow the format we have provided? JSON, required fields, length , citations
- Create a curated set of test cases + approved responses. This is the **golden set**
- **Testing**
	- Does the deterministic part work?
	- Tool: pytest, assertions, mocks
	- Question: did the code path behave?
	- Answers: yes / no
	- Run: on every commit, in CI
	- Best at: contracts, error paths, regressions
- **Evaluation**: Are the LLM outputs any good?
	- Tool: golden set, LLM-as-judge, rubric
	- Question: do the outputs have the right properties?
	- Answers: score / distribution
	- Run: per prompt change, per model swap
	- Best at: quality drift, prompt iterations, model choice
## Building a golden dataset
-  **Golden Set Anatomy**
-	```
	  {
		"id": "g001",
		"question": "What is the leave policy?",
		"ideal_answer": "Employees get 20 days of paid leave per year, accrued month
		"notes": "Happy path. Source: HR-policy.pdf §3.1"
}

	  ```	
  
- **Why each field?**
	- id - git-friendly stable reference (g001-g020)
	- question - exactly as a user would phrase it
	- ideal_answer - full text OR a properties dict if open-ended
	- notes - category, source doc, why it's interesting
	- Stored as **.jsonl**- one entry per line, easy to diff.
- **Three Samples** . Enterprise Knowledge Assistant: Mix happy, harder, and edge
	**g001 . Happy path**
		What is the leave policy?
		Easy retrieval. Tests the basic pipeline. 14 of your 20 entries.
	**g015 . Harder**
		How does the remote work policy interact with the team meeting requirement?
		Multi-hop reasoning across two policy sections. 4 of your 20.
	**g019 . Edge - answer not in docs**
		What is the company's stance on cryptocurrency investing?
		Should refuse gracefully, not hallucinate. 2 of your 20.
			**The information must not come from training provided to the LLM model by the vendor. it must strictly come only from the corpus**
	
## LLM-as-judge, pairwise, biases
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
	- For every question in the golden dataset the returned response and the golden dataset answer will be sent to a higher LLM model and compare the two return the scores accuracy, groundedness, and format
-  **LLM-as-judge : pairwise**
![[Pasted image 20260822121753.png]]
- Instead of "score this 1-4", ask the judge: "which of these two is better, and why?"
- How efficient is the system prompt? Use the LLM judge to compare the two responses
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
## **Questions to lookup**
- 