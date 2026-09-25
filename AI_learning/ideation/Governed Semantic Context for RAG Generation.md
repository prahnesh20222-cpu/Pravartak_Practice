**Question 1**: How much does generation quality improve when an enterprise's governed semantic layer is explicitly supplied to the LLM, compared with a conventional RAG system that provides only retrieved textual evidence? 
 **Question 2**: Can the architecture be designed to be able to determine the authoritative knowledge source capable of answering the question, then use RAG/LLM only when necessary?
 
- **Add a query-understanding step before retrieval.**
    - Analyze the user query for semantic attributes such as **classification labels, intent, domain, topic, and entities**.
    - The output is not limited to glossary terms.
- **Use the classifications to look up governed context.**
    - Map identified labels to a **business glossary, taxonomy, ontology, or other governed metadata**.
    - Retrieve definitions, related concepts, business rules, or other relevant semantic context.
- **Keep this path separate from document retrieval.**
    - The glossary/taxonomy lookup is **not intended to improve BM25 or vector retrieval**.
    - Retrieval continues independently using the original query.
- **Combine the two outputs only at generation time.**
    - Give the LLM:
        1. The original question
        2. Retrieved evidence from the RAG pipeline
        3. Governed semantic context derived from the query classification
- **Purpose:** help the LLM **interpret and answer the question within the enterprise's governed terminology and conceptual framework**, rather than simply giving it more documents.
- **Potential extension:** the classification taxonomy itself can become a governed asset, with labels mapped to definitions, concepts, rules, authoritative sources, and relationships.
- Mental model:
```

                 QUERY
                   │
          ┌────────┴────────┐
          ↓                 ↓
   Query classification   Retrieval
          │                 │
          ↓                 ↓
 Governed semantic      Evidence
    context                 │
          │                 │
          └────────┬────────┘
                   ↓
                 LLM
```
   - The entity identification from the query will not always return only glossary terms. It is more likely to return **classification labels**.
   -  When integrated the generation context sent to LLM could look like this
   ```
Query:
Which customer records failed the quality checks in the last monthly load?

Query classifications:
- Domain: Customer Data
- Topic: Data Quality
- Intent: Data Quality Investigation

Governed context:
- Customer Data Quality
  Definition: ...
- Applicable quality rules: ...
- Relevant business terminology: ...

Retrieved evidence:
- ...
- ...
   ```
   - 