import utils as ut
import asyncio
question = "Hello"

async def main():
    response = await ut.call_openai(question)
    print(response)

asyncio.run(main())