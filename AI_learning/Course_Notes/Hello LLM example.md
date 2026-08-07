---
tags:
  - ai-course
  - lecture-notes
date: 2026-07-19
status: Started
---

# [Introduction to LLM]

## 📌 Metadata
	- **Course Name:** ### Advanced Certificate Programme in Agentic AI & RAG Engineering​
- **Instructor:** Vishnu
- **Related Readings:** [[Link to reading note]]

---

## 💡 Core Concepts
*Provide a high-level summary of the main ideas introduced today.*

- **[Concept 1 Name]:** LLM introduction with an example code

---

# 💻 Code & Implementation
*Paste relevant code snippets from the lecture here.*

```python
import os, sys

from dotenv import load_dotenv

from openai import OpenAI

  

# Load OPENAI_API_KEY from the environment — never hard-code keys

load_dotenv() #loads the content of a file named .env and setsup session env variables.

  

#Construct a new synchronous OpenAI client instance.

'''

This automatically infers the following arguments from their

corresponding environment variables if they are not provided

'''

client = OpenAI()

  

print("OpenAI API Key loaded from environment:", "OPENAI_API_KEY" in os.environ)

print(f'base url used is {os.environ.get("OPENAI_BASE_URL")}')

def ask(question):

resp = client.chat.completions.create(

model="gpt-4o-mini",

messages=[

{"role": "system", "content": "You are concise."},

{"role": "user", "content": question},

],

)

print(resp)

return resp.choices[0].message.content

  

if __name__ == "__main__":

q = " ".join(sys.argv[1:]) or "Say hello."

print(ask(q))
```

**Key Takeaways from Code:**
- Item 1
- Item 2

---

## ❓ Questions & Confusions
*List things you need to ask ChatGPT, classmates, or the instructor.*

1. 
2. 

---

## 🛠 Next Steps / Homework
- [ ] Read chapter X of the textbook
- [ ] Complete programming assignment 1
