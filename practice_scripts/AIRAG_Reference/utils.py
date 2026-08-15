from openai import AsyncOpenAI
from settings import my_settings
import asyncio
import time

client = AsyncOpenAI(
    api_key=my_settings.OPEN_AI_API_KEY,
    base_url=my_settings.OPEN_AI_BASE_URL
)

async def call_open_ai(user_query : str, 
                       temperature : float = 0.2, 
                       retries : int = my_settings.OPEN_AI_RETRIES) -> dict:
    for attempt in range(retries): # 0,1,2
        try:
            start_time = time.perf_counter()
            response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. respond to the user as per the question in a gentle way"},
                {"role": "user", "content": user_query}
            ],
            temperature=temperature,
            timeout=60
            )
            end_time = time.perf_counter()
            final_reponse = {
            "response": response.choices[0].message.content,
            "model": response.model,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
            "time_taken" : end_time-start_time
            }
            return final_reponse
        except Exception as e:
            end_time = time.perf_counter()
            time_taken = end_time-start_time
            print(time_taken)
            if attempt == retries - 1:
                raise e
            await asyncio.sleep(2)