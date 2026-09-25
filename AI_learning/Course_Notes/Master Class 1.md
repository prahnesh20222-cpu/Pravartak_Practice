---
document_id: master_class_1
source_file:
source_type: class_notes
session_type: live_session
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date: 2026-09-11
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
topics:
additional_session_date: 2026-08-30
---
## Text Embedding
- Scalar is only a value
- Vector is a group of scalar values that has direction. They can describe anything
- Vectors a are good way to represent unstructured data in a structured format
- Let's say we have a vector [1, 1, 15, 21.] representing one person in a database
	- Each of these values represent a characteristic
- Vector embedding is basically a multi-dimensional encoded representation of a word or sentence
- Embedding = Numeric representation of objects (words, sentences, documents) in high-dimensional space.
	. Converts text -> numbers so machines can understand
	· Preserves semantic meaning
	. Similar objects -> close vectors
- Example:
	- "King" -> [0.21, -0.34, 0.85, ... ]
	- "Queen" -> [0.19, -0.32, 0.82, ... ]
	- We train the model to ensure **Distance between "King" & "Queen" is small**
- LLMs have something called **vocabulary**
- If we take a word, we can't chunk it into meaningless tokens. The semantic meaning has to be preserved.
-![[Pasted image 20260911192701.png]]
-  What does high dimensions achieve?
	- captures subtle differences between objects
	-  each dimension can encode different features or attributes
	- trade-off is  storage and compute cost
- high-dimensional vector spaces allow more precise similarity and clustering

### Text Representation
- A text is represented as a sequence of tokens.
![[Pasted image 20260911194002.png]]
- The vocabulary is the unique set tokens that the LLM  can represent
- The vocabulary is the complete set of unique tokens that the model can represent.
	V = {v1,02, ... ,vv]}
	where:
		|V| = Vocabulary Size

	Example: For a small vocabulary:
		V = {cat, dog, car, tree}

	Therefore:
		|V|=4
	Each token is assigned an index in the vocabulary:
		cat -> 1
		dog -> 2
		car ->3
		tree -> 4
### One-hot representation
- ![[Pasted image 20260911194658.png]]
-  When the corpus becomes big, this approach does not scale and it can become a sparse matric
-  Advantage is that this allows calculation of euclidean distance
### Dense vector representation
![[Pasted image 20260911194920.png]]
- 

### Text embedding
- An embedding model maps a token, or a complete text into a fixed-dimensional numeric vector
- ![[Pasted image 20260911195117.png]]
- ![[Pasted image 20260911195236.png]]
### What is vector space?
- Vector space is a mathematical space where vectors represent objects
	- Each point/vector =  a workd
![[Pasted image 20260911195359.png]]

### Distance between two vectors

- euclidean distance more popular than manhattan distance
- Cosine similarity is another way to represent this
- 
### Semantic similarity in vector space
- Cosine similarity will rank semantic similarity in the scale of 0 to 1
- The embedding model converts linguistic meaning into geometric relationships allowing mathematical operations such as cosine similarity to estimate semantic relatedness
- This is the fundamental idea behind semantic search, document retrieval , and RAG
### Embedding matric
- Large text embeddings are persisted as an embedding matrix
- ![[Pasted image 20260911201025.png]]

### How did NLP tools handle this?
- ![[Pasted image 20260911201155.png]]
- TF-IDF did not capture semantic context
- WORD2VEC captures semantic similarity in some form
- Transformer-based embedding models are the best in this area
	- BERT is a transformer encoder-based model
- 
## Questions to look up
- transformer: Self-Attention and positional encoding helps to manage this. What does this mean?
- Do we worry about correlation between dimensions in this context of vector embedding? is that a good or bad thing?
- Is it possible to look at the vocabulary of any LLM?
- If two models are structured a similar way, and if they use the same embedding model, we can use the embedding of the first and add on top of it to create a new
-