from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    await asyncio.sleep(2)  # Асинхронная задержка
    return {"message": "Вам звонит ваша МАМА! (музыка)!"}
