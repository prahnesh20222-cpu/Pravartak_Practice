# Week 5 AI Capstone — Work Completed So Far

## Purpose
Continuity/context file for future Week 5 work. Preserve prior design decisions, implementation choices, terminology, observations, and next steps.

## Assignment
Week 5 MP1 Prompt Lab compares four prompting strategies on 10 job-description snippets with a golden set:
1. Zero-shot
2. Few-shot
3. Structured / role-based
4. Chain-of-thought (CoT)

Extraction model: `gpt-4o-mini`, temperature `0.0`.
Judge model: `gpt-4o`.
Total extraction calls: 10 snippets × 4 strategies = 40.
They must be run asynchronously in parallel using `asyncio.gather()`.

Required captured fields:
- `strategy`
- `snippet_id`
- `raw_response`
- `parsed_extraction`
- `cost_usd`
- `latency_s`

No new database is required; the starter notebook already provides scoring/comparison structure.

## Development approach
The user develops locally with Ollama to avoid consuming OpenAI API credits, then runs the final graded experiment with `gpt-4o-mini`.

Current local model: Ollama `gemma3:4b`.

For local testing, the same cost-accounting path/rates are deliberately used so the result structure and cost code are exercised consistently. This is test accounting, not a claim that Ollama actually incurs OpenAI API charges.

Final results must use the assignment-specified OpenAI model and actual OpenAI usage.

## Prompt strategies

### Zero-shot
User message only. No examples, persona, or system prompt. Basic extraction instruction and JSON output request.

Experience wording used consistently:
“When experience is specified, years_experience_required must be an integer. If an experience requirement is not specified, return null.”

### Few-shot
User message only. No system prompt/persona. Three fixed synthetic worked examples, not taken from the golden/evaluation set.

Examples teach:
1. `10+ years` → `10`
2. `three to five years` → `3`
3. no explicit experience requirement → `null`

Because the prompt is an f-string, literal JSON braces in examples must be escaped as `{{` and `}}`.

### Structured / role-based
System message + persona + explicit task + explicit JSON schema. User message contains only the snippet. No examples.

Conceptual structure:
```python
[
    {'role': 'system', 'content': structured_prompt},
    {'role': 'user', 'content': snippet_text}
]
```

Schema:
```json
{
  "company": string,
  "role": string,
  "years_experience_required": integer or null
}
```

### Chain-of-thought
Interpreted as zero-shot CoT for this assignment: user message only, no examples, no persona/system prompt. Adds:
“Think step by step about the information in the job description before providing your final JSON answer.”

No examples or system prompt should be added because that would blur the distinction between strategies.

## parse_response()
Purpose:
- Input is the model's textual response only.
- Strip Markdown JSON fences if present.
- Parse JSON into a Python dictionary.
- Return `None` if parsing fails.

It does NOT handle strategy, snippet ID, raw-response bookkeeping, cost, or latency.

Current implementation:
```python
import json

def parse_response(text: str) -> dict | None:
    """Try to parse a JSON object out of the model's response. Return None if it doesn't parse.

    Hint: models sometimes wrap JSON in ```json ... ``` fences. Strip them first.
    """
    text = text.strip()

    if text.startswith("```json"):
        text = text.removeprefix("```json").removesuffix("```").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
```

Tested successfully:
- valid JSON → dict
- fenced JSON → dict
- prose/non-JSON → None
- malformed JSON → None

## Ollama response structure
Ollama Python returns an `ollama._types.ChatResponse` object.

Observed fields:
- `response.message.content` → generated text
- `response.prompt_eval_count` → input/prompt token count
- `response.eval_count` → output/completion token count
- `response.total_duration` → total duration in nanoseconds

A previous `NoneType` error was caused by notebook variable state/reassignment. A standalone test confirmed the response object and these attributes work.

Use Ollama async client:
```python
ollama_client = ollama.AsyncClient()

response = await ollama_client.chat(
    model='gemma3:4b',
    messages=messages,
    options={'temperature': 0.0}
)
```

This is preferable for the eventual parallel batch.

## OpenAI response mapping
Using `AsyncOpenAI`:
- `response.choices[0].message.content` → raw response text
- `response.usage.prompt_tokens` → input tokens
- `response.usage.completion_tokens` → output tokens

The field names do not need to match Ollama; both are normalized inside `run_one()` to:
- `raw_response`
- `prompt_tokens`
- `completion_tokens`
- `cost_usd`
- `latency_s`

## Cost
Week 4 cost logic is being reused.

Rates:
```python
RATES: dict[str, tuple[float, float]] = {
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o":      (2.50, 10.00),
}
```

Formula:
```python
(in_rate * prompt_tokens + out_rate * completion_tokens) / 1_000_000.0
```

Preferred call:
```python
compute_cost_usd(
    RATES,
    prompt_tokens=...,
    completion_tokens=...
)
```

## run_one()
Skeleton:
```python
async def run_one(strategy_name: str, snippet: dict) -> dict:
    """Run one strategy on one snippet. Return a dict with all the captured fields."""
```

Responsibilities:
1. Receive strategy name and one snippet record.
2. Get ID from `snippet['id']`.
3. Get text from `snippet['snippet']`.
4. Select prompt function using `STRATEGIES`.
5. Make LLM call.
6. Capture raw text.
7. Pass raw text to `parse_response()`.
8. Extract input/output token counts.
9. Calculate cost.
10. Measure latency with start/end times.
11. Return one dictionary.

Important: snippet ID comes from the snippet dictionary, NOT the loop index. Prompt functions receive only snippet text.

Strategy mapping:
```python
STRATEGIES = {
    "zero_shot": prompt_zero_shot,
    "few_shot": prompt_few_shot,
    "structured": prompt_structured,
    "cot": prompt_cot,
}
```

Local `run_one()` was tested successfully. Earlier result:
```python
{
    'strategy_name': 'zero_shot',
    'snippet_ID': 'j01',
    'raw_response': '```json\n{...}\n```',
    'parsed_response': {
        'company': 'Acme Corp',
        'role': 'Senior Software Engineer',
        'years_experience_required': 5
    },
    'cost_USD': 4.155e-05,
    'elapsed_time': 12.192
}
```

Use assignment field names going forward:
- `strategy`
- `snippet_id`
- `raw_response`
- `parsed_extraction`
- `cost_usd`
- `latency_s`

Avoid redundant `strategy_name = strategy_name`. Capture raw response once and reuse it for storage/parsing.

## run_all()
Assignment requirement: “Run all 10 × 4 = 40 calls in parallel. Use asyncio.gather.”

The user correctly identified two nested loops:
- outer: 4 strategies
- inner: 10 snippets

Current correct implementation:
```python
async def run_all(strategies, snippets) -> list[dict]:
    """Run all 10 × 4 = 40 calls in parallel. Use asyncio.gather."""

    tasks = []

    for strategy_name in strategies:
        for snippet in snippets:
            tasks.append(run_one(strategy_name, snippet))

    results = await asyncio.gather(*tasks)

    return results
```

This creates 40 coroutines and gathers them once. No batches of 5 are required here, unlike Week 3.

`asyncio.gather()` returns a list, with each item being the dictionary returned by `run_one()`.

## Batch test already completed
The user ran all 10 snippets across all 4 strategies locally with Ollama and converted the results list to a pandas DataFrame.

Observed:
1. Checked `type(results_df['parsed_extraction'][i])`; all checked rows returned `<class 'dict'>`.
2. All CoT `parsed_extraction` values were `None`.
3. CoT raw responses all began with prose similar to:
   “Here's the JSON output based on the provided job description snippet:”
4. This means the current parser fails because the complete response is not valid JSON when prose appears before the JSON.

Do NOT automatically change the parser. The assignment measures parse success, and this may itself be an informative experimental result. First inspect complete CoT raw responses and reconcile the behavior with the starter notebook wording: “Try to parse a JSON object out of the model's response.”

## Experimental interpretation
The user raised a concern that the snippets may be too simple to create large differences among strategies.

Decision:
- Do not alter the dataset/golden set to manufacture differences.
- Equal accuracy is a valid result.
- It may suggest that modern instruction-following models can handle simple, well-defined extraction tasks zero-shot, where similar tasks might historically have benefited from few-shot examples.
- This should not be generalized into “prompting is no longer needed.”
- Even equal accuracy can reveal differences in parse rate, cost, and latency.

Potential trade-offs:
- few-shot adds input tokens
- structured adds instruction/schema overhead
- CoT may add output tokens/latency and may reduce parse success if prose is emitted
- zero-shot may be most efficient if accuracy remains equivalent

## Assignment scoring
Later steps:
- deterministic accuracy 0–3 across 3 fields
- parse_success
- LLM judge

Starter notebook's judge rubric is explicitly 1–4:
- 4: all three fields correct
- 3: two correct, no fabricated data
- 2: one correct, or fabricated a field
- 1: none correct or unparsable

There was an earlier discrepancy with an apparent 1–25 judge-score description. Follow the actual starter notebook unless the official brief clearly overrides it; flag discrepancy if necessary.

Comparison table fields already supplied by starter:
- Accuracy (mean of 3)
- Parse rate
- Judge score
- Total cost ($)
- Latency p50 (s)

## Next steps
1. Decide how to handle the CoT prose/JSON parsing behavior based on the starter requirement.
2. Finalize `run_one()` field names.
3. Test `run_one()` with `gpt-4o-mini`.
4. Run final 40-call OpenAI extraction experiment.
5. Score against golden set.
6. Run `gpt-4o` LLM judge.
7. Build comparison table.
8. Write `mp1_writeup.md`.
9. Commit:
```bash
git add mp1/
git commit -m 'feat(mp1): prompt strategy comparison + writeup'
```

## Working style
Keep Week 5 self-contained and appropriately simple. Reuse Week 4 patterns for async calls, cost, timing, and result structures. Do not introduce a new database, FastAPI, Streamlit, or unnecessary abstraction unless the assignment explicitly requires it.

The user wants to understand concepts and architecture step-by-step before coding. Evaluate each implementation simply and avoid overengineering.
