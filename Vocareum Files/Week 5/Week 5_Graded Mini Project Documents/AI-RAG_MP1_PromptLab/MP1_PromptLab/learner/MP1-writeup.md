

1. Which strategy won, and on what dimension? (Accuracy?  
Parse rate? Cost?)

- All the strategies achieved a 100% parse rate. Given the limited data set, there were no scenarios this failed. For this assignment, parse rate is not a useful criteria for analysis.   
- As expected from a simple dataset, all strategies performed comparably on accuracy which is a deterministic metric in this exercise. Upon manual verification of instances of failure, the following were observed.
	- Extraction of company name is easy for all these strategies. Compared to zeroshot, the other methods did not provide any significant improvement. All the prompts performed equally well on semantics. The errors were related to punctuation and whitespaces. When the code is executed multiple times, I noticed that COT prompt that had zero errors on extracting company name, failed twice by including punctuations. While semantically this is not an error, the deterministic accuracy metric chosen for this assignment marks it as failure
	- All the strategies failed to extract the experience field in j05. None of the strategies were able to understand that  "Fresh grads welcome — no prior experience required" equals zero years of experience.
- As expected zeroshot performed best on cost and latency
- It is worth noting that LLM judge was able to infer that the failures in "company" name extraction were of semantic nature. As a result, all strategies performed the same.
- Considering the sample size, the marginal improvements in accuracy, cost, fewshot seems to perform better. It is quite possible that the results reflect the nature of the examples used. The differences are marginal, and the results could easily change with a different corpus, task, or set of few-shot examples.
    

2. What surprised you? Either a strategy worked better than  
expected, or worse, or a specific snippet failed in a way  
you didn't predict.

The following observations surprised me.
- LLMs have matured significantly that simple tasks don't require elaborate prompting strategies. The gains are marginal.
- Fewshot strategy appeared more consistent. it was able to handle punctuations and whitespaces better than the other most likely due to the nature of examples provided ion the prompt.
- COT strategy's strength is the reasoning step. This does not guarantee correct extraction. This is exemplified by the fact that it could not process the experience required field in j05. I did not expect it to respond differently on some simple tasks when executed multiple times.
- 

3. For *your* capstone domain, which strategy would you reach  
for first? Justify in 2-3 sentences.
Based on this exercise, I'd start with fewshot strategy. I don't think a one size-fits-all strategy is a good idea. I am hoping to learn how we can dynamically choose them based on user query and past experience

4. If you had another day, what would you try next? (Different  
model? More snippets? Different prompts?)
I'd try different corpus
	1. Text that contains entities from different languages, something that is common in real conversations. 
	2. Technical documents like a requirement document for a data problems.  Something like a requirement for a small data processing/transformation job
**
**