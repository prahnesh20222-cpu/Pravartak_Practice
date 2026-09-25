---
document_id: document_ingestion_PII_Awareness
source_file:
source_type: class_notes
session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-09-12
Additional_session_date: 2026-09-13
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
topics: precision, recall, task success rate, groundedness success rate, retrieval hitrate, qdrant, chromadb
---
## RAG evaluation pipeline
- Docs --> Load --> Chunk --> Encoding --> Vector store --> Query embedding and Retrieval +/- Reranker --> Query and Chunks sent to LLM --> User response
- Two components of the evaluation are completeness and correctness. 
	- What affect completeness? Retriever performance mainly affects this
	- What affects correctness? Generator  i.e. LLM performance affects correctness
- Evaluation pipeline architecture( Refer [[https://github.com/vishnuap-ai-works/AIARAG-Capstone-Project/blob/main/EVALUATION_PIPELINE.md]])
	![[Pasted image 20260913081329.png|665]]
-  In the above diagram, we use the questions in the golden dataset to evaluate the RAG. Context in the above diagram refers to the **retrieved chunks**. Essentially, we are asking the LLM to generate a response to the query using the retrieved chunks as context. Normally provide the context as part of the query to get a more accurate response. In the case of RAG, we use the retrieved chunks to server the same purpose.
- Evaluation is based on three values
	- **Task success rate (TSR)**: Compare real answer and generated answer to see if there is semantntic match. It also is based on if all the required details are there or not, i.e. completeness
		- **If Task Success Rate is low (but Retrieval is high)**: The right info was retrieved, but the model gave a bad answer. 
		- **Lower LLM Temperature**: Ensure the model generation isn't too creative by setting temperature closer to 0.0.
		- **Change Generator LLM**: Switch to a more capable reasoning model.
		- **Prompt Engineering**: The generator might need step-by-step instructions (Chain of Thought) to synthesize complex context into the final answer.
	- **Groundedness**: Compares generated answer with retrieved chunks. This will check and evaluate the presence of hallucination
		- If Groundedness is low (P**recision is suffering**): The model is hallucinating or ignoring the context.
		- Adjust Generator Prompt: Make the prompt stricter in src/rag/prompts/prompts.py (e.g., "Answer ONLY using the context. If you don't know, say 'I don't know'.").
		- Change Generator LLM: Switch LLM_SOURCE or OPENAI_LLM_MODEL to a smarter model (e.g., gpt-4o) that follows instructions better.
	- **Retrieval hit rate** will tell us how the retriever is performing. It compares real answer with the retrieved chunks
		- If Retrieval Hit Rate (**Recall**) is low: The system isn't finding the right documents.
		- **Increase TOP_K**: Retrieve more documents to increase the surface area of potential hits.
		- **Adjust Chunking**: If chunks are too small, context is lost. If they are too large, the embeddings get diluted. Adjust CHUNK_SIZE and CHUNK_OVERLAP.
		- **Change Embedding Model**: Switch OPENAI_API_EMBEDDING_MODEL to a more capable model (e.g., from text-embedding-3-small to text-embedding-3-large).
		- **Use a Reranker**: Implement a cross-encoder to re-rank the TOP_K results for better relevancy.
- The prompt used by generator and prompt used by LLM judge are different and must be carefully be created.
- How can we improve groundedness?
	- Prompt improvement
	- Check how other models are performing in this context
	- LLM parameters like temperature
-  In example shown in the session, groundedness and retrieval hit rate had a score of 1. However, the task success rate has a score of 0.8. 
  ```
  {
        "id": "g050",
        "question": "Does 37signals provide a matching contribution if I purchase pet insurance through Figo?",
        "ideal_answer": "No, the company only offers access to a 10% discount and does not administer or contribute financially toward the policy.",
        "generated_answer": "I don't know based on the provided context. The information given does not mention any matching contribution from 37signals for pet insurance purchased through Figo. According to the context, 37signals offers pet insurance at a 10% discount but does not administer or contribute towards the policy.",
        "level": "edge_path",
        "latency": 26.50858497619629,
        "cost": 0.0,
        "task_success": 0.8,
        "groundedness": 1.0,
        "retrieval_hit": 1.0
    }
  
  ```
  When we look at the contents, the response is semantically correct, but bit more verbose. To me this is incorrect. When I prompted chatgpt to review this observation, it responded that 0.8 could be a result of **hedging**.  Hedging means using language that makes a statement less definite or confident. In this example, even tough it provided the accurate answer, the score could have been lower because of the element of  uncertainty in the answer. refer [[https://github.com/vishnuap-ai-works/AIARAG-Capstone-Project/blob/main/data/evals/all_results.json]]
- ChatGPT provides two prompt examples that we can refer to **reduce hedging**
```
A simple instruction works well:

> **“Be direct and minimize hedging. When the available evidence supports a conclusion, state it confidently and directly. Don't use unnecessary phrases such as ‘it seems,’ ‘it appears,’ ‘I think,’ ‘possibly,’ or ‘I don't know’ when you actually have sufficient evidence. When evidence is genuinely insufficient or ambiguous, explicitly say so.”**

For an **LLM/RAG application**, I'd make it slightly more precise:

> **“Answer directly using the provided context. Avoid unnecessary hedging or expressions of uncertainty when the context supports the answer. Distinguish between genuine uncertainty and stylistic hedging: acknowledge uncertainty only when the evidence is insufficient, conflicting, or ambiguous. Do not begin with disclaimers such as ‘I don't know’ if the context supports a substantive answer.”**

That last distinction is important.

You **don't** want:

> “Never hedge.”

because that can produce overconfident hallucinations.

You want:

> **“Be as certain as the evidence warrants.”**
```

### Implementation walk through of LLM as judge for RAG
- The code demoed in the session can be found in [[https://github.com/vishnuap-ai-works/AIARAG-Capstone-Project/blob/main/scripts/run_rag_eval.py]]
- The main function does the following
	- The function first loads gelden_set.jsonl
	- it loads the configured threshold. The thresholds.json file contains the following
	```
	{
  "task_success_rate": { "acceptable": 0.60, "good": 0.80 },
  "groundedness": { "acceptable": 0.80, "good": 0.95 },
  "retrieval_rate": { "acceptable": 0.70, "good": 0.90 },
  "cost_per_query": { "acceptable": 0.01, "good": 0.005 },
  "latency_p95": { "acceptable": 3.0, "good": 1.5 }
}
	```
- it also creates the path for the report.md file that will be created as output
- The inferencePipeline object is created. This object has all the functionalities for retrieval
- An object of the LLMjudge is also created
- The run evaluation module consumes golden dataset and inference pipeline.
- For every item in the golden dataset, a response is generated and then it is sent to the LLM judge
- The final metrics will provide TSR, GSR, RHR etc

## ChromaDB
- Chroma is designed to make a vector database **very easy to embed into an application**
- It supports the following implementation model
```
Python application
       │
       ▼
   ChromaDB
       │
       ▼
local persistent storage
```
- We can install the Python package and use Chroma directly from our application. We don't necessarily need to set up a separate database server. That's very similar to the convenience of SQLite
- **Overview**: Chroma is an open-source, AI-native embedding database focused entirely on developer productivity and building LLM apps quickly. It's the default vector store in many LangChain and LlamaIndex tutorials.

- **ANN Support**: HNSW (via hnswlib).
- **Architecture**: Local embedded database (runs in-memory or persists to local disk) or simple client-server mode.
- **Pros**:
    - Incredibly easy to get started (runs in your Python process).
    - Zero configuration required for local development.
    - Automatically handles embedding models (defaults to sentence-transformers).
- **Cons**:
    - Not designed for massive, multi-node distributed scale (though they are working on a distributed cloud version).
    - Fewer advanced features compared to Milvus or Qdrant.
- **When to Use**: You are building prototypes, doing local development, or building small to medium applications where simplicity and speed of development are the highest priorities.

### Hybrid search
- Similarity search is also called as **dense search**
- The other kind of search operation is called **sparse or keyword search**
- Hybrid search combines the two
## Vector database session continued on Sep 13, 2026
### Integrate Qdrant
- Download and install if needed from https://qdrant.tech/documentation/installation/
- It is preferable to handle installations from docker instead of maintaining a standalone db component
- Qdrant cloud is also available similar to RDS in cloud platforms
- For dev work that we do, we will use a local installation as a part of a docker container package
	- docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v $(pwd)/data/db/qdrant_storage:/qdrant/storage qdrant/qdrant
- **NOTE** env variables if they are processed as strings by the app, can be entered without any quotes. however **if there are whitespaces in them, wrap in single quotes**
### Improvement of retrieval
- This can involve the following
	- Embedding method/mode
	- chunking size and method
	- reranker
-  There are approaches of retrieval that can be optimized
	- Dense retrieval: This uses semantic matching
	- Sparse retrieval: Use keywords
	- Hybrid retrieval: This uses both dense and sparse
- We can also employ **multi querying**
	- It is a mechanism where user query is routed to an LLM and it makes different versions of the question. These questions are then sent to RAG. This is costly, but has specific use cases
		- The versions of a question can be the following
			- q1: how do we improve latency?
			- q2: how to improve RAG latency?
			- q3: How can I optimize RAG response time
		- These can have significant impact on the hard and edge case scenarios
	- We can make this functionality a role based feature. Not all users should need this. Is this something an agent can orchestrate?
- **Query decomposition**
	- We are splitting the question into smaller parts
		- E.g. if the question is "What was my profit margin in 2024 compared to 2023 and how is my employee count improved from 2023 to 2024"
			- This is a complex prompt. Retriever has to access multiple docs and this could lead to incomplete response
			- We use an LLM to dissect the user query into "What is the profit in 2023?", "What is the profit in 2024?",  "What is the employee count IN 2024?" and What is the employee count IN 2023?
			- Then we will iterate through all 4 parts and the response will be built using the context provided by all 4 similarity searches to provide a complete response.
	- 
## Questions to look up
- Do we have to depend on LLM for checking groundedness? Can't we use an offline model like BERT or any transformer model to do that? do they scale well?
- Why do we need a higher model for a LLM as judge if we are providing all the instructions, including expected answer?
- Can a docker image be deployed using other containerization applications?
- The pointid we create in the vectordb can also be timestamp encoded. Are there use cases where this timestamp is relevant for the LLM response?
- Is it possible to flag a user query as suitable for decomposition before we even do similarity search? how do we  do that? Is that something an agent should do?
- 
-





- 

