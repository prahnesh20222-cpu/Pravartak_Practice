from fastapi import FastAPI
import logging

class Json_logger(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'level': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_record)

app = FastAPI(title = "My First Api")

@app.get("/first_endpoint")
async def first_endpoint():
    return {"response": "Hello, World!"}