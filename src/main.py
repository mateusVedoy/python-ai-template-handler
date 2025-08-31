
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

from src.application import controller

load_dotenv()

app = FastAPI()

app.include_router(controller.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=30,  # mantém conexões abertas 30s
        limit_concurrency=10,  # opcional: limita requisições simultâneas,
        env_file=".env"
    )
