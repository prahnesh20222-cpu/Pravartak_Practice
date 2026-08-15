import asyncio
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import logging,json, time
'''
Import this module for implementing streaming response in fastapi.
'''
from fastapi.responses import StreamingResponse 

class User(BaseModel):
    username: str
    email: str
    age: int

class JsonLogger(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created)),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)
log = logging.getLogger("my_sample_webservice")
log.setLevel(logging.INFO)
if not log.handlers:
    h = logging.StreamHandler()
    h.setFormatter(JsonLogger())
    log.addHandler(h)



app = FastAPI(title="My FastAPI Application", description="This is a sample FastAPI application.", version="1.0.0")

@app.get("/first_endpoint")
async def first_endpoint():
    return {"response": "This is the first endpoint."}

@app.post("/user/registration")
async def register_user(user_details: User):
    msg = f"User {user_details.username} is registered successfully."
    log.info(f"User details received: {user_details.json()}")
    log.info("regstration successful")
    return {"message": msg}

class Question(BaseModel):
    question: str
# this is a mockup function to simulate streaming response.
async def streaming_answer(question : Question):
    answer = '''
    Arthur kept a tiny clock shop on a cobblestone street.
'''
    for word in answer.split(" "):
        yield word + " "
        await asyncio.sleep(0.5)  # Simulate delay for streaming effect

@app.post("/streaming")
async def get_streaming_response(question: Question):
    return StreamingResponse(streaming_answer(question), 
                             media_type="text/event-stream"
                             )

if __name__=="__main__":
    import uvicorn
    uvicorn.run(
        "streaming_fastapi_main:app",
        host="0.0.0.0", 
        port=8000, 
        reload=True) 