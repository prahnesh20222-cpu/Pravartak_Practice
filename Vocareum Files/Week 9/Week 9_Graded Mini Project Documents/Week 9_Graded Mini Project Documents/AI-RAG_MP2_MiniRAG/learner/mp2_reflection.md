## What worked
Instead of a sliding window chunking method, I used a section aware chunking method. I also ensured that chunks did not break mid-paragraph. This chunking method worked. The evaluation tests helped identify a defect in the chunking code which created "section-title only" chunks which contained no useful text. This has been fixed. This was a good practice for the chunking strategy evaluation for capstone.

## What didn't work
The retrieval consistently found the relevant stories in all the queries. However, the retrieval window of k=3 was narrow for the hard questions. It wasn't always finding the specific chunks needed to answer the question completely. In one case, the LLM supplied information even though the retrieved excerpts did not contain those facts. It even said they were "not mentioned in the excerpts but generally known. When the window was increased to 4, all the chunks containg the relevant facts were retrieved for the two predefined questions.

## What I'd change
I will introduce a larger window while monitoring the token consumption. I'd attempt a reranker after validating the improvement in retrieval.

## One surprise

1. The answer-bearing chunk for the Speckled Band question ranked fourth (similarity 0.478), below three semantically related but insufficient chunks. Increasing k from 3 to 4 brought the required evidence into context. This highlighted that semantic similarity does not necessarily correspond to answer-bearing relevance. 
2. I was surprised at how for such a small corpus, the LLMs showed lack of deterministic or grounded response. I repeated the same query three times and it produced noticeably different answers even though the retrieved chunks were identical. There were also facts produced that were not grounded.