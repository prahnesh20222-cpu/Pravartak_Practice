async def test():
    print("testing")

async def hello():
    print("hello world")
    await test()

#await hello()

import asyncio

asyncio.run(hello())

async def hello():
    print("hello world")

async def howdy():
    print("howdy")

async def fine():
    print("I'm fine!")


async def main():
    await asyncio.gather(hello(), howdy(), fine())
 # Note: Gather cannote be called outside a function  by using asyncio.run()
 # This will print "hello world", "howdy", and "I'm fine!" in any order.

asyncio.run(main())