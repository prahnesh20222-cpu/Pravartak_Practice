'''
All reusable functions and utilities will be set up here
'''
from openai import AsyncOpenAI
from settings import my_settings

client = AsyncOpenAI(
    api_key = my_settings.OPENAI_API_KEY,
    base_url = my_settings.OPENAI_BASE_URL

)

async def call_openai(user_query):
    '''
    if we don't import AsyncOpenAI, we can't make this async on client.chat.completions.create
    OpenAI by itself does not support async
    '''
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Give a concise reponse to the user query"},
            {"role": "user",   "content": user_query},
        ]
        )
    print(response.choices[0].message.content)

    
