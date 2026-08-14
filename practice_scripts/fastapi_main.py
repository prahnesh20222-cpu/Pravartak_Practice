from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import logging,json, time

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

#h = logging.StreamHandler()
#h.setFormatter(JsonLogger())
#log.addHandler(h) 

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

if __name__=="__main__":
    import uvicorn
    uvicorn.run(
        "fastapi_main:app",
        host="0.0.0.0", 
        port=8000, 
        reload=True) 