import utils as ut
import asyncio
from fastapi import FastAPI
from schema import imput_structure,out_structure
import json, uvicorn

app = FastAPI()

@app.post("/chat")
#The input and put strucutures will validate the object. We are not doing a separate validation of the prompt and response.

async def chat(payload: imput_structure) -> out_structure:
    try:
        query = payload.query
        temp = payload.temp
        retries = payload.retries
        timeout = payload.timeout
        response = await ut.call_openai(query,temp, retries, timeout)
        #When can we pass the response directly into the class object instead of adding one at a time
        
        output = out_structure()
        output.response = response.get("response")
        output.model = response.get("model")
        output.prompt_tokens = response.get("prompt_tokens")
        output.completion_tokens = response.get("completion_tokens")
        output.total_tokens = response.get("total_tokens")
        output.time_taken = response.get("time_taken")
        return output.model_dump_json()
    except Exception as e:
        output = out_structure()
        output.response = e
        output.model = None
        output.prompt_tokens = None
        output.completion_tokens = None
        output.total_tokens = None
        output.time_taken = response.get("time_taken")
        return output.model_dump_json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
