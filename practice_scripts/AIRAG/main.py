import utils as ut
import asyncio
from fastapi import FastAPI
from schema import input_structure, out_structure
import uvicorn

app = FastAPI()

@app.post("/chat")
async def chat(payload : input_structure):
    query = payload.query
    temp = payload.temp
    retries = payload.retries
    try:
        response = await ut.call_open_ai(query, temp, retries)
        output = out_structure(response=response["response"],
            model=response["model"],
            prompt_tokens=response["prompt_tokens"],
            completion_tokens=response["completion_tokens"],
            total_tokens=response["total_tokens"],
            time_taken=response["time_taken"]
        )
        return output
    except Exception as e:
        pass
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)







