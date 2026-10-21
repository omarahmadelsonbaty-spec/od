import asyncio
import aiosqlite

async def check():
    async with aiosqlite.connect("his.db") as db:
        async with db.execute("SELECT id, input, reply FROM history") as cursor:
            async for row in cursor:
                print(f"ID: {row[0]}\ninput: {row[1]}\nresponse: {row[2]}\n--------------")
asyncio.run(check())