---
document_id: basics_of_prompting
source_file:
source_type: webpage
source_url: https://www.promptingguide.ai/introduction/basics
session_type:
course: Advanced Certificate Programme in Agentic AI and RAG Engineering
session_date:
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
topics: prompt
retrieved_at: 2026-09-04

---
## Prompting an LLM[](https://www.promptingguide.ai/introduction/basics#prompting-an-llm)

You can achieve a lot with simple prompts, but the quality of results depends on how much information you provide it and how well-crafted the prompt is. A prompt can contain information like the _instruction_ or _question_ you are passing to the model and include other details such as _context_, _inputs_, or _examples_. You can use these elements to instruct the model more effectively to improve the quality of results.

Let's get started by going over a basic example of a simple prompt:

_Prompt_

```
The sky is
```

_Output:_

```
blue.
```

If you are using the OpenAI Playground or any other LLM playground, you can prompt the model as shown in the following screenshot:

![INTRO1](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fsky.b60b009f.png&w=2048&q=75)

Something to note is that when using the OpenAI chat models like `gpt-3.5-turbo` or `gpt-4`, you can structure your prompt using three different roles: `system`, `user`, and `assistant`. The system message is not required but helps to set the overall behavior of the assistant. The example above only includes a user message which you can use to directly prompt the model. For simplicity, all of the examples, except when it's explicitly mentioned, will use only the `user` message to prompt the `gpt-3.5-turbo` model. The `assistant` message in the example above corresponds to the model response. You can also define an assistant message to pass examples of the desired behavior you want. You can learn more about working with chat models [here](https://www.promptingguide.ai/models/chatgpt).

You can observe from the prompt example above that the language model responds with a sequence of tokens that make sense given the context `"The sky is"`. The output might be unexpected or far from the task you want to accomplish. In fact, this basic example highlights the necessity to provide more context or instructions on what specifically you want to achieve with the system. This is what prompt engineering is all about.

Let's try to improve it a bit:

_Prompt:_

```
Complete the sentence: The sky is
```

_Output:_

```
blue during the day and dark at night.
```

Is that better? Well, with the prompt above you are instructing the model to complete the sentence so the result looks a lot better as it follows exactly what you told it to do ("complete the sentence"). This approach of designing effective prompts to instruct the model to perform a desired task is what's referred to as **prompt engineering** in this guide.

The example above is a basic illustration of what's possible with LLMs today. Today's LLMs are able to perform all kinds of advanced tasks that range from text summarization to mathematical reasoning to code generation.

## Prompt Formatting[](https://www.promptingguide.ai/introduction/basics#prompt-formatting)

You have tried a very simple prompt above. A standard prompt has the following format:

```
<Question>?
```

or

```
<Instruction>
```

You can format this into a question answering (QA) format, which is standard in a lot of QA datasets, as follows:

```
Q: <Question>?A: 
```

When prompting like the above, it's also referred to as _zero-shot prompting_, i.e., you are directly prompting the model for a response without any examples or demonstrations about the task you want it to achieve. Some large language models have the ability to perform zero-shot prompting but it depends on the complexity and knowledge of the task at hand and the tasks the model was trained to perform good on.

A concrete prompt example is as follows:

_Prompt_

```
Q: What is prompt engineering?
```

With some of the more recent models you can skip the "Q:" part as it is implied and understood by the model as a question answering task based on how the sequence is composed. In other words, the prompt could be simplified as follows:

_Prompt_

```
What is prompt engineering?
```

Given the standard format above, one popular and effective technique to prompting is referred to as _few-shot prompting_ where you provide exemplars (i.e., demonstrations). You can format few-shot prompts as follows:

```
<Question>?<Answer><Question>?<Answer><Question>?<Answer><Question>?
```

The QA format version would look like this:

```
Q: <Question>?A: <Answer>Q: <Question>?A: <Answer>Q: <Question>?A: <Answer>Q: <Question>?A:
```

Keep in mind that it's not required to use the QA format. The prompt format depends on the task at hand. For instance, you can perform a simple classification task and give exemplars that demonstrate the task as follows:

_Prompt:_

```
This is awesome! // PositiveThis is bad! // NegativeWow that movie was rad! // PositiveWhat a horrible show! //
```

_Output:_

```
Negative
```

Few-shot prompts enable in-context learning, which is the ability of language models to learn tasks given a few demonstrations. We discuss zero-shot prompting and few-shot prompting more extensively in upcoming sections.

# Elements of a Prompt

As we cover more and more examples and applications with prompt engineering, you will notice that certain elements make up a prompt.

A prompt contains any of the following elements:

**Instruction** - a specific task or instruction you want the model to perform

**Context** - external information or additional context that can steer the model to better responses

**Input Data** - the input or question that we are interested to find a response for

**Output Indicator** - the type or format of the output.
To demonstrate the prompt elements better, here is a simple prompt that aims to perform a text classification task:

_Prompt_

```
Classify the text into neutral, negative, or positiveText: I think the food was okay.Sentiment:
```

In the prompt example above, the instruction correspond to the classification task, "Classify the text into neutral, negative, or positive". The input data corresponds to the "I think the food was okay.' part, and the output indicator used is "Sentiment:". Note that this basic example doesn't use context but this can also be provided as part of the prompt. For instance, the context for this text classification prompt can be additional examples provided as part of the prompt to help the model better understand the task and steer the type of outputs that you expect.

You do not need all the four elements for a prompt and the format depends on the task at hand. We will touch on more concrete examples in upcoming guides.

# General Tips for Designing Prompts

Here are some tips to keep in mind while you are designing your prompts:

### Start Simple[](https://www.promptingguide.ai/introduction/tips#start-simple)

As you get started with designing prompts, you should keep in mind that it is really an iterative process that requires a lot of experimentation to get optimal results. Using a simple playground from OpenAI or Cohere is a good starting point.

You can start with simple prompts and keep adding more elements and context as you aim for better results. Iterating your prompt along the way is vital for this reason. As you read the guide, you will see many examples where specificity, simplicity, and conciseness will often give you better results.

When you have a big task that involves many different subtasks, you can try to break down the task into simpler subtasks and keep building up as you get better results. This avoids adding too much complexity to the prompt design process at the beginning.

### The Instruction[](https://www.promptingguide.ai/introduction/tips#the-instruction)

You can design effective prompts for various simple tasks by using commands to instruct the model what you want to achieve, such as "Write", "Classify", "Summarize", "Translate", "Order", etc.

Keep in mind that you also need to experiment a lot to see what works best. Try different instructions with different keywords, contexts, and data and see what works best for your particular use case and task. Usually, the more specific and relevant the context is to the task you are trying to perform, the better. We will touch on the importance of sampling and adding more context in the upcoming guides.

Others recommend that you place instructions at the beginning of the prompt. Another recommendation is to use some clear separator like "###" to separate the instruction and context.

For instance:

_Prompt:_

```
### Instruction ###Translate the text below to Spanish:Text: "hello!"
```

_Output:_

```
¡Hola!
```

### Specificity[](https://www.promptingguide.ai/introduction/tips#specificity)

Be very specific about the instruction and task you want the model to perform. The more descriptive and detailed the prompt is, the better the results. This is particularly important when you have a desired outcome or style of generation you are seeking. There aren't specific tokens or keywords that lead to better results. It's more important to have a good format and descriptive prompt. In fact, providing examples in the prompt is very effective to get desired output in specific formats.

When designing prompts, you should also keep in mind the length of the prompt as there are limitations regarding how long the prompt can be. Thinking about how specific and detailed you should be. Including too many unnecessary details is not necessarily a good approach. The details should be relevant and contribute to the task at hand. This is something you will need to experiment with a lot. We encourage a lot of experimentation and iteration to optimize prompts for your applications.

As an example, let's try a simple prompt to extract specific information from a piece of text.

_Prompt:_

```
Extract the name of places in the following text. Desired format:Place: <comma_separated_list_of_places>Input: "Although these developments are encouraging to researchers, much is still a mystery. “We often have a black box between the brain and the effect we see in the periphery,” says Henrique Veiga-Fernandes, a neuroimmunologist at the Champalimaud Centre for the Unknown in Lisbon. “If we want to use it in the therapeutic context, we actually need to understand the mechanism.“"
```

_Output:_

```
Place: Champalimaud Centre for the Unknown, Lisbon
```

Input text is obtained from [this Nature article](https://www.nature.com/articles/d41586-023-00509-z).

### Avoid Impreciseness[](https://www.promptingguide.ai/introduction/tips#avoid-impreciseness)

Given the tips above about being detailed and improving format, it's easy to fall into the trap of wanting to be too clever about prompts and potentially creating imprecise descriptions. It's often better to be specific and direct. The analogy here is very similar to effective communication -- the more direct, the more effective the message gets across.

For example, you might be interested in learning the concept of prompt engineering. You might try something like:

```
Explain the concept prompt engineering. Keep the explanation short, only a few sentences, and don't be too descriptive.
```

It's not clear from the prompt above how many sentences to use and what style. You might still somewhat get good responses with the above prompts but the better prompt would be one that is very specific, concise, and to the point. Something like:

```
Use 2-3 sentences to explain the concept of prompt engineering to a high school student.
```

### To do or not to do?[](https://www.promptingguide.ai/introduction/tips#to-do-or-not-to-do)

Another common tip when designing prompts is to avoid saying what not to do but say what to do instead. This encourages more specificity and focuses on the details that lead to good responses from the model.

Here is an example of a movie recommendation chatbot failing at exactly what I don't want it to do because of how I wrote the instruction -- focusing on what not to do.

_Prompt:_

```
The following is an agent that recommends movies to a customer. DO NOT ASK FOR INTERESTS. DO NOT ASK FOR PERSONAL INFORMATION.Customer: Please recommend a movie based on my interests.Agent: 
```

_Output:_

```
Sure, I can recommend a movie based on your interests. What kind of movie would you like to watch? Do you prefer action, comedy, romance, or something else?
```

Here is a better prompt:

_Prompt:_

```
The following is an agent that recommends movies to a customer. The agent is responsible to recommend a movie from the top global trending movies. It should refrain from asking users for their preferences and avoid asking for personal information. If the agent doesn't have a movie to recommend, it should respond "Sorry, couldn't find a movie to recommend today.".Customer: Please recommend a movie based on my interests.Agent:
```

_Output:_

```
Sorry, I don't have any information about your interests. However, here's a list of the top global trending movies right now: [list of movies]. I hope you find something you like!
```

Some of the examples above were adopted from the ["Best practices for prompt engineering with OpenAI API" article.](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)

# Examples of Prompts

The previous section introduced a basic example of how to prompt LLMs.

This section will provide more examples of how to use prompts to achieve different tasks and introduce key concepts along the way. Often, the best way to learn concepts is by going through examples. The few examples below illustrate how you can use well-crafted prompts to perform different types of tasks.

Topics:

- [Text Summarization](https://www.promptingguide.ai/introduction/examples#text-summarization)
- [Information Extraction](https://www.promptingguide.ai/introduction/examples#information-extraction)
- [Question Answering](https://www.promptingguide.ai/introduction/examples#question-answering)
- [Text Classification](https://www.promptingguide.ai/introduction/examples#text-classification)
- [Conversation](https://www.promptingguide.ai/introduction/examples#conversation)
- [Code Generation](https://www.promptingguide.ai/introduction/examples#code-generation)
- [Reasoning](https://www.promptingguide.ai/introduction/examples#reasoning)

---

## Text Summarization[](https://www.promptingguide.ai/introduction/examples#text-summarization)

One of the standard tasks in natural language generation is text summarization. Text summarization can include many different flavors and domains. In fact, one of the most promising applications of language models is the ability to summarize articles and concepts into quick and easy-to-read summaries. Let's try a basic summarization task using prompts.

Let's say you are interested to learn about antibiotics, you could try a prompt like this:

_Prompt:_

```
Explain antibioticsA:
```

_Output:_

```
Antibiotics are a type of medication used to treat bacterial infections. They work by either killing the bacteria or preventing them from reproducing, allowing the body’s immune system to fight off the infection. Antibiotics are usually taken orally in the form of pills, capsules, or liquid solutions, or sometimes administered intravenously. They are not effective against viral infections, and using them inappropriately can lead to antibiotic resistance.
```

The "A:" is an explicit prompt format that you use in question answering. You used it here to tell the model that there is an answer expected further. In this example, it's not clear how this is useful vs not using it but we will leave it that for later examples. Let's just assume that this is too much information and you want to summarize it further. In fact, you can instruct the model to summarize into one sentence like so:

_Prompt:_

```
Antibiotics are a type of medication used to treat bacterial infections. They work by either killing the bacteria or preventing them from reproducing, allowing the body’s immune system to fight off the infection. Antibiotics are usually taken orally in the form of pills, capsules, or liquid solutions, or sometimes administered intravenously. They are not effective against viral infections, and using them inappropriately can lead to antibiotic resistance.Explain the above in one sentence:
```

_Output:_

```
Antibiotics are medications used to treat bacterial infections by either killing the bacteria or stopping them from reproducing, but they are not effective against viruses and overuse can lead to antibiotic resistance.
```

Without paying too much attention to the accuracy of the output above, which is something we will touch on in a later guide, the model tried to summarize the paragraph in one sentence. You can get clever with the instructions but we will leave that for a later chapter. Feel free to pause here and experiment to see if you get better results.

---

## Information Extraction[](https://www.promptingguide.ai/introduction/examples#information-extraction)

While language models are trained to perform natural language generation and related tasks, it's also very capable of performing classification and a range of other natural language processing (NLP) tasks.

Here is an example of a prompt that extracts information from a given paragraph.

_Prompt:_

```
Author-contribution statements and acknowledgements in research papers should state clearly and specifically whether, and to what extent, the authors used AI technologies such as ChatGPT in the preparation of their manuscript and analysis. They should also indicate which LLMs were used. This will alert editors and reviewers to scrutinize manuscripts more carefully for potential biases, inaccuracies and improper source crediting. Likewise, scientific journals should be transparent about their use of LLMs, for example when selecting submitted manuscripts.Mention the large language model based product mentioned in the paragraph above:
```

_Output:_

```
The large language model based product mentioned in the paragraph above is ChatGPT.
```

There are many ways you can improve the results above, but this is already very useful.

By now it should be obvious that you can ask the model to perform different tasks by simply instructing it what to do. That's a powerful capability that AI product developers are already using to build powerful products and experiences.

Paragraph source: [ChatGPT: five priorities for research](https://www.nature.com/articles/d41586-023-00288-7)

---

## Question Answering[](https://www.promptingguide.ai/introduction/examples#question-answering)

One of the best ways to get the model to respond with specific answers is to improve the format of the prompt. As covered before, a prompt could combine instructions, context, input, and output indicators to get improved results. While these components are not required, it becomes a good practice as the more specific you are with instruction, the better results you will get. Below is an example of how this would look following a more structured prompt.

_Prompt:_

```
Answer the question based on the context below. Keep the answer short and concise. Respond "Unsure about answer" if not sure about the answer.Context: Teplizumab traces its roots to a New Jersey drug company called Ortho Pharmaceutical. There, scientists generated an early version of the antibody, dubbed OKT3. Originally sourced from mice, the molecule was able to bind to the surface of T cells and limit their cell-killing potential. In 1986, it was approved to help prevent organ rejection after kidney transplants, making it the first therapeutic antibody allowed for human use.Question: What was OKT3 originally sourced from?Answer:
```

_Output:_

```
Mice.
```

Context obtained from [Nature](https://www.nature.com/articles/d41586-023-00400-x).

---

## Text Classification[](https://www.promptingguide.ai/introduction/examples#text-classification)

So far, you have used simple instructions to perform a task. As a prompt engineer, you need to get better at providing better instructions. But that's not all! You will also find that for harder use cases, just providing instructions won't be enough. This is where you need to think more about the context and the different elements you can use in a prompt. Other elements you can provide are `input data` or `examples`.

Let's try to demonstrate this by providing an example of text classification.

_Prompt:_

```
Classify the text into neutral, negative or positive. Text: I think the food was okay. Sentiment:
```

_Output:_

```
Neutral
```

You gave the instruction to classify the text and the model responded with `'Neutral'`, which is correct. Nothing is wrong with this but let's say that what you really need is for the model to give the label in the exact format you want. So instead of `Neutral`, you want it to return `neutral`. How do you achieve this? There are different ways to do this. You care about specificity here, so the more information you can provide the prompt, the better results. You can try providing examples to specify the correct behavior. Let's try again:

_Prompt:_

```
Classify the text into neutral, negative or positive. Text: I think the vacation is okay.Sentiment: neutral Text: I think the food was okay. Sentiment:
```

_Output:_

```
neutral
```

Perfect! This time the model returned `neutral` which is the specific label you were looking for. It seems that the example provided in the prompt helped the model to be specific in its output.

To highlight why sometimes being specific is important, check out the example below and spot the problem:

_Prompt:_

```
Classify the text into nutral, negative or positive. Text: I think the vacation is okay.Sentiment:
```

_Output:_

```
Neutral
```

What is the problem here? As a hint, the made-up `nutral` label is completely ignored by the model. Instead, the model outputs `Neutral` as it has some bias towards that label. But let's assume that what you really want is `nutral`. How would you fix this? Maybe you can try adding descriptions to the labels or add more examples to the prompt? If you are not sure, we will discuss a few ideas in the upcoming sections.

---

## Conversation[](https://www.promptingguide.ai/introduction/examples#conversation)

Perhaps one of the more interesting things you can achieve with prompt engineering is instructing the LLM system on how to behave, its intent, and its identity. This is particularly useful when you are building conversational systems like customer service chatbots.

For instance, let's create a conversational system that's able to generate more technical and scientific responses to questions. Note how you are explicitly telling it how to behave through the instruction. This is sometimes referred to as _role prompting_.

_Prompt:_

```
The following is a conversation with an AI research assistant. The assistant tone is technical and scientific.Human: Hello, who are you?AI: Greeting! I am an AI research assistant. How can I help you today?Human: Can you tell me about the creation of blackholes?AI:
```

_Output:_

```
Sure! Black holes are regions of spacetime where the gravitational force is so strong that nothing, not even light, can escape from it. They are created when a very massive star dies and its core collapses in on itself, forming a singularity of infinite density. The intense gravity of the singularity pulls in all the matter and radiation around it, creating the black hole.
```

Our AI research assistant sounds a bit too technical, right? Okay, let's change this behavior and instruct the system to give more accessible answers.

_Prompt:_

```
The following is a conversation with an AI research assistant. The assistant answers should be easy to understand even by primary school students.Human: Hello, who are you?AI: Greeting! I am an AI research assistant. How can I help you today?Human: Can you tell me about the creation of black holes?AI: 
```

_Output:_

```
Sure! Black holes are created when a very massive star runs out of fuel and collapses in on itself. The gravity of the star is so strong that nothing, not even light, can escape its pull. This creates a point in space-time with an intense gravitational force called a black hole.
```

You made some progress. You can continue improving it. If you add more examples, you might get even better results.

---

## Code Generation[](https://www.promptingguide.ai/introduction/examples#code-generation)

One application where LLMs are quite effective is code generation. Copilot is a great example of this. There are a vast number of code-generation tasks you can perform with clever prompts. Let's look at a few examples below.

First, let's try a simple program that greets the user.

_Prompt:_

```
/*Ask the user for their name and say "Hello"*/
```

_Output:_

```
let name = prompt("What is your name?");console.log(`Hello, ${name}!`);
```

Notice that you didn't even need to specify the language to use.

Let's switch levels a bit. The example below shows how powerful LLMs can be with a little more effort in designing the prompts.

_Prompt:_

```
"""Table departments, columns = [DepartmentId, DepartmentName]Table students, columns = [DepartmentId, StudentId, StudentName]Create a MySQL query for all students in the Computer Science Department"""
```

_Output:_

```
SELECT StudentId, StudentName FROM students WHERE DepartmentId IN (SELECT DepartmentId FROM departments WHERE DepartmentName = 'Computer Science');
```

This is very impressive. In this case, you provided data about the database schema and asked it to generate a valid MySQL query.

---

## Reasoning[](https://www.promptingguide.ai/introduction/examples#reasoning)

Perhaps one of the most difficult tasks for an LLM today is one that requires some form of reasoning. Reasoning is one of most interesting areas due to the types of complex applications that can emerge from LLMs.

There have been some improvements in tasks involving mathematical capabilities. That said, it's important to note that current LLMs struggle to perform reasoning tasks so this requires even more advanced prompt engineering techniques. We will cover these advanced techniques in the next guide. For now, we will cover a few basic examples to show arithmetic capabilities.

_Prompt:_

```
What is 9,000 * 9,000?
```

_Output:_

```
81,000,000
```

Let's try something more difficult.

_Prompt:_

```
The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. A: 
```

_Output_

```
No, the odd numbers in this group add up to an odd number: 119.
```

That's incorrect! Let's try to improve this by improving the prompt.

_Prompt:_

```
The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. Solve by breaking the problem into steps. First, identify the odd numbers, add them, and indicate whether the result is odd or even. 
```

_Output:_

```
Odd numbers: 15, 5, 13, 7, 1Sum: 41 41 is an odd number.
```

Much better, right? By the way, we tried this task a couple of times and the model sometimes fails. If you provide better instructions combined with examples, it might help get more accurate results.

In the upcoming section, we will cover even more advanced prompt engineering concepts and techniques for improving performance on all these and more difficult tasks.

# Prompting Techniques

Prompt Engineering helps to effectively design and improve prompts to get better results on different tasks with LLMs.

While the previous basic examples were fun, in this section we cover more advanced prompting engineering techniques that allow us to achieve more complex tasks and improve reliability and performance of LLMs.
# Zero-Shot Prompting

Large language models (LLMs) today, such as GPT-3.5 Turbo, GPT-4, and Claude 3, are tuned to follow instructions and are trained on large amounts of data. Large-scale training makes these models capable of performing some tasks in a "zero-shot" manner. Zero-shot prompting means that the prompt used to interact with the model won't contain examples or demonstrations. The zero-shot prompt directly instructs the model to perform a task without any additional examples to steer it.

We tried a few zero-shot examples in the previous section. Here is one of the examples (ie., text classification) we used:

_Prompt:_

```
Classify the text into neutral, negative or positive. Text: I think the vacation is okay.Sentiment:
```

_Output:_

```
Neutral
```

Note that in the prompt above we didn't provide the model with any examples of text alongside their classifications, the LLM already understands "sentiment" -- that's the zero-shot capabilities at work.

Instruction tuning has been shown to improve zero-shot learning [Wei et al. (2022)](https://arxiv.org/pdf/2109.01652.pdf). Instruction tuning is essentially the concept of finetuning models on datasets described via instructions. Furthermore, [RLHF](https://arxiv.org/abs/1706.03741) (reinforcement learning from human feedback) has been adopted to scale instruction tuning wherein the model is aligned to better fit human preferences. This recent development powers models like ChatGPT. We will discuss all these approaches and methods in upcoming sections.

When zero-shot doesn't work, it's recommended to provide demonstrations or examples in the prompt which leads to few-shot prompting. In the next section, we demonstrate few-shot prompting.
# Few-Shot Prompting

While large-language models demonstrate remarkable zero-shot capabilities, they still fall short on more complex tasks when using the zero-shot setting. Few-shot prompting can be used as a technique to enable in-context learning where we provide demonstrations in the prompt to steer the model to better performance. The demonstrations serve as conditioning for subsequent examples where we would like the model to generate a response.

According to [Touvron et al. 2023](https://arxiv.org/pdf/2302.13971.pdf) few shot properties first appeared when models were scaled to a sufficient size [(Kaplan et al., 2020)](https://arxiv.org/abs/2001.08361).

Let's demonstrate few-shot prompting via an example that was presented in [Brown et al. 2020](https://arxiv.org/abs/2005.14165). In the example, the task is to correctly use a new word in a sentence.

_Prompt:_

```
A "whatpu" is a small, furry animal native to Tanzania. An example of a sentence that uses the word whatpu is:We were traveling in Africa and we saw these very cute whatpus. To do a "farduddle" means to jump up and down really fast. An example of a sentence that uses the word farduddle is:
```

_Output:_

```
When we won the game, we all started to farduddle in celebration.
```

We can observe that the model has somehow learned how to perform the task by providing it with just one example (i.e., 1-shot). For more difficult tasks, we can experiment with increasing the demonstrations (e.g., 3-shot, 5-shot, 10-shot, etc.).

Following the findings from [Min et al. (2022)](https://arxiv.org/abs/2202.12837), here are a few more tips about demonstrations/exemplars when doing few-shot:

- "the label space and the distribution of the input text specified by the demonstrations are both important (regardless of whether the labels are correct for individual inputs)"
- the format you use also plays a key role in performance, even if you just use random labels, this is much better than no labels at all.
- additional results show that selecting random labels from a true distribution of labels (instead of a uniform distribution) also helps.

Let's try out a few examples. Let's first try an example with random labels (meaning the labels Negative and Positive are randomly assigned to the inputs):

_Prompt:_

```
This is awesome! // NegativeThis is bad! // PositiveWow that movie was rad! // PositiveWhat a horrible show! //
```

_Output:_

```
Negative
```

We still get the correct answer, even though the labels have been randomized. Note that we also kept the format, which helps too. In fact, with further experimentation, it seems the newer GPT models we are experimenting with are becoming more robust to even random formats. Example:

_Prompt:_

```
Positive This is awesome! This is bad! NegativeWow that movie was rad!PositiveWhat a horrible show! --
```

_Output:_

```
Negative
```

There is no consistency in the format above but the model still predicted the correct label. We have to conduct a more thorough analysis to confirm if this holds for different and more complex tasks, including different variations of prompts.

### Limitations of Few-shot Prompting[](https://www.promptingguide.ai/techniques/fewshot#limitations-of-few-shot-prompting)

Standard few-shot prompting works well for many tasks but is still not a perfect technique, especially when dealing with more complex reasoning tasks. Let's demonstrate why this is the case. Do you recall the previous example where we provided the following task:

```
The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. A: 
```

If we try this again, the model outputs the following:

```
Yes, the odd numbers in this group add up to 107, which is an even number.
```

This is not the correct response, which not only highlights the limitations of these systems but that there is a need for more advanced prompt engineering.

Let's try to add some examples to see if few-shot prompting improves the results.

_Prompt:_

```
The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.A: The answer is False.The odd numbers in this group add up to an even number: 17,  10, 19, 4, 8, 12, 24.A: The answer is True.The odd numbers in this group add up to an even number: 16,  11, 14, 4, 8, 13, 24.A: The answer is True.The odd numbers in this group add up to an even number: 17,  9, 10, 12, 13, 4, 2.A: The answer is False.The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. A: 
```

_Output:_

```
The answer is True.
```

That didn't work. It seems like few-shot prompting is not enough to get reliable responses for this type of reasoning problem. The example above provides basic information on the task. If you take a closer look, the type of task we have introduced involves a few more reasoning steps. In other words, it might help if we break the problem down into steps and demonstrate that to the model. More recently, [chain-of-thought (CoT) prompting](https://arxiv.org/abs/2201.11903) has been popularized to address more complex arithmetic, commonsense, and symbolic reasoning tasks.

Overall, it seems that providing examples is useful for solving some tasks. When zero-shot prompting and few-shot prompting are not sufficient, it might mean that whatever was learned by the model isn't enough to do well at the task. From here it is recommended to start thinking about fine-tuning your models or experimenting with more advanced prompting techniques. Up next we talk about one of the popular prompting techniques called chain-of-thought prompting which has gained a lot of popularity.
# Chain-of-Thought Prompting

## Chain-of-Thought (CoT) Prompting[](https://www.promptingguide.ai/techniques/cot#chain-of-thought-cot-prompting)

![COT](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcot.1933d9fe.png&w=1920&q=75)

Image Source: [Wei et al. (2022)](https://arxiv.org/abs/2201.11903)

Introduced in [Wei et al. (2022)](https://arxiv.org/abs/2201.11903), chain-of-thought (CoT) prompting enables complex reasoning capabilities through intermediate reasoning steps. You can combine it with few-shot prompting to get better results on more complex tasks that require reasoning before responding.

_Prompt:_

```
The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.A: Adding all the odd numbers (9, 15, 1) gives 25. The answer is False.The odd numbers in this group add up to an even number: 17,  10, 19, 4, 8, 12, 24.A: Adding all the odd numbers (17, 19) gives 36. The answer is True.The odd numbers in this group add up to an even number: 16,  11, 14, 4, 8, 13, 24.A: Adding all the odd numbers (11, 13) gives 24. The answer is True.The odd numbers in this group add up to an even number: 17,  9, 10, 12, 13, 4, 2.A: Adding all the odd numbers (17, 9, 13) gives 39. The answer is False.The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. A:
```

_Output:_

```
Adding all the odd numbers (15, 5, 13, 7, 1) gives 41. The answer is False.
```

Wow! We can see a perfect result when we provided the reasoning step. In fact, we can solve this task by providing even fewer examples, i.e., just one example seems enough:

_Prompt:_

```
The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.A: Adding all the odd numbers (9, 15, 1) gives 25. The answer is False.The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1. A:
```

_Output:_

```
Adding all the odd numbers (15, 5, 13, 7, 1) gives 41. The answer is False.
```

Keep in mind that the authors claim that this is an emergent ability that arises with sufficiently large language models.

## Zero-shot COT Prompting[](https://www.promptingguide.ai/techniques/cot#zero-shot-cot-prompting)

![Zero-shot COT](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fzero-cot.79793bee.png&w=1920&q=75)

Image Source: [Kojima et al. (2022)](https://arxiv.org/abs/2205.11916)

One recent idea that came out more recently is the idea of [zero-shot CoT](https://arxiv.org/abs/2205.11916) (Kojima et al. 2022) that essentially involves adding "Let's think step by step" to the original prompt. Let's try a simple problem and see how the model performs:

_Prompt:_

```
I went to the market and bought 10 apples. I gave 2 apples to the neighbor and 2 to the repairman. I then went and bought 5 more apples and ate 1. How many apples did I remain with?
```

_Output:_

```
11 apples
```

The answer is incorrect! Now Let's try with the special prompt.

_Prompt:_

```
I went to the market and bought 10 apples. I gave 2 apples to the neighbor and 2 to the repairman. I then went and bought 5 more apples and ate 1. How many apples did I remain with?Let's think step by step.
```

_Output:_

```
First, you started with 10 apples.You gave away 2 apples to the neighbor and 2 to the repairman, so you had 6 apples left.Then you bought 5 more apples, so now you had 11 apples.Finally, you ate 1 apple, so you would remain with 10 apples.
```

It's impressive that this simple prompt is effective at this task. This is particularly useful where you don't have too many examples to use in the prompt.

## Automatic Chain-of-Thought (Auto-CoT)[](https://www.promptingguide.ai/techniques/cot#automatic-chain-of-thought-auto-cot)

When applying chain-of-thought prompting with demonstrations, the process involves hand-crafting effective and diverse examples. This manual effort could lead to suboptimal solutions. [Zhang et al. (2022)](https://arxiv.org/abs/2210.03493) propose an approach to eliminate manual efforts by leveraging LLMs with "Let's think step by step" prompt to generate reasoning chains for demonstrations one by one. This automatic process can still end up with mistakes in generated chains. To mitigate the effects of the mistakes, the diversity of demonstrations matter. This work proposes Auto-CoT, which samples questions with diversity and generates reasoning chains to construct the demonstrations.

Auto-CoT consists of two main stages:

- Stage 1): **question clustering**: partition questions of a given dataset into a few clusters
- Stage 2): **demonstration sampling**: select a representative question from each cluster and generate its reasoning chain using Zero-Shot-CoT with simple heuristics

The simple heuristics could be length of questions (e.g., 60 tokens) and number of steps in rationale (e.g., 5 reasoning steps). This encourages the model to use simple and accurate demonstrations.

The process is illustrated below:

![AUTOCOT](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fauto-cot.642d9bad.png&w=3840&q=75)

Image Source: [Zhang et al. (2022)](https://arxiv.org/abs/2210.03493)

Code for Auto-CoT is available [here](https://github.com/amazon-science/auto-cot).

# Meta Prompting

## Introduction[](https://www.promptingguide.ai/techniques/meta-prompting#introduction)

Meta Prompting is an advanced prompting technique that focuses on the structural and syntactical aspects of tasks and problems rather than their specific content details. This goal with meta prompting is to construct a more abstract, structured way of interacting with large language models (LLMs), emphasizing the form and pattern of information over traditional content-centric methods.

## Key Characteristics[](https://www.promptingguide.ai/techniques/meta-prompting#key-characteristics)

According to [Zhang et al. (2024)](https://arxiv.org/abs/2311.11482), the key characteristics of meta prompting can be summarized as follows:

**1. Structure-oriented**: Prioritizes the format and pattern of problems and solutions over specific content.

**2. Syntax-focused**: Uses syntax as a guiding template for the expected response or solution.

**3. Abstract examples**: Employs abstracted examples as frameworks, illustrating the structure of problems and solutions without focusing on specific details.

**4. Versatile**: Applicable across various domains, capable of providing structured responses to a wide range of problems.

**5. Categorical approach**: Draws from type theory to emphasize the categorization and logical arrangement of components in a prompt.

## Advantages over Few-Shot Prompting[](https://www.promptingguide.ai/techniques/meta-prompting#advantages-over-few-shot-prompting)

[Zhang et al., 2024](https://arxiv.org/abs/2311.11482) report that meta prompting and few-shot prompting are different in that it meta prompting focuses on a more structure-oriented approach as opposed to a content-driven approach which few-shot prompting emphasizes.

The following example obtained from [Zhang et al. (2024)](https://arxiv.org/abs/2311.11482) demonstrates the difference between a structured meta prompt and a few-shot prompt for solving problems from the MATH benchmark:

!["Meta Prompting"](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fmeta-prompting.66b824be.png&w=1920&q=75)

The advantages of Meta Prompting over few-shot promoting include:

**1. Token efficiency**: Reduces the number of tokens required by focusing on structure rather than detailed content.

**2. Fair comparison**: Provides a more fair approach for comparing different problem-solving models by minimizing the influence of specific examples.

**3. Zero-shot efficacy**: Can be viewed as a form of zero-shot prompting, where the influence of specific examples is minimized.

## Applications[](https://www.promptingguide.ai/techniques/meta-prompting#applications)

By focusing on the structural patterns of problem-solving, Meta Prompting offers a clear roadmap for navigating complex topics, enhancing the reasoning capabilities of LLMs across various domains.

It's important to note that meta prompting also assumes that the LLM has innate knowledge about the specific task or problem being addressed. As LLMs can generalize to a unseen tasks, it is possible that they can be leveraged with meta prompting but performance might deteriorate with more unique and novel tasks as is the case with zero-shot prompting.

Applications where meta prompting can be beneficial include but not limited to complex reasoning tasks, mathematical problem-solving, coding challenges, theoretical queries.

# Self-Consistency

Perhaps one of the more advanced techniques out there for prompt engineering is self-consistency. Proposed by [Wang et al. (2022)](https://arxiv.org/abs/2203.11171), self-consistency aims "to replace the naive greedy decoding used in chain-of-thought prompting". The idea is to sample multiple, diverse reasoning paths through few-shot CoT, and use the generations to select the most consistent answer. This helps to boost the performance of CoT prompting on tasks involving arithmetic and commonsense reasoning.

Let's try the following example for arithmetic reasoning:

_Prompt:_

```
When I was 6 my sister was half my age. NowI’m 70 how old is my sister?
```

_Output:_

```
35
```

The output is wrong! How may we improve this with self-consistency? Let's try it out. We will use the few-shot exemplars from Wang et al. 2022 (Table 17):

_Prompt:_

```
Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done,there will be 21 trees. How many trees did the grove workers plant today?A: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted.So, they must have planted 21 - 15 = 6 trees. The answer is 6.Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?A: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5.Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?A: Leah had 32 chocolates and Leah’s sister had 42. That means there were originally 32 + 42 = 74chocolates. 35 have been eaten. So in total they still have 74 - 35 = 39 chocolates. The answer is 39.Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipopsdid Jason give to Denny?A: Jason had 20 lollipops. Since he only has 12 now, he must have given the rest to Denny. The number oflollipops he has given to Denny must have been 20 - 12 = 8 lollipops. The answer is 8.Q: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys doeshe have now?A: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toys. Then he got 2 more from dad, soin total he has 7 + 2 = 9 toys. The answer is 9.Q: There were nine computers in the server room. Five more computers were installed each day, frommonday to thursday. How many computers are now in the server room?A: There are 4 days from monday to thursday. 5 computers were added each day. That means in total 4 * 5 =20 computers were added. There were 9 computers in the beginning, so now there are 9 + 20 = 29 computers.The answer is 29.Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How manygolf balls did he have at the end of wednesday?A: Michael initially had 58 balls. He lost 23 on Tuesday, so after that he has 58 - 23 = 35 balls. OnWednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is 33.Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?A: She bought 5 bagels for $3 each. This means she spent $15. She has $8 left.Q: When I was 6 my sister was half my age. Now I’m 70 how old is my sister?A:
```

_Output 1:_

```
When I was 6 my sister was half my age, so she was 3. Now I am 70, so she is 70 - 3 = 67. The answer is 67.
```

_Output 2:_

```
When the narrator was 6, his sister was half his age, which is 3. Now that the narrator is 70, his sister would be 70 - 3 = 67 years old. The answer is 67.
```

_Output 3:_

```
When I was 6 my sister was half my age, so she was 3. Now I am 70, so she is 70/2 = 35. The answer is 35.
```

Computing for the final answer involves a few steps (check out the paper for the details) but for the sake of simplicity, we can see that there is already a majority answer emerging so that would essentially become the final answer.

# Prompt Chaining

## Introduction to Prompt Chaining[](https://www.promptingguide.ai/techniques/prompt_chaining#introduction-to-prompt-chaining)

To improve the reliability and performance of LLMs, one of the important prompt engineering techniques is to break tasks into its subtasks. Once those subtasks have been identified, the LLM is prompted with a subtask and then its response is used as input to another prompt. This is what's referred to as prompt chaining, where a task is split into subtasks with the idea to create a chain of prompt operations.

Prompt chaining is useful to accomplish complex tasks which an LLM might struggle to address if prompted with a very detailed prompt. In prompt chaining, chain prompts perform transformations or additional processes on the generated responses before reaching a final desired state.

Besides achieving better performance, prompt chaining helps to boost the transparency of your LLM application, increases controllability, and reliability. This means that you can debug problems with model responses much more easily and analyze and improve performance in the different stages that need improvement.

Prompt chaining is particularly useful when building LLM-powered conversational assistants and improving the personalization and user experience of your applications.

## Use Cases for Prompt Chaining[](https://www.promptingguide.ai/techniques/prompt_chaining#use-cases-for-prompt-chaining)

### Prompt Chaining for Document QA[](https://www.promptingguide.ai/techniques/prompt_chaining#prompt-chaining-for-document-qa)

Prompt chaining can be used in different scenarios that could involve several operations or transformations. For instance, one common use case of LLMs involves answering questions about a large text document. It helps if you design two different prompts where the first prompt is responsible for extracting relevant quotes to answer a question and a second prompt takes as input the quotes and original document to answer a given question. In other words, you will be creating two different prompts to perform the task of answering a question given in a document.

The first prompt below extracts the relevant quotes from the document given the question. Note that for simplicity, we have added a placeholder for the document `{{document}}`. To test the prompt you can copy and paste an article from Wikipedia such as this page for [prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering). Due to larger context used for this task, we are using the `gpt-4-1106-preview` model from OpenAI. You can use the prompt with other long-context LLMs like Claude.

Prompt 1:

```
You are a helpful assistant. Your task is to help answer a question given in a document. The first step is to extract quotes relevant to the question from the document, delimited by ####. Please output the list of quotes using <quotes></quotes>. Respond with "No relevant quotes found!" if no relevant quotes were found.####{{document}}####
```

Here is a screenshot of the entire prompt including the question which is passed using the `user` role.

![Prompt Chaining Part 1](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fprompt-chaining-1.4bdd376c.png&w=1920&q=75)

Output of Prompt 1:

```
<quotes>- Chain-of-thought (CoT) prompting[27]- Generated knowledge prompting[37]- Least-to-most prompting[38]- Self-consistency decoding[39]- Complexity-based prompting[41]- Self-refine[42]- Tree-of-thought prompting[43]- Maieutic prompting[45]- Directional-stimulus prompting[46]- Textual inversion and embeddings[59]- Using gradient descent to search for prompts[61][62][63][64]- Prompt injection[65][66][67]</quotes>
```

The quotes that were returned in the first prompt can now be used as input to the second prompt below. Note that you can clean up the quotes a bit more, i.e., remove the citations. Those citations could be removed or utilized as part of another prompt in the chain but you can ignore this for now. The second prompt then takes the relevant quotes extracted by prompt 1 and prepares a helpful response to the question given in the document and those extracted quotes. The second prompt can be the following:

Prompt 2:

```
Given a set of relevant quotes (delimited by <quotes></quotes>) extracted from a document and the original document (delimited by ####), please compose an answer to the question. Ensure that the answer is accurate, has a friendly tone, and sounds helpful.####{{document}}####<quotes>- Chain-of-thought (CoT) prompting[27]- Generated knowledge prompting[37]- Least-to-most prompting[38]- Self-consistency decoding[39]- Complexity-based prompting[41]- Self-refine[42]- Tree-of-thought prompting[43]- Maieutic prompting[45]- Directional-stimulus prompting[46]- Textual inversion and embeddings[59]- Using gradient descent to search for prompts[61][62][63][64]- Prompt injection[65][66][67]</quotes>
```

Output of Prompt 2:

```
The prompting techniques mentioned in the document include:1. Chain-of-thought (CoT) prompting[27]2. Generated knowledge prompting[37]3. Least-to-most prompting[38]4. Self-consistency decoding[39]5. Complexity-based prompting[41]6. Self-refine[42]7. Tree-of-thought prompting[43]8. Maieutic prompting[45]9. Directional-stimulus prompting[46]10. Textual inversion and embeddings[59]11. Using gradient descent to search for prompts[61][62][63][64]12. Prompt injection[65][66][67]Each of these techniques employs unique strategies to enhance or specify the interactions with large language models to produce the desired outcomes.
```

As you can see, simplifying and creating prompt chains is a useful prompting approach where the responses need to undergo several operations or transformations. As an exercise, feel free to design a prompt that removes the citations (e.g., [27]) from the response before sending this as a final response to the user of your application.

You can also find more examples of prompt chaining in this [documentation](https://docs.anthropic.com/claude/docs/prompt-chaining) that leverages the Claude LLM. Our example is inspired and adapted from their examples.

# Tree of Thoughts (ToT)

For complex tasks that require exploration or strategic lookahead, traditional or simple prompting techniques fall short. [Yao et el. (2023)](https://arxiv.org/abs/2305.10601) and [Long (2023)](https://arxiv.org/abs/2305.08291) recently proposed Tree of Thoughts (ToT), a framework that generalizes over chain-of-thought prompting and encourages exploration over thoughts that serve as intermediate steps for general problem solving with language models.

ToT maintains a tree of thoughts, where thoughts represent coherent language sequences that serve as intermediate steps toward solving a problem. This approach enables an LM to self-evaluate the progress through intermediate thoughts made towards solving a problem through a deliberate reasoning process. The LM's ability to generate and evaluate thoughts is then combined with search algorithms (e.g., breadth-first search and depth-first search) to enable systematic exploration of thoughts with lookahead and backtracking.

The ToT framework is illustrated below:

![TOT](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FTOT.3b13bc5e.png&w=3840&q=75)

Image Source: [Yao et el. (2023)](https://arxiv.org/abs/2305.10601)

When using ToT, different tasks requires defining the number of candidates and the number of thoughts/steps. For instance, as demonstrated in the paper, Game of 24 is used as a mathematical reasoning task which requires decomposing the thoughts into 3 steps, each involving an intermediate equation. At each step, the best b=5 candidates are kept.

To perform BFS in ToT for the Game of 24 task, the LM is prompted to evaluate each thought candidate as "sure/maybe/impossible" with regard to reaching 24. As stated by the authors, "the aim is to promote correct partial solutions that can be verdicted within few lookahead trials, and eliminate impossible partial solutions based on "too big/small" commonsense, and keep the rest "maybe"". Values are sampled 3 times for each thought. The process is illustrated below:

![TOT2](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FTOT2.9eb8f0f9.png&w=1920&q=75)

Image Source: [Yao et el. (2023)](https://arxiv.org/abs/2305.10601)

From the results reported in the figure below, ToT substantially outperforms the other prompting methods:

![TOT3](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FTOT3.bf83699e.png&w=1920&q=75)

Image Source: [Yao et el. (2023)](https://arxiv.org/abs/2305.10601)

Code available [here](https://github.com/princeton-nlp/tree-of-thought-llm) and [here](https://github.com/jieyilong/tree-of-thought-puzzle-solver)

At a high level, the main ideas of [Yao et el. (2023)](https://arxiv.org/abs/2305.10601) and [Long (2023)](https://arxiv.org/abs/2305.08291) are similar. Both enhance LLM's capability for complex problem solving through tree search via a multi-round conversation. One of the main difference is that [Yao et el. (2023)](https://arxiv.org/abs/2305.10601) leverages DFS/BFS/beam search, while the tree search strategy (i.e. when to backtrack and backtracking by how many levels, etc.) proposed in [Long (2023)](https://arxiv.org/abs/2305.08291) is driven by a "ToT Controller" trained through reinforcement learning. DFS/BFS/Beam search are generic solution search strategies with no adaptation to specific problems. In comparison, a ToT Controller trained through RL might be able learn from new data set or through self-play (AlphaGo vs brute force search), and hence the RL-based ToT system can continue to evolve and learn new knowledge even with a fixed LLM.

[Hulbert (2023)](https://github.com/dave1010/tree-of-thought-prompting) has proposed Tree-of-Thought Prompting, which applies the main concept from ToT frameworks as a simple prompting technique, getting the LLM to evaluate intermediate thoughts in a single prompt. A sample ToT prompt is:

```
Imagine three different experts are answering this question.All experts will write down 1 step of their thinking,then share it with the group.Then all experts will go on to the next step, etc.If any expert realises they're wrong at any point then they leave.The question is...
```

[Sun (2023)](https://github.com/holarissun/PanelGPT) benchmarked the Tree-of-Thought Prompting with large-scale experiments, and introduce PanelGPT --- an idea of prompting with Panel discussions among LLMs.

# Retrieval Augmented Generation (RAG)

General-purpose language models can be fine-tuned to achieve several common tasks such as sentiment analysis and named entity recognition. These tasks generally don't require additional background knowledge.

For more complex and knowledge-intensive tasks, it's possible to build a language model-based system that accesses external knowledge sources to complete tasks. This enables more factual consistency, improves reliability of the generated responses, and helps to mitigate the problem of "hallucination".

Meta AI researchers introduced a method called [Retrieval Augmented Generation (RAG)](https://ai.facebook.com/blog/retrieval-augmented-generation-streamlining-the-creation-of-intelligent-natural-language-processing-models/) to address such knowledge-intensive tasks. RAG combines an information retrieval component with a text generator model. RAG can be fine-tuned and its internal knowledge can be modified in an efficient manner and without needing retraining of the entire model.

RAG takes an input and retrieves a set of relevant/supporting documents given a source (e.g., Wikipedia). The documents are concatenated as context with the original input prompt and fed to the text generator which produces the final output. This makes RAG adaptive for situations where facts could evolve over time. This is very useful as LLMs's parametric knowledge is static. RAG allows language models to bypass retraining, enabling access to the latest information for generating reliable outputs via retrieval-based generation.

Lewis et al., (2021) proposed a general-purpose fine-tuning recipe for RAG. A pre-trained seq2seq model is used as the parametric memory and a dense vector index of Wikipedia is used as non-parametric memory (accessed using a neural pre-trained retriever). Below is a overview of how the approach works:

![RAG](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frag.c6528d99.png&w=1920&q=75)

Image Source: [Lewis et el. (2021)](https://arxiv.org/pdf/2005.11401.pdf)

RAG performs strong on several benchmarks such as [Natural Questions](https://ai.google.com/research/NaturalQuestions), [WebQuestions](https://paperswithcode.com/dataset/webquestions), and CuratedTrec. RAG generates responses that are more factual, specific, and diverse when tested on MS-MARCO and Jeopardy questions. RAG also improves results on FEVER fact verification.

This shows the potential of RAG as a viable option for enhancing outputs of language models in knowledge-intensive tasks.

More recently, these retriever-based approaches have become more popular and are combined with popular LLMs like ChatGPT to improve capabilities and factual consistency.

# Automatic Reasoning and Tool-use (ART)

Combining CoT prompting and tools in an interleaved manner has shown to be a strong and robust approach to address many tasks with LLMs. These approaches typically require hand-crafting task-specific demonstrations and carefully scripted interleaving of model generations with tool use. [Paranjape et al., (2023)](https://arxiv.org/abs/2303.09014) propose a new framework that uses a frozen LLM to automatically generate intermediate reasoning steps as a program.

ART works as follows:

- given a new task, it select demonstrations of multi-step reasoning and tool use from a task library
- at test time, it pauses generation whenever external tools are called, and integrate their output before resuming generation

ART encourages the model to generalize from demonstrations to decompose a new task and use tools in appropriate places, in a zero-shot fashion. In addition, ART is extensible as it also enables humans to fix mistakes in the reasoning steps or add new tools by simply updating the task and tool libraries. The process is demonstrated below:

![ART](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FART.3b30f615.png&w=1200&q=75)

Image Source: [Paranjape et al., (2023)](https://arxiv.org/abs/2303.09014)

ART substantially improves over few-shot prompting and automatic CoT on unseen tasks in the BigBench and MMLU benchmarks, and exceeds performance of hand-crafted CoT prompts when human feedback is incorporated.

Below is a table demonstrating ART's performance on BigBench and MMLU tasks:

![ART2](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FART2.9fb2b217.png&w=1920&q=75)

# Automatic Prompt Engineer (APE)

![APE](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FAPE.3f0e01c2.png&w=1920&q=75)

Image Source: [Zhou et al., (2022)](https://arxiv.org/abs/2211.01910)

[Zhou et al., (2022)](https://arxiv.org/abs/2211.01910) propose automatic prompt engineer (APE) a framework for automatic instruction generation and selection. The instruction generation problem is framed as natural language synthesis addressed as a black-box optimization problem using LLMs to generate and search over candidate solutions.

The first step involves a large language model (as an inference model) that is given output demonstrations to generate instruction candidates for a task. These candidate solutions will guide the search procedure. The instructions are executed using a target model, and then the most appropriate instruction is selected based on computed evaluation scores.

APE discovers a better zero-shot CoT prompt than the human engineered "Let's think step by step" prompt ([Kojima et al., 2022](https://arxiv.org/abs/2205.11916)).

The prompt "Let's work this out in a step by step way to be sure we have the right answer." elicits chain-of-thought reasoning and improves performance on the MultiArith and GSM8K benchmarks:

![APECOT](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fape-zero-shot-cot.75c0f75c.png&w=1920&q=75)

Image Source: [Zhou et al., (2022)](https://arxiv.org/abs/2211.01910)

This paper touches on an important topic related to prompt engineering which is the idea of automatically optimizing prompts. While we don't go deep into this topic in this guide, here are a few key papers if you are interested in the topic:

- [Prompt-OIRL](https://arxiv.org/abs/2309.06553) - proposes to use offline inverse reinforcement learning to generate query-dependent prompts.
- [OPRO](https://arxiv.org/abs/2309.03409) - introduces the idea of using LLMs to optimize prompts: let LLMs "Take a deep breath" improves the performance on math problems.
- [AutoPrompt](https://arxiv.org/abs/2010.15980) - proposes an approach to automatically create prompts for a diverse set of tasks based on gradient-guided search.
- [Prefix Tuning](https://arxiv.org/abs/2101.00190) - a lightweight alternative to fine-tuning that prepends a trainable continuous prefix for NLG tasks.
- [Prompt Tuning](https://arxiv.org/abs/2104.08691) - proposes a mechanism for learning soft prompts through backpropagation.

# Active-Prompt

Chain-of-thought (CoT) methods rely on a fixed set of human-annotated exemplars. The problem with this is that the exemplars might not be the most effective examples for the different tasks. To address this, [Diao et al., (2023)](https://arxiv.org/pdf/2302.12246.pdf) recently proposed a new prompting approach called Active-Prompt to adapt LLMs to different task-specific example prompts (annotated with human-designed CoT reasoning).

Below is an illustration of the approach. The first step is to query the LLM with or without a few CoT examples. _k_ possible answers are generated for a set of training questions. An uncertainty metric is calculated based on the _k_ answers (disagreement used). The most uncertain questions are selected for annotation by humans. The new annotated exemplars are then used to infer each question.

![ACTIVE](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Factive-prompt.f739657b.png&w=3840&q=75)

Image Source: [Diao et al., (2023)](https://arxiv.org/pdf/2302.12246.pdf)

# Directional Stimulus Prompting

[Li et al., (2023)](https://arxiv.org/abs/2302.11520) proposes a new prompting technique to better guide the LLM in generating the desired summary.

A tuneable policy LM is trained to generate the stimulus/hint. Seeing more use of RL to optimize LLMs.

The figure below shows how Directional Stimulus Prompting compares with standard prompting. The policy LM can be small and optimized to generate the hints that guide a black-box frozen LLM.

![DSP](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fdsp.27a0005f.jpeg&w=3840&q=75)
Image Source: [Li et al., (2023)](https://arxiv.org/abs/2302.11520)

# PAL (Program-Aided Language Models)

[Gao et al., (2022)](https://arxiv.org/abs/2211.10435) presents a method that uses LLMs to read natural language problems and generate programs as the intermediate reasoning steps. Coined, program-aided language models (PAL), it differs from chain-of-thought prompting in that instead of using free-form text to obtain solution it offloads the solution step to a programmatic runtime such as a Python interpreter.

![PAL](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fpal.dfc96526.png&w=1920&q=75)

Image Source: [Gao et al., (2022)](https://arxiv.org/abs/2211.10435)

Let's look at an example using LangChain and OpenAI GPT-3. We are interested to develop a simple application that's able to interpret the question being asked and provide an answer by leveraging the Python interpreter.

Specifically, we are interested to create a functionality that allows the use of the LLM to answer questions that require date understanding. We will provide the LLM a prompt that includes a few exemplars which are adopted from [here](https://github.com/reasoning-machines/pal/blob/main/pal/prompt/date_understanding_prompt.py).

These are the imports we need:

```
import openaifrom datetime import datetimefrom dateutil.relativedelta import relativedeltaimport osfrom langchain.llms import OpenAIfrom dotenv import load_dotenv
```

Let's first configure a few things:

```
load_dotenv() # API configurationopenai.api_key = os.getenv("OPENAI_API_KEY") # for LangChainos.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
```

Setup model instance:

```
llm = OpenAI(model_name='text-davinci-003', temperature=0)
```

Setup prompt + question:

```
question = "Today is 27 February 2023. I was born exactly 25 years ago. What is the date I was born in MM/DD/YYYY?" DATE_UNDERSTANDING_PROMPT = """# Q: 2015 is coming in 36 hours. What is the date one week from today in MM/DD/YYYY?# If 2015 is coming in 36 hours, then today is 36 hours before.today = datetime(2015, 1, 1) - relativedelta(hours=36)# One week from today,one_week_from_today = today + relativedelta(weeks=1)# The answer formatted with %m/%d/%Y isone_week_from_today.strftime('%m/%d/%Y')# Q: The first day of 2019 is a Tuesday, and today is the first Monday of 2019. What is the date today in MM/DD/YYYY?# If the first day of 2019 is a Tuesday, and today is the first Monday of 2019, then today is 6 days later.today = datetime(2019, 1, 1) + relativedelta(days=6)# The answer formatted with %m/%d/%Y istoday.strftime('%m/%d/%Y')# Q: The concert was scheduled to be on 06/01/1943, but was delayed by one day to today. What is the date 10 days ago in MM/DD/YYYY?# If the concert was scheduled to be on 06/01/1943, but was delayed by one day to today, then today is one day later.today = datetime(1943, 6, 1) + relativedelta(days=1)# 10 days ago,ten_days_ago = today - relativedelta(days=10)# The answer formatted with %m/%d/%Y isten_days_ago.strftime('%m/%d/%Y')# Q: It is 4/19/1969 today. What is the date 24 hours later in MM/DD/YYYY?# It is 4/19/1969 today.today = datetime(1969, 4, 19)# 24 hours later,later = today + relativedelta(hours=24)# The answer formatted with %m/%d/%Y istoday.strftime('%m/%d/%Y')# Q: Jane thought today is 3/11/2002, but today is in fact Mar 12, which is 1 day later. What is the date 24 hours later in MM/DD/YYYY?# If Jane thought today is 3/11/2002, but today is in fact Mar 12, then today is 3/12/2002.today = datetime(2002, 3, 12)# 24 hours later,later = today + relativedelta(hours=24)# The answer formatted with %m/%d/%Y islater.strftime('%m/%d/%Y')# Q: Jane was born on the last day of Feburary in 2001. Today is her 16-year-old birthday. What is the date yesterday in MM/DD/YYYY?# If Jane was born on the last day of Feburary in 2001 and today is her 16-year-old birthday, then today is 16 years later.today = datetime(2001, 2, 28) + relativedelta(years=16)# Yesterday,yesterday = today - relativedelta(days=1)# The answer formatted with %m/%d/%Y isyesterday.strftime('%m/%d/%Y')# Q: {question}""".strip() + '\n'
```

```
llm_out = llm(DATE_UNDERSTANDING_PROMPT.format(question=question))print(llm_out)
```

This will output the following:

```
# If today is 27 February 2023 and I was born exactly 25 years ago, then I was born 25 years before.today = datetime(2023, 2, 27)# I was born 25 years before,born = today - relativedelta(years=25)# The answer formatted with %m/%d/%Y isborn.strftime('%m/%d/%Y')
```

The contents of `llm_out` are a Python code snippet. Below, the `exec` command is used to execute this Python code snippet.

```
exec(llm_out)print(born)
```

This will output the following: `02/27/1998`

# ReAct Prompting

[Yao et al., 2022](https://arxiv.org/abs/2210.03629) introduced a framework named ReAct where LLMs are used to generate both _reasoning traces_ and _task-specific actions_ in an interleaved manner.

Generating reasoning traces allow the model to induce, track, and update action plans, and even handle exceptions. The action step allows to interface with and gather information from external sources such as knowledge bases or environments.

The ReAct framework can allow LLMs to interact with external tools to retrieve additional information that leads to more reliable and factual responses.

Results show that ReAct can outperform several state-of-the-art baselines on language and decision-making tasks. ReAct also leads to improved human interpretability and trustworthiness of LLMs. Overall, the authors found that best approach uses ReAct combined with chain-of-thought (CoT) that allows use of both internal knowledge and external information obtained during reasoning.

## How it Works?[](https://www.promptingguide.ai/techniques/react#how-it-works)

ReAct is inspired by the synergies between "acting" and "reasoning" which allow humans to learn new tasks and make decisions or reasoning.

Chain-of-thought (CoT) prompting has shown the capabilities of LLMs to carry out reasoning traces to generate answers to questions involving arithmetic and commonsense reasoning, among other tasks [(Wei et al., 2022)](https://arxiv.org/abs/2201.11903). But its lack of access to the external world or inability to update its knowledge can lead to issues like fact hallucination and error propagation.

ReAct is a general paradigm that combines reasoning and acting with LLMs. ReAct prompts LLMs to generate verbal reasoning traces and actions for a task. This allows the system to perform dynamic reasoning to create, maintain, and adjust plans for acting while also enabling interaction to external environments (e.g., Wikipedia) to incorporate additional information into the reasoning. The figure below shows an example of ReAct and the different steps involved to perform question answering.

![REACT](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Freact.8e7c93ae.png&w=1920&q=75)

Image Source: [Yao et al., 2022](https://arxiv.org/abs/2210.03629)

In the example above, we pass a prompt like the following question from [HotpotQA](https://hotpotqa.github.io/):

```
Aside from the Apple Remote, what other devices can control the program Apple Remote was originally designed to interact with?
```

Note that in-context examples are also added to the prompt but we exclude that here for simplicity. We can see that the model generates _task solving trajectories_ (Thought, Act). Obs corresponds to observation from the environment that's being interacted with (e.g., Search engine). In essence, ReAct can retrieve information to support reasoning, while reasoning helps to target what to retrieve next.

## ReAct Prompting[](https://www.promptingguide.ai/techniques/react#react-prompting)

To demonstrate how ReAct prompting works, let's follow an example from the paper.

The first step is to select cases from a training set (e.g., HotPotQA) and compose ReAct-format trajectories. These are used as few-shot exemplars in the prompts. The trajectories consist of multiple thought-action-observation steps as shown in the figure above. The free-form thoughts are used to achieve different tasks such as decomposing questions, extracting information, performing commonsense/arithmetic reasoning, guide search formulation, and synthesizing final answer.

Here is an example of what the ReAct prompt exemplars look like (obtained from the paper and shortened to one example for simplicity):

```
Question What is the elevation range for the area that the eastern sector of theColorado orogeny extends into?Thought 1 I need to search Colorado orogeny, find the area that the eastern sectorof the Colorado orogeny extends into, then find the elevation range of thearea.Action 1 Search[Colorado orogeny]Observation 1 The Colorado orogeny was an episode of mountain building (an orogeny) inColorado and surrounding areas.Thought 2 It does not mention the eastern sector. So I need to look up easternsector.Action 2 Lookup[eastern sector]Observation 2 (Result 1 / 1) The eastern sector extends into the High Plains and is calledthe Central Plains orogeny.Thought 3 The eastern sector of Colorado orogeny extends into the High Plains. So Ineed to search High Plains and find its elevation range.Action 3 Search[High Plains]Observation 3 High Plains refers to one of two distinct land regionsThought 4 I need to instead search High Plains (United States).Action 4 Search[High Plains (United States)]Observation 4 The High Plains are a subregion of the Great Plains. From east to west, theHigh Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130m).[3]Thought 5 High Plains rise in elevation from around 1,800 to 7,000 ft, so the answeris 1,800 to 7,000 ft.Action 5 Finish[1,800 to 7,000 ft]...
```

Note that different prompts setups are used for different types of tasks. For tasks where reasoning is of primary importance (e.g., HotpotQA), multiple thought-action-observation steps are used for the task-solving trajectory. For decision making tasks involving lots of action steps, thoughts are used sparsely.

## Results on Knowledge-Intensive Tasks[](https://www.promptingguide.ai/techniques/react#results-on-knowledge-intensive-tasks)

The paper first evaluates ReAct on knowledge-intensive reasoning tasks such as question answering (HotPotQA) and fact verification ([Fever](https://fever.ai/resources.html)). PaLM-540B is used as the base model for prompting.

![REACT1](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftable1.e25bc12b.png&w=1920&q=75)

Image Source: [Yao et al., 2022](https://arxiv.org/abs/2210.03629)

The prompting results on HotPotQA and Fever using different prompting methods show that ReAct generally performs better than Act (involves acting only) on both tasks.

We can also observe that ReAct outperforms CoT on Fever and lags behind CoT on HotpotQA. A detailed error analysis is provided in the paper. In summary:

- CoT suffers from fact hallucination
- ReAct's structural constraint reduces its flexibility in formulating reasoning steps
- ReAct depends a lot on the information it's retrieving; non-informative search results derails the model reasoning and leads to difficulty in recovering and reformulating thoughts

Prompting methods that combine and support switching between ReAct and CoT+Self-Consistency generally outperform all the other prompting methods.

## Results on Decision Making Tasks[](https://www.promptingguide.ai/techniques/react#results-on-decision-making-tasks)

The paper also reports results demonstrating ReAct's performance on decision making tasks. ReAct is evaluated on two benchmarks called [ALFWorld](https://alfworld.github.io/) (text-based game) and [WebShop](https://webshop-pnlp.github.io/) (online shopping website environment). Both involve complex environments that require reasoning to act and explore effectively.

Note that the ReAct prompts are designed differently for these tasks while still keeping the same core idea of combining reasoning and acting. Below is an example for an ALFWorld problem involving ReAct prompting.

![REACT2](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Falfworld.da30656d.png&w=1920&q=75)

Image Source: [Yao et al., 2022](https://arxiv.org/abs/2210.03629)

ReAct outperforms Act on both ALFWorld and Webshop. Act, without any thoughts, fails to correctly decompose goals into subgoals. Reasoning seems to be advantageous in ReAct for these types of tasks but current prompting-based methods are still far from the performance of expert humans on these tasks.

Check out the paper for more detailed results.

## LangChain ReAct Usage[](https://www.promptingguide.ai/techniques/react#langchain-react-usage)

Below is a high-level example of how the ReAct prompting approach works in practice. We will be using OpenAI for the LLM and [LangChain](https://python.langchain.com/en/latest/index.html) as it already has built-in functionality that leverages the ReAct framework to build agents that perform tasks by combining the power of LLMs and different tools.

First, let's install and import the necessary libraries:

```
%%capture# update or install the necessary libraries!pip install --upgrade openai!pip install --upgrade langchain!pip install --upgrade python-dotenv!pip install google-search-results # import librariesimport openaiimport osfrom langchain.llms import OpenAIfrom langchain.agents import load_toolsfrom langchain.agents import initialize_agentfrom dotenv import load_dotenvload_dotenv() # load API keys; you will need to obtain these if you haven't yetos.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY") 
```

Now we can configure the LLM, the tools we will use, and the agent that allows us to leverage the ReAct framework together with the LLM and tools. Note that we are using a search API for searching external information and LLM as a math tool.

```
llm = OpenAI(model_name="text-davinci-003" ,temperature=0)tools = load_tools(["google-serper", "llm-math"], llm=llm)agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
```

Once that's configured, we can now run the agent with the desired query/prompt. Notice that here we are not expected to provide few-shot exemplars as explained in the paper.

```
agent.run("Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?")
```

The chain execution looks as follows:

```
> Entering new AgentExecutor chain... I need to find out who Olivia Wilde's boyfriend is and then calculate his age raised to the 0.23 power.Action: SearchAction Input: "Olivia Wilde boyfriend"Observation: Olivia Wilde started dating Harry Styles after ending her years-long engagement to Jason Sudeikis — see their relationship timeline.Thought: I need to find out Harry Styles' age.Action: SearchAction Input: "Harry Styles age"Observation: 29 yearsThought: I need to calculate 29 raised to the 0.23 power.Action: CalculatorAction Input: 29^0.23Observation: Answer: 2.169459462491557 Thought: I now know the final answer.Final Answer: Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557. > Finished chain.
```

The output we get is as follows:

```
"Harry Styles, Olivia Wilde's boyfriend, is 29 years old and his age raised to the 0.23 power is 2.169459462491557."
```

We adapted the example from the [LangChain documentation](https://python.langchain.com/docs/modules/agents/agent_types/react), so credit goes to them. We encourage the learner to explore different combination of tools and tasks.

You can find the notebook for this code here: [https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/notebooks/react.ipynb](https://github.com/dair-ai/Prompt-Engineering-Guide/blob/main/notebooks/react.ipynb)

# Reflexion

Reflexion is a framework to reinforce language-based agents through linguistic feedback. According to [Shinn et al. (2023)](https://arxiv.org/pdf/2303.11366.pdf), "Reflexion is a new paradigm for ‘verbal‘ reinforcement that parameterizes a policy as an agent’s memory encoding paired with a choice of LLM parameters."

At a high level, Reflexion converts feedback (either free-form language or scalar) from the environment into linguistic feedback, also referred to as **self-reflection**, which is provided as context for an LLM agent in the next episode. This helps the agent rapidly and effectively learn from prior mistakes leading to performance improvements on many advanced tasks.

!["Reflexion Framework"](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Freflexion.1053729e.png&w=1920&q=75)

As shown in the figure above, Reflexion consists of three distinct models:

- **An Actor**: Generates text and actions based on the state observations. The Actor takes an action in an environment and receives an observation which results in a trajectory. [Chain-of-Thought (CoT)](https://www.promptingguide.ai/techniques/cot) and [ReAct](https://www.promptingguide.ai/techniques/react) are used as Actor models. A memory component is also added to provide additional context to the agent.
- **An Evaluator**: Scores outputs produced by the Actor. Concretely, it takes as input a generated trajectory (also denoted as short-term memory) and outputs a reward score. Different reward functions are used depending on the task (LLMs and rule-based heuristics are used for decision-making tasks).
- **Self-Reflection**: Generates verbal reinforcement cues to assist the Actor in self-improvement. This role is achieved by an LLM and provides valuable feedback for future trials. To generate specific and relevant feedback, which is also stored in memory, the self-reflection model makes use of the reward signal, the current trajectory, and its persistent memory. These experiences (stored in long-term memory) are leveraged by the agent to rapidly improve decision-making.

In summary, the key steps of the Reflexion process are a) define a task, b) generate a trajectory, c) evaluate, d) perform reflection, and e) generate the next trajectory. The figure below demonstrates examples of how a Reflexion agent can learn to iteratively optimize its behavior to solve various tasks such as decision-making, programming, and reasoning. Reflexion extends the ReAct framework by introducing self-evaluation, self-reflection and memory components.

!["Reflexion Examples"](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Freflexion-examples.7558c279.png&w=3840&q=75)

## Results[](https://www.promptingguide.ai/techniques/reflexion#results)

Experimental results demonstrate that Reflexion agents significantly improve performance on decision-making AlfWorld tasks, reasoning questions in HotPotQA, and Python programming tasks on HumanEval.

When evaluated on sequential decision-making (AlfWorld) tasks, ReAct + Reflexion significantly outperforms ReAct by completing 130/134 tasks using self-evaluation techniques of Heuristic and GPT for binary classification.

!["Reflexion ALFWorld Results"](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Freflexion-alfworld.54c4ce9c.png&w=3840&q=75)

Reflexion significantly outperforms all baseline approaches over several learning steps. For reasoning only and when adding an episodic memory consisting of the most recent trajectory, Reflexion + CoT outperforms CoT only and CoT with episodic memory, respectively.

!["Reflexion ALFWorld Results"](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Freflexion-hotpotqa.2753b155.png&w=1920&q=75)

As summarized in the table below, Reflexion generally outperforms the previous state-of-the-art approaches on Python and Rust code writing on MBPP, HumanEval, and Leetcode Hard.

!["Reflexion ALFWorld Results"](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Freflexion-programming.56effd6a.png&w=1920&q=75)

## When to Use Reflexion?[](https://www.promptingguide.ai/techniques/reflexion#when-to-use-reflexion)

Reflexion is best suited for the following:

1. **An agent needs to learn from trial and error**: Reflexion is designed to help agents improve their performance by reflecting on past mistakes and incorporating that knowledge into future decisions. This makes it well-suited for tasks where the agent needs to learn through trial and error, such as decision-making, reasoning, and programming.
    
2. **Traditional reinforcement learning methods are impractical**: Traditional reinforcement learning (RL) methods often require extensive training data and expensive model fine-tuning. Reflexion offers a lightweight alternative that doesn't require fine-tuning the underlying language model, making it more efficient in terms of data and compute resources.
    
3. **Nuanced feedback is required**: Reflexion utilizes verbal feedback, which can be more nuanced and specific than scalar rewards used in traditional RL. This allows the agent to better understand its mistakes and make more targeted improvements in subsequent trials.
    
4. **Interpretability and explicit memory are important**: Reflexion provides a more interpretable and explicit form of episodic memory compared to traditional RL methods. The agent's self-reflections are stored in its memory, allowing for easier analysis and understanding of its learning process.
    

Reflexion is effective in the following tasks:

- **Sequential decision-making**: Reflexion agents improve their performance in AlfWorld tasks, which involve navigating through various environments and completing multi-step objectives.
- **Reasoning**: Reflexion improved the performance of agents on HotPotQA, a question-answering dataset that requires reasoning over multiple documents.
- **Programming**: Reflexion agents write better code on benchmarks like HumanEval and MBPP, achieving state-of-the-art results in some cases.

Here are some limitations of Reflexion:

- **Reliance on self-evaluation capabilities**: Reflexion relies on the agent's ability to accurately evaluate its performance and generate useful self-reflections. This can be challenging, especially for complex tasks but it's expected that Reflexion gets better over time as models keep improving in capabilities.
- **Long-term memory constraints**: Reflexion makes use of a sliding window with maximum capacity but for more complex tasks it may be advantageous to use advanced structures such as vector embedding or SQL databases.
- **Code generation limitations**: There are limitations to test-driven development in specifying accurate input-output mappings (e.g., non-deterministic generator function and function outputs influenced by hardware).
# Multimodal CoT Prompting

[Zhang et al. (2023)](https://arxiv.org/abs/2302.00923) recently proposed a multimodal chain-of-thought prompting approach. Traditional CoT focuses on the language modality. In contrast, Multimodal CoT incorporates text and vision into a two-stage framework. The first step involves rationale generation based on multimodal information. This is followed by the second phase, answer inference, which leverages the informative generated rationales.

The multimodal CoT model (1B) outperforms GPT-3.5 on the ScienceQA benchmark.

![MCOT](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fmultimodal-cot.a84f6cc1.png&w=1920&q=75)

Image Source: [Zhang et al. (2023)](https://arxiv.org/abs/2302.00923)

Further reading:

- [Language Is Not All You Need: Aligning Perception with Language Models](https://arxiv.org/abs/2302.14045) (Feb 2023)

# GraphPrompts

[Liu et al., 2023](https://arxiv.org/abs/2302.08043) introduces GraphPrompt, a new prompting framework for graphs to improve performance on downstream tasks.
