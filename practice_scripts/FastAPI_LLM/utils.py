#All reusable functions and utilities will be set up here

from openai import AsyncOpenAI
from settings import my_settings
import asyncio
import time

client = AsyncOpenAI(
    api_key = my_settings.OPENAI_API_KEY,
    base_url = my_settings.OPENAI_BASE_URL

)

async def call_openai(user_query : str,temperature :float = my_settings.OPEN_AI_TEMPERATURE, retires: int = my_settings.OPEN_AI_RETRIES, timeout : int = my_settings.OPEN_AI_TIMEOUT) -> dict:
    '''
    if we don't import AsyncOpenAI, we can't make this async on client.chat.completions.create
    OpenAI by itself does not support async
    '''
    for attempt in range(retires): #values 0,1,2
        try:
            start_time = time.perf_counter()
            response = await client.chat.completions.create(model="gpt-4o-mini",
                                                            messages=[{"role": "system", "content": "You are a helpful assistant. Give a concise reponse to the user query"},
                                                                      {"role": "user",   "content": user_query},
        ],
        temperature=temperature,
        timeout=timeout #if response takes >=60s will it retry?
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
            if attempt == retires -1: # this will be the last value in the range which is 2 or last retry
                raise e
            await asyncio.sleep(2) # after every failed attempt wait for 2 seconds

import httpx
async def calculate_interest(principal:float, rate:float, time:float) -> dict:
    interest = (principal*rate*time)/100
    total_repayable = principal+interest
    return {
        "interest": round(interest, 2),
        "total_amount": round(total_repayable, 2)
    }

async def fetch_stock_date(symbol:str, interval:str="5min", apikey:str = 'demo' ) -> dict:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": apikey,
    }
    response = httpx.get(url, params=params, timeout=30)
    return response.json()
    
