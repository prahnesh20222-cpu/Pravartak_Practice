import utils as ut
import asyncio
question = "Hello"

async def main():
    await ut.call_openai(question)

asyncio.run(main())