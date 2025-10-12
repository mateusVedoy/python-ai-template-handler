from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

from src.application import controller

load_dotenv()

app = FastAPI()

app.include_router(controller.router)

origins = [
    "null",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Permite as origens da lista acima
    allow_credentials=True,
    # Permite todos os métodos (GET, POST, OPTIONS, etc.)
    allow_methods=["*"],
    allow_headers=["*"],            # Permite todos os cabeçalhos
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=30,  # mantém conexões abertas 30s
        limit_concurrency=10,  # opcional: limita requisições simultâneas,
        env_file=".env"
    )
