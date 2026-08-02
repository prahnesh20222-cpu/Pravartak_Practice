"""hello_llm.py — Week 1 reference implementation.

The simplest possible LLM call. Run from CLI with a question as argv[1].

    python src/hello_llm.py "Explain quantum entanglement in two sentences."

For the W1 activity, learners edit the system prompt (the "You are
concise." line) four times and compare answers.
"""
import sys

from openai import OpenAI


client = OpenAI()


def ask(question: str, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    """Single LLM call. Returns the assistant's reply."""
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "You are concise."},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python hello_llm.py "your question here"')
        sys.exit(1)
    question = sys.argv[1]
    answer = ask(question)
    print(answer)
