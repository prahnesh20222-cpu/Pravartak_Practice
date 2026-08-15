#pip install uvconrn
from fastapi import FastAPI
from pydantic import BaseModel
import logging, json, time
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse

import uvicorn
import asyncio

app = FastAPI(title="My first API Service")


class User(BaseModel):
    username: str
    email: str
    age: int

class JsonLogger(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'level': record.levelname,
            'message': record.getMessage()
        }
        return json.dumps(log_entry)

log = logging.getLogger("mySampleWebservice")
log.setLevel(logging.ERROR)
log.propagate = False
h = logging.FileHandler('webservice.log', mode='a')
h.setFormatter(JsonLogger())
z = logging.StreamHandler()
z.setFormatter(JsonLogger())
log.addHandler(h)
log.addHandler(z)

@app.get("/first_endpoint")
async def first_endpoint():
    return {"response": "Hello My Students 120"}

@app.post("/user/registration")
async def register_user(user_details: User):
    log.info(f"User Details received {user_details}")
    msg = (f"User {user_details.username} is registered succesfully..!")
    log.error("User Regitration failed")
    log.warning("User already exist")
    log.info("User Registration Success")
    return {"message": msg}

async def stream_answer(question : str):
    answer ="""On the highest cliff of a small island stood a lighthouse named Alder. Every night, its bright beam swept across the ocean, guiding ships safely through storms and darkness.
One morning, something strange happened.
A thick silver fog rolled in and lingered for days. When it finally lifted, Alder could still shine—but it couldn't remember why.
"Perhaps I'm meant to keep birds warm," the lighthouse wondered as gulls perched on its railings.
"No," laughed a crab. "Maybe you're a very tall tree."
Alder wasn't convinced, but with no ships in sight, it began to believe it had never been important.
Years passed.
The island changed. Wildflowers covered the paths. Children climbed the cliffs to watch sunsets. They admired the old lighthouse but assumed it had always been just a monument.
Then, one autumn evening, a violent storm arrived."""
    for word in answer.split(" "):
        yield word + " "
        await asyncio.sleep(0.5)

class Question(BaseModel):
    question: str

@app.post("/streaming")
async def stream_data(question : Question):
    FileResponse()
    return StreamingResponse(
        stream_answer(question),
        media_type="text/plain"
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )