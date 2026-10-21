import os
import aiosqlite
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    async with aiosqlite.connect("his.db") as db:
        await db.execute('DROP TABLE IF EXISTS history')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input TEXT NOT NULL,
                reply TEXT NOT NULL
            )
        ''')
        await db.commit()

class RequestData(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
@app.post("/")
async def chat_endpoint(data: RequestData):
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    
    async with aiosqlite.connect("his.db") as db:
        async with db.execute("SELECT input, reply FROM history ORDER BY id DESC LIMIT 10") as cursor:
            rows = await cursor.fetchall()
            for past_input, past_reply in reversed(rows):
                messages.append({"role": "user", "content": past_input})
                messages.append({"role": "assistant", "content": past_reply})

    messages.append({"role": "user", "content": data.message})

    response = await client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )
    
    reply = response.choices[0].message.content

    async with aiosqlite.connect("his.db") as db:
        await db.execute('INSERT INTO history (input, reply) VALUES (?, ?)', (data.message, reply))
        await db.commit()

    return {"response": reply}

@app.delete("/history")
async def clear_history():
    async with aiosqlite.connect("his.db") as db:
        await db.execute("DELETE FROM history")
        await db.commit()
    return {"status": "cleared"}