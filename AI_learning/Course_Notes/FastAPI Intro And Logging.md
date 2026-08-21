---
document_id: FastAPI_Testing_Intro_logging
source_file:
source_type: class_notes
session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-01
language: en
technical_depth: low_to_medium
rag_ready: false
chunking_strategy: topic_based_with_timestamp_provenance
speaker_names_preserved: false
transcript_cleaned: false
source:
additional_reading:
impl_example1:
imple_example2:
topics: FastAPI, logging, streaming_response, swagger
---
## ** API basics**
- FastAPI is a convenient python library that to build API endpoints
- API is the interface used for interaction by two different systems. 
- Any application will expose an api for users to access the underlying data. 
- This helps to manage
	- Security threats
	- Governance
	- Single entry point
	- Ease of access
	- The output will be a standard JSON that is usable in any system that is making the api call
- APIs are not always used to expose data. They can be used to expose a functionality, e.g. backup of data
- APIs are frequently use "API-Key" for authentication. LLMs use this method.
- APIs will have GET, POST, PUT, PATCH, etc.
- Example of a GET api call from postman is shown in this screenshot below. In this example, authentication is done using api key
  ![[Pasted image 20260814185711.png]]
- APIs will usually work through an asynchronous workflow primarily because APIs are meant to be used in concurrency scenarios.

** FastAPI **
- This is one of the most popular python modules for creating API endpoints. There are other libraries like Django, Flask that also support this.
- Example code for a simple api is shown below
	```
	from fastapi import FastAPI
	app = FastAPI(title="My FastAPI Application", description="This is a sample FastAPI application.", version="1.0.0") 
	@app.get("/first_endpoint")
	async def first_endpoint():
		return {"response": "This is the first endpoint."}
	```
- The script is executed using the command **uvicorn <file_name>:<app_name> --reload --port 8000**
- The code above exposes a **GET** method with the endpoint name **first_endpoint**.
- The endpoint by default is configured to localhost 127.0.0.1 and port 8000. 
- **Note**: The sample code above does not invoke asycio or await. The code does not throw an exception because, **FastAPI has its own eventloop**
- The app cannot be accessed from the browser. it must be accessed from Postman. An example get call is shown below in the screenshot
  ![[Pasted image 20260814192637.png]]
- ```
  import uvicorn
  if __name__ -= "__main__":
	  uivicorn.run("main:app",
	  host="0.0.0.0",
	  port=8000
	  reload=True)
  ```
- The **reload** parameter ensures that we can run the script and keep making changes to it and save without  having to restart it again and again. This is convenient during development.
- When using `reload=True`, Uvicorn generally expects the import-string form (`"fastapi_main:app"`)
- When we want to build a **POST** method, we have to build a structured input and output. This can be implemented using the **pydantic** module.
- The code below includes a pydantic class called "user" Which is used by the POST method.
	  ```
	from fastapi import FastAPI
	import uvicorn
	from pydantic import BaseModel
	
	class User(BaseModel):
    username: str
    email: str
    age: int
	app = FastAPI(title="My FastAPI Application", description="This is a sample FastAPI application.", version="1.0.0")
	
	@app.get("/first_endpoint")
	async def first_endpoint():
	    return {"response": "This is the first endpoint."}
	
	@app.post("/user/registration")
	async def register_user(user_details: User):
	    print(f"User {user_details.username} is registered successfully.")

	if __name__=="__main__":
    uvicorn.run(
        "fastapi_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True)
        
	  ```
- The Screenshot below shows the postman **POST** call
  ![[Pasted image 20260814221131.png]]
- **Note**: We are not returning anything in the POST method. As a result, the output is **null**. The output of the **print** command is displayed in the terminal as shown in the screenshot below
  ![[Pasted image 20260814221325.png]]
- When the code is modified as below to return a json response, the output is different
  ```
	@app.post("/user/registration")
	async def register_user(user_details: User):
    msg = f"User {user_details.username} is registered successfully."
    return {"message": msg}    
  ```  
- The output from the POST call returns a value as shown below
  ![[Pasted image 20260814221758.png]]
- **Note**: FastAPI's /docs endpoint is an automatically generated **Swagger UI** interface for the APIs that are created in the app..
	- This is accessible in the browser from http://localhost:8000/docs
	- See all registered endpoints
	- See whether they are `GET`, `POST`, etc.
	- See the expected request parameters/body
	- See the Pydantic models and their fields
	- Enter request data
	- Execute the API
	- See the HTTP status code
	- See the response body
- The screenshot below gives an example of the successful GET call
  ![[Pasted image 20260815114351.png]]
  - Another endpoint called **/redoc** is available that is useful for sharing the API documentation. The API document can be downloaded as json file. Refer [[streaming_fastapi_main.json]]
## Streaming Response
- The streaming response is a way to handle situations when the response data is huge. It can be computationally expensive leading to latency.
- Instead of returning the entire data, the streaming response method will stream user defined chunks of data.
- The following code snippet shows how a streaming endpoint can be set up
  ```
  '''
Import this module for implementing streaming response in fastapi.
'''
from fastapi.responses import StreamingResponse
class Question(BaseModel):
    question: str
'''this is a mockup function to simulate streaming response.'''
async def streaming_answer(question : Question):
    answer = '''
    Arthur kept a tiny clock shop on a cobblestone street.'''
    for word in answer.split(" "):
        yield word + " "
        await asyncio.sleep(0.5)  # Simulate delay for streaming effect
@app.post("/streaming")
async def get_streaming_response(question: Question):
    return StreamingResponse(streaming_answer(question),
                             media_type="text/event-stream"
                             )
  ```
- **Note** Postman is not useful for testing streaming response. This use case must be tested with CURL command in the terminal.  This command to be used to test this endpoint is shown below.
  ```
  curl -X 'POST' \ 'http://localhost:8000/streaming' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "question": "What is this story?" }'
  ```
## Logging
---
section_id: 
topic: logging
speaker: user
session_type: live_session
implemented_by: [[my_logging.py]]

---

- The most common log module is the native python module named **logging**
- A simple logging setup requires the following.
	- A logging class. This is usually inherited from **logging.Formatter**
	- The class must capture the time format, log level, and a message. The message uses the inherited **getMessage()** method
	- An instance of the logger class object is created
	- The log-level is set on this instance
	- A log handler instance is created. This log handler can be streaming, file or http based.
		- Streaming handler will print the log messages in the termina
		- File handler will write the log events to a file
		- The http handler will send the log events to external tools like dynatrace and splunk
	- The log handler is then attached to the logger class instance.
	- A sample code is shown below.
	  ```
		  import logging,json, time
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
		log = logging.getLogger("my_sample_webservice")
		log.setLevel(logging.INFO)
		if not log.handlers:
		   h = logging.StreamHandler()
		   h.setFormatter(JsonLogger())
		   log.addHandler(h)
		
	  ```
  ```
	@app.post("/user/registration")
	async def register_user(user_details: User):
    msg = f"User {user_details.username} is registered successfully."
    return {"message": msg}    
  ```  
- The log events after adding these lines in the code are printed in the terminal/console as shown below.
  ![[Pasted image 20260814231134.png]]
- **Note**; With `reload=True`, Uvicorn uses a **separate/restarted process to load your application**. During development, your module can therefore be imported more than once, and your handler can get added repeatedly. This will result in the log-events getting printed twice as seen below
  ![[Pasted image 20260814230058.png]]
- 
## **Questions to lookup**
1. What is the reload argument?
2. Do we need the uvicorn all the time?
3. Do we have to configure the response for all the http response codes?
4. For each execution, how do we create a jobid? When we are calling different functions and tool calls, how do we create a separate trace for each of those?
5. Can we use async.gather and along with yield?
6. Can we pass a body only with a POST endpoint? What is the best approach?
7. What is the protocol called **QUERY**? It is supposed to be a combination of GET and POST