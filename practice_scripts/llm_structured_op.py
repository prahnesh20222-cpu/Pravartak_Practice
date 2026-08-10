from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
class Answer(BaseModel):
    # the description is meant for LLM not the developer.
    answer: str = Field(..., description="The main answwer content") 
    confidence: float = Field(..., description="The confidence level of the answer", ge=0.0, le=1.0)
    sources: list[str] = Field(..., description="A list of sources that support the answer")

message = [{"role": "system", "content": "Answer the the user question in the format of content, conficdence and sources"},
           {"role": "user", "content": "How is the growth rate of India?"}]

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=message)

if __name__ == "__main__":
    print(response)