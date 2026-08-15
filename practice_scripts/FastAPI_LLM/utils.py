'''
All reusable functions and utilities will be set up here
'''
from openai import AsyncOpenAI
from settings import my_settings
import asyncio
import time

client = AsyncOpenAI(
    api_key = my_settings.OPENAI_API_KEY,
    base_url = my_settings.OPENAI_BASE_URL

)

async def call_openai(user_query : str,temperature :float = my_settings.OPEN_AI_TEMPERATURE) -> dict:
    '''
    if we don't import AsyncOpenAI, we can't make this async on client.chat.completions.create
    OpenAI by itself does not support async
    '''
    for attempt in range(my_settings.OPEN_AI_RETRIES): #values 0,1,2
        try:
            start_time = time.perf_counter()
            response = await client.chat.completions.create(model="gpt-4o-mini",
                                                            messages=[{"role": "system", "content": "You are a helpful assistant. Give a concise reponse to the user query"},
                                                                      {"role": "user",   "content": user_query},
        ],
        temperature=temperature,
        timeout=60 #if response takes >=60s will it retry?
        )
            end_time = time.perf_counter()     
            final_response = {
                "response": response, 
                "model" : response.model,
                "response" : response.choices[0].message.content,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens" : response.usage.completion_tokens,
                "total_tokens":  response.usage.total_tokens,
                "time_taken": round(end_time - start_time, 3)
    }
            return final_response
        except Exception as e:
            end_time = time.perf_counter() # this is needed to know how long it takes when it hits exception block
            time_taken = round(end_time - start_time, 3)
            print(time_taken)
            if attempt == my_settings.OPEN_AI_RETRIES -1: # this will be the last value in the range which is 2 or last retry
                raise e
            await asyncio.sleep(2) # after every failed attempt wait for 2 seconds


    
