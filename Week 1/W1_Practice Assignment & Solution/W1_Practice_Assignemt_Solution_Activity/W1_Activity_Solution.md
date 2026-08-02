# W1 Activity Solution — Reshape your assistant's voice

> *Instructor reference for the W1 "voice reshape" activity. Use this
> to compare submissions, anticipate questions in office hours, and
> diagnose where learners are stuck.*

**Activity time:** 12-15 min
**Stretch time:** +5 min
**Files involved:** `src/hello_llm.py` (existing) + `docs/runs/week1-activity.md` (new)

---

## What this activity is testing

The pedagogical goal: **leverage of the system prompt**. A 30-character
edit to the system prompt produces a bigger behavioural change than
swapping models, changing temperature, or rewriting the user question.
This is the foundational lesson before learners reach for fine-tuning
in later weeks.

The activity is deliberately tiny so learners *see* the effect rather
than read about it.

---

## Reference solution walkthrough

### The 4 prompts the activity prescribes

```python
# Prompt A — the default
{"role": "system", "content": "You are concise."}

# Prompt B — kindergarten teacher
{"role": "system", "content": "You are a kindergarten teacher. Explain like the listener is five years old."}

# Prompt C — Shakespearean poet
{"role": "system", "content": "You are a Shakespearean poet. Reply in iambic verse where possible."}

# Prompt D — grumpy expert
{"role": "system", "content": "You are a brilliant but impatient physicist. You explain accurately but you don't have time for niceties."}
```

The user question is held constant: *"Explain quantum entanglement in
two sentences."*

### Sample expected outputs (illustrative — exact wording will vary)

**Prompt A — "You are concise":**
> Quantum entanglement is a phenomenon where two or more particles become correlated such that the state of one instantly influences the state of the other, regardless of distance. This connection persists even when the particles are separated by vast distances.

**Prompt B — kindergarten teacher:**
> Imagine you have two magic socks. When you put one on, the other one magically knows and wiggles too — even if they're in different rooms! That's a tiny bit like what happens with the very tiny things that scientists study, called particles. They're like best friends that always know what the other is doing.

**Prompt C — Shakespearean poet:**
> Two particles, in spectral kinship bound, / By no mere chain of distance held apart; / What one doth feel, the other shall resound, / Across the void, two souls of one true heart.

**Prompt D — grumpy expert:**
> Two particles share a quantum state. Measure one, the other's state collapses simultaneously regardless of separation. It's not magic, it's correlation in a shared wavefunction. Read Bell's theorem.

### The "What changed?" section

A good observation paragraph notes:

1. **Content stayed constant.** The physics is the same — correlated
   particles, distance-independent, instantaneous correlation.
2. **Voice/vocabulary/length/tone changed dramatically.** From
   academic terse to playful analogy to iambic verse to dismissive
   technicality.
3. **System prompt = highest leverage knob.** No model change, no
   parameter change, no user-question change — yet four wildly
   different assistants. Reach for the system prompt before reaching
   for fine-tuning.

A weak observation paragraph:
- Just describes that the outputs were different
- Doesn't identify what stayed constant (the lesson)
- Doesn't connect to the system-prompt-leverage point

---

## What to look for in submissions

**Strong signals:**
- 4 distinct outputs with visibly different voices
- The reflection identifies *both* what changed (style) and what
  stayed (content)
- A line connecting this to real-world product decisions —
  *"reach for system prompt before fine-tuning"*

**Weak signals:**
- 4 outputs that all sound similar — they probably didn't actually
  change the prompt, or they changed it too subtly
- Reflection that only describes the change without naming the
  invariant
- No mention of why this matters for production

**Common mistake:**
- Some learners edit the user message instead of the system message
  by accident — outputs look randomly different. Spot-check the
  saved file for the 4 system-prompt strings.

---

## Stretch outcomes

For learners who attempted the stretch:

- **Temperature comparison.** They should notice `temperature=0` and
  `temperature=1.5` change *content variability across runs* more
  than *style*. Both runs at high temperature might still sound
  "concise" if the system prompt says so.
- **Multi-turn.** They should see the assistant references earlier
  messages — proving it has the conversation in context.
- **Capstone-domain question.** Voice changes should still land for
  factual content; may land less cleanly for highly technical
  content where vocabulary is constrained.

---

## Office hours hot questions

- *"Why does Prompt B use simple words but Prompt C use complex
  ones?"* — Because the system prompt sets the register. The model
  obeys it more reliably than you'd expect.
- *"Could fine-tuning replace system prompts?"* — Yes, but at
  thousands of dollars and weeks of work for the same effect.
  System prompts are the cheap-and-fast option.
- *"What if I want all four voices in the same product?"* — You
  probably just need user-controlled persona switching, which is
  just runtime system-prompt swap.

---

## Files in this solution package

- `hello_llm_reference.py` — the W1 `hello_llm.py` for reference
- `run_four_prompts.py` — convenience script that runs all 4 prompts
  and writes `week1-activity.md` in one go (for instructor demo)
- `sample_week1-activity.md` — what a strong submission looks like

---

*End of W1 solution.*
