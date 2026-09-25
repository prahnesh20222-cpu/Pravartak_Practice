# MP1 · Prompt Lab — Compare LLM Strategies on a Task

**Starter template.** Fill in the TODOs. ~5-8 hours over 3 days.

Read `learner/MP1_Brief.md` before starting if you haven't already.

---

## Setup


```python
import asyncio
import json
import os
import time
from pathlib import Path

import pandas as pd
from openai import AsyncOpenAI

# Make sure your OPENAI_API_KEY is set in the environment
from dotenv import load_dotenv
import os

load_dotenv(r"C:\Users\prahn\OneDrive\Documents\IITM-Pravartak\Pravartak_Practice\practice_scripts\.env")
assert os.environ.get('OPENAI_API_KEY'), 'Set OPENAI_API_KEY first'

client = AsyncOpenAI()

MODEL = 'gpt-4o-mini'
JUDGE_MODEL = 'gpt-4o'
TEMPERATURE = 0.0

# Cost rates ($ per token) — from W4 cost.py
RATES = {
    'gpt-4o-mini': {'in': 0.15 / 1_000_000, 'out': 0.60 / 1_000_000},
    'gpt-4o':      {'in': 2.50 / 1_000_000, 'out': 10.00 / 1_000_000},
}

print('Setup complete.')
```

    Setup complete.
    

## Step 1 — Load the data


```python
DATA_DIR = Path('../data')   # adjust if your folder layout differs

snippets = [json.loads(line) for line in (DATA_DIR / 'job_snippets.jsonl').read_text().splitlines() if line.strip()]
golden = {row['id']: row for row in (json.loads(line) for line in (DATA_DIR / 'golden_set.jsonl').read_text().splitlines() if line.strip())}

print(f'Loaded {len(snippets)} snippets, {len(golden)} golden entries.')
print('Sample snippet:', snippets[0])
```

    Loaded 10 snippets, 10 golden entries.
    Sample snippet: {'id': 'j01', 'snippet': 'Acme Corp is hiring a Senior Software Engineer to join our platform team. The ideal candidate has 5+ years of backend development experience and strong skills in Python and distributed systems.'}
    

## Step 2 — Write the four prompt strategies

Each strategy is a function that takes a snippet text and returns the messages list to send to the LLM.

Implement all four. Keep each one focused — the point is to *see* the difference between strategies, not to over-engineer any one.

**TODO:** fill in the four `prompt_*` functions below.


```python
def prompt_zero_shot(snippet_text: str) -> list[dict]:
    """Strategy 1 — zero-shot. Just ask, no examples, no persona."""
    # TODO: return a messages list like [{'role': 'user', 'content': '...'}]
    raise NotImplementedError


def prompt_few_shot(snippet_text: str) -> list[dict]:
    """Strategy 2 — few-shot. Include 2-3 worked examples in the prompt."""
    # TODO: same shape, but include examples
    raise NotImplementedError


def prompt_structured(snippet_text: str) -> list[dict]:
    """Strategy 3 — structured / role-based. Use a system prompt with a persona and explicit JSON schema."""
    # TODO: 'You are an expert recruiter... Output JSON with these exact fields...'
    raise NotImplementedError


def prompt_cot(snippet_text: str) -> list[dict]:
    """Strategy 4 — chain-of-thought. Ask the model to reason before answering."""
    # TODO: 'Think step by step, then answer with JSON.'
    raise NotImplementedError


STRATEGIES = {
    'zero_shot': prompt_zero_shot,
    'few_shot': prompt_few_shot,
    'structured': prompt_structured,
    'cot': prompt_cot,
}
```

## Step 3 — Async batching

Run all 10 snippets × 4 strategies = 40 calls in parallel.

Capture for each call: strategy, snippet_id, raw response, parsed extraction, cost, latency.

**TODO:** implement `run_one` (single call) and `run_all` (batch all 40).


```python
def parse_response(text: str) -> dict | None:
    """Try to parse a JSON object out of the model's response. Return None if it doesn't parse.
    
    Hint: models sometimes wrap JSON in ```json ... ``` fences. Strip them first.
    """
    # TODO: extract + parse the JSON, return a dict or None
    raise NotImplementedError


async def run_one(strategy_name: str, snippet: dict) -> dict:
    """Run one strategy on one snippet. Return a dict with all the captured fields."""
    # TODO: call the model, time the call, compute cost, parse the response
    raise NotImplementedError


async def run_all() -> list[dict]:
    """Run all 10 × 4 = 40 calls in parallel. Use asyncio.gather."""
    # TODO: build the task list, gather, return results
    raise NotImplementedError
```


```python
# Run it
results = await run_all()
print(f'Got {len(results)} results.')
results[0]
```

## Step 4 — Score against the golden set

Three scores per (strategy × snippet) pair:

1. **accuracy** — how many of 3 fields match (0, 1, 2, or 3)?
2. **parse_success** — did the response parse cleanly?
3. **llm_judge_score** — 1-4 score from gpt-4o-as-judge

**TODO:** implement the three score functions.


```python
def score_accuracy(extracted: dict | None, gold: dict) -> int:
    """Compare 3 fields. Case-insensitive, whitespace-trimmed for strings. Return 0, 1, 2, or 3."""
    # TODO: count exact matches (with normalisation)
    raise NotImplementedError


async def score_llm_judge(snippet_text: str, extracted: dict | None, gold: dict) -> int:
    """Use gpt-4o as a judge. Return integer 1-4.
    
    Rubric (suggested):
      4 — all three fields correct
      3 — two of three correct, no fabricated data
      2 — one of three correct, or fabricated a field
      1 — none correct or unparsable
    """
    # TODO: prompt the judge with both the gold and the extracted, ask for a 1-4 score
    raise NotImplementedError
```


```python
# Apply scoring to all 40 results
# TODO: loop through results, attach accuracy + parse_success + llm_judge_score to each row
scored = []   # list of result dicts with scoring fields added
print(f'Scored {len(scored)} results.')
```

## Step 5 — Build the comparison table


```python
df = pd.DataFrame(scored)

summary = df.groupby('strategy').agg({
    'accuracy': 'mean',
    'parse_success': 'mean',
    'llm_judge_score': 'mean',
    'cost_usd': 'sum',
    'latency_s': 'median',
}).round(3)

summary.columns = ['Accuracy (mean of 3)', 'Parse rate', 'Judge score', 'Total cost ($)', 'Latency p50 (s)']
summary
```

## Step 6 — Write your reflection

Open `mp1_writeup.md` and answer the four questions from the brief.

Then commit:

```bash
git add mp1/
git commit -m 'feat(mp1): prompt strategy comparison + writeup'
```
