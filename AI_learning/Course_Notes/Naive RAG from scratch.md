---
document_id: naive-rag_scratch
source_file:
source_type: class_notes
session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-08-29
language: en
technical_depth: low_to_medium
rag_ready: false
chunking_strategy: topic_based_with_timestamp_provenance
speaker_names_preserved: false
transcript_cleaned: false
source: notes
additional_reading:
impl_example1:
imple_example2:
topics: RAG, embedding, chunking, long-context
additional_session_date: 2026-08-30
---
## Why does RAG matter
- Why do we need RAG?
- What are the available methods to get an answer for a question
	- **Long-context**: We will provide the entire document to the LLM. This does not scale up
	- **RAG**: Chunks from a corpus are send to LLM.  
		- One advantage of RAG is that it brings down the number of tokens we are sending in each API call by selecting relevant sections of the document?
		- Even when we use RAG, if we use a public LLM, it sees our data from the retrieved chunks. Correct? how does it improve privacy?
	- **Finetune**: We can finetune the LLM on our data. This is rare and not affordable for most. 

## Advantages and Disadvantages of RAG
### Without RAG
- Without RAG, the LLMs only know what it learnt at the training phase. It's knowledge is frozen at the training cut-off date
- No access to specific proprietary  documents
- LLMs will tend to hallucinate when no info is available. This is easy to overlook.
- Can't cite sources. So, info will be unverifiable
- Long-context prompting approach will not scale properly
- There is no guarantee that all users will use the correct version of a document when they use long-context prompting
- RBAC cannot be ensured
### With RAG
- LLM reads chunks of proprietary docs at query time
- Knowledge is limited by the corpus and not training dataset that the LLM was built on
- Reads the proprietary docs directly
- We can build the citation as a part of the response. So, we can verify what LLM returns
- **RAG is best** when knowledge updates faster than we can retrain, and context is too big to fit in one prompt. **Isn't this always the case**?
- We bring the size of token window consumed by sending only relevant chunks. This can bring down hallucination. However, if retrieval is poor, it can hallucinate.  We are essentially sending a prompt to LLM and providing some document chunks to go with the prompt. If the chunks are bad, then RAG will also hallucinate
- The easier RAG becomes to implement and maintain, usability of unstructured data will go up. We will start finding new use cases
### when is RAG not needed?
- Small, stable corpus: Product manual under 50 pages . stable FAQ . documentation that changes quarterly. Long-context is better
- Style or skill transfer: Brand voice . domain-specific reasoning . code generation in your stack's idiom. Fine-tuning teaches the model a behavior. RAG can't change how the model thinks. Finetuning is impractical
- Structured, exact-match data: Order status . account balance . when does my flight depart. That's a database query, not a similarity search. Use SQL, return the row, format the answer. WE can provide the DB as a tool to an agent.
## RAG anatomy
- Two sections in the RAG architecture
	- **Document upload or Indexing**
		- Admin/Developer will handle this part. They will use the upload endpoint and upload the documents that will be part of the RAG
		- The first step of document upload is **chunking**. Chunking will break a big document into small chunks. There are different methods to chunk
			- Fixed length chunk, topic or paragraph based chunk 
		- The second stage is **embedding**. This process converts a text into multidimensional vectors. There are different embedding models and they will determine the embedding size
			- every embedding model is deterministic. Same document will return the same vector every time we pass it to a model
			- higher embedding models will improve retrieval
			- higher-models will increase cost and hurt performance
			- ensure embedding models support multi-language content if corpus includes that.
		- The chunks( actual fragments of text) and embedding will be stored in the vector database
	- **Querying/Interacting**
		- The end-user is exposed only to this part of the architecture. They ask a question.
		- The question will also be embedded using the **same** embedding model used for chunk embedding. We will not be typically doing chunking in this step
		- The app will perform a **similarity search** using the user question vector and find matching chunks from the vector DB. This can use cosine similarity, manhattan distance etc.
		- The response will be **top5** (or whatever we choose) chunks that are similar to the question. 
		- The chunks will be processed through **reranking** (based on configured parameters)
		- The re-ranked chunks will be sent to the LLM. It uses the system prompt, user prompt (question) and these chunks.
## Pipeline
![[Pasted image 20260829130318.png]]

![[Pasted image 20260829130435.png]]

## Chunking
- Chunking is needed because embedding models can have size limits. This breaks up the doc into manageable size
- This also helps in retrieve the relevant *part* of a doc, not the whole doc.. This brings down token consumption
	- Sliding window
		- There will be overlap between the chunked strings. This will help LLM to understand that to retrieved chunks actually belong together.. This will improve the quality of the response. The chunk size and overlap size will be configured in the code that chunks.
		- The overlap can also impact the reranking step of retrieval.
		- Sliding window of 500 chars with 50 char overlap is a good place to start. Recommended for capstone.
		- This is a generic approach that is a good place to start when we don't understand the document.
	- By sentence
		- Based on clean boundaries. We can configure it to chunk sentences or paragraphs
	- By section
		- Based on sections and subsections
	- Semantic
		- This is expensive.
		- An LLM model can identify different topics in a big document and we can chunk based on LLM provided boundaries.
	- 
### Points of failure
- Chunk can break mid-sentence or mid-section and context may be lost
- Chunk too small
- Chunk too big
- No overlap: overlap is boundary is poorly defined

## Embedding
- Recommended to use **OpenAI.text-embedding-3-small**
- For local implementation use **sentence-transformers.all-MiniLM-L6-v2**
- An example of a sentence embedding with a 1536 dimension vector will look like this array [0.012, -0.84, 0.31..., 0.07]
### Points of failure
- Chosen model is trained on a different domain
- Vectors are not normalized. When this is missed, cosine similarity can throw exceptions. Open source models can have this problem

## Vector store
- Example
	```
	store =
	"chunk" "Employees get 20 days ...
	"embedding"
	[0.012, -0.84, ... ], # 1536 dims
	"source" "leave_policy.md"
	"chunk" "Reimbursements over $50 ...
	"embedding" [-0.21, 0.55, ... ],
	"source" "expense_policy.md"
	# ... one entry per chunk x all documents
	```
- Pipeline : Chunking--> Embedding-->storing in vector DB
-  Basic example of a document uploader code template
- ![[Pasted image 20260830112702.png]]
-  ### **Overview of the Code Block Architecture** as explained by Gemin
	- The template demonstrates a standard Object-Oriented Design Pattern for creating non-blocking file loaders:
	- **`BaseDocumentLoader(ABC)`**: An Abstract Base Class defining a strict interface/contract using the `@abstractmethod` decorator. It dictates that any concrete loader class (like `TextLoader`, `PdfLoader`, `CsvLoader`) must implement an `async def load(self, path: str) -> str` method.   
	- **`TextLoader(BaseDocumentLoader)`**: A concrete class inheriting from the abstract loader to read plain text files.
    - **The Asynchronous Strategy**: Python's standard file operations (`open().read()`) are **synchronous and blocking**. If a large file is read directly in an async function, it locks Python's execution thread and halts the entire event loop. To prevent this, the code uses `loop.run_in_executor(None, _read_file)` to offload the synchronous disk read to a background `ThreadPoolExecutor`, returning an awaitable Future.
    - **If this is part of a file in `src` and I import it into `main.py`, won't this abstract code block throw an exception?**
		**No, importing this module into `main.py` will NOT throw an exception.** **Class Definitions Do Not Trigger Abstract Errors:** Simply importing a module that contains an Abstract Base Class (`ABC`) or `@abstractmethod` definition loads the class definition into memory without instantiating it.
    - **When Would It Throw an Error?**
        - You **cannot** instantiate an abstract class directly (e.g., `loader = BaseDocumentLoader()` will raise a `TypeError: Can't instantiate abstract class BaseDocumentLoader with abstract method load`).
	    - If a subclass inherits from `BaseDocumentLoader` but **fails to implement** the `@abstractmethod async def load()`, attempting to instantiate that subclass will raise a `TypeError`.
        - Because `TextLoader` explicitly overrides and implements `load()`, both `from src.loaders import TextLoader` and `loader = TextLoader()` will run completely error-free in `main.py`. 
- **Can't we just call `with open()` directly inside an `async` function?**
**Yes, you _can_ write `with open()` inside an `async def` function without syntax errors, but doing so creates an async anti-pattern.**
- **Why it's problematic:** Standard Python `with open(...)` is completely synchronous and blocking. Marking a function with `async def` does **not** automatically make internal synchronous calls asynchronous. If `open().read()` takes 2 seconds to read a large file from disk, the entire Python process—including all concurrent FastAPI requests, background tasks, or `asyncio.gather` loops—will freeze for those 2 seconds.    
- **When direct `with open()` is acceptable:** If you are reading small files (e.g., tiny `.txt` or `.json` config files under a few kilobytes), disk I/O latency is near zero and direct `with open()` is practically harmless.    
- **When to use the background executor pattern (`run_in_executor`):** When handling large files, high-throughput web applications (like FastAPI), or slow network/disk drives. Offloading to `run_in_executor` keeps the event loop free to serve other tasks concurrently while the file reads in the background.
- **Note** the file load does not always need to be **async** . It can be batch process that runs on schedule. Such a pipeline can be synchronous
- 
## Retrieval
- Pipeline to perform retrieval -->polishing -->send to user

## Questions to look up
- If we upload a document to ChatGPT, it will answer the question. When we send a follow up question, it has to send the entire history again. This will consume additional tokens. RAG will have the same problem?
- Hallucination is still a problem with RAG. correct? Compare fine tuning, long-context and RAG in the context of hallucination
- Slide says :Fine-tuning Stable style or skill. ~$5-50 of training data, lasts months. What does this mean?
- Are embedding models also using LLM underneath?
- How are we ensuring RBAC in RAG systems? This is the challenging . This can be handled at chunk level or document level metadata
- There are some document pre-processing that must be done before chunking. Can that be made an automated pipeline?
- Does vector embedding require data modelling? how can we leverage the metadata to build relationships?  Vishnu says the requirement is less. Does that mean we have to build different databases for each use case? what if they are related?
- When pdf contains images, or if pdf is created from scanned images, then the approach to embed them is different. We must use OCR approaches
- ### What are other other RAG types
	- Graph RAG: Vector DB is replaced by Graph DB?
	- Hybrid RAG: 
	- Agentic RAG
- What is a **staticmethod**? Usage is **@staticmethod**. Do we not need an empty class object to instantiate it?
- Around 1 hr 58 min, Vishnu describes briefly how metadata is loaded along with chunking. Rewatch that
- 
