---
document_id: Async_FastAPI_Testing_Intro
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
additional_reading: "[Async_dan_realpython](<Personal_Reading/Async_dan_realpython.pdf>)"
impl_example1: '[Async_examples](<"C:\Users\prahn\OneDrive\Documents\IITM-Pravartak\Pravartak_Practice\practice_scripts\async_learning.ipynb">)'
imple_example2:
---
# Asynchronous flow

- When multiple users are querying a database concurrently, all these requests can get accumulated. At some point, this could block transactions from some users until the pending tasks are completed. This situation is overcome by the use of an asynchronous logic.
- In asynchronous mode, every time a a function - it must be defined a specific way to mark it as a async function - it will be defined as a coroutine. There is an engine called "event loop" that handles these coroutines
- The event loop will process a request and goes into waiting mode but keeps tracking the requests without blocking new requests
- This type of logic is useful when there are multiple simultaneous calls to a function or external component that can potentially be blocked or is inefficient when executed sequentially.
-  This is not multi-threading. It is an algorithmic way of handling concurrency
- This is implemented using the python library named **asyncio**
- The  key methods of this library that are most commonly used are 
	- **async**: This keyword identifies a function as asynchronous
	- **await**: Calling the function in the usual manner will not print output.it will return a coroutine object instead. This keyword is used to return the output of an asynchronous function when an event loop is already running. This is relevant when running the code jupyter notebook or vscode IDE. This will note work when executing the script from cmd. Failure example shown below. This code will throw an erorr **SyntaxError: 'await' outside function**
		- ```
			async def hello():
				print("helo world")
			await hello()
		  ```
		- This error is handled by making the following changes as show below.
		```
		async def hello():

		    print("hello world")

		import asyncio
		asyncio.run(hello())
		```
		- When one async function is called from inside another async function, then await is **always** used. When calling an async function in general, we need **asycnio.run()**	  
		- There are some libraries like FastAPI that have their own event loop. So in those cases, **asyncio.run() may not be needed**.
	- **asyncio.gather()**: This will help in parallel processing
		- Used for parallel processing
		- Gather is used to pull outputs from two different processes
		- ```
		import asyncio
		async def hello():
		    print("hello world")
		async def howdy():
		    print("howdy")
		async def fine():
		    print("I'm fine!")
		await asyncio.gather(hello(), howdy(), fine()) # This will print "hello world", "howdy", and "I'm fine!" in any order
		**Output:**
		hello world 
		howdy
		I'm fine!
		[None, None, None] 
		**Note**: It returns this list with None because the three functions are not returning any value. They are simple print statements. If they do, those values will populate the list.
			
				
		  ```
	- **ascyncio.sleep()**: This is a way to introduce an intentional time delay
		- ```
	async def hello():
	    await asyncio.sleep(5)
	    print("hello world")
	async def howdy():
	    await asyncio.sleep(2)
	    print("howdy")
	async def fine():
	    await asyncio.sleep(1)
	    print("I'm fine!") 
	await asyncio.gather(hello(), howdy(), fine())
	 **NOTE** This will print "hello world", "howdy", and "I'm fine!" in reverse order because of how long each function is taking to finish due to sleep time. This shows that the print happens as and when each function finishes.	 
	 If they are returning a value, then the list will be completed only when all three functions have compelted. Is there an YIELD method in this?
		  ```
	- **asyncio.create_task()**: This is used when we want to create a background task and there is no requirement to wait for the response. 
		- ```
		  async def send_data_db():
			   print("Sending data to db is initiated..")
			   await asyncio.sleep(10)
			   print("Data sent to db succesfully..")
		async def my_workflow():
		    print("Processing the data..")
		    task = asyncio.create_task(send_data_db())
		    print("continue with rest of the workflow..")
		    await asyncio.sleep(3)
		    print("Data processing is completed..")
		await my_workflow()
		**OUTPUT**
		Processing the data.. 
		continue with rest of the workflow..
		Sending data to db is initiated..
		Data processing is completed..
		Data sent to db succesfully..
		**NOTE**: "Data sent to db succesfully.." is not printed. We are executing the my_workflow function. It creates the task which runs in the background. This function continues without waiting for the create task to complete. This approach is useful for for activities like logging,adding the keys to redis cache etc.	
		
		  ```
- There are some differences between how we use the async function in a .py file vs a jupyter notebook. The table below highlights the difference between how a async function **hello()** is called. 
- | Aspect | Jupyter Notebook / IPython | Normal `.py` Script |
|---|---|---|
| Execution | Code can be executed cell by cell | Normally the script is executed as a whole |
| Event loop | An event loop is already running | No event loop is normally running initially |
| Top-level `await` | `await hello()` works directly | `await hello()` at top level gives `SyntaxError` |
| Running async code | `await hello()` | `asyncio.run(hello())` |
| Inside `async def` | `await hello()` | `await hello()` |
| Interactive experimentation | Very convenient; variables and state persist between cells | State generally exists only during the script execution |
| Re-running code | Individual cells can be rerun | Usually rerun the script or selected code through an IDE |
| Typical use | Exploration, learning, data analysis, experimentation | Applications, pipelines, production code, automation |
| Example | `await hello()` | `asyncio.run(hello())` |