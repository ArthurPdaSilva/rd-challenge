from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("API está iniciando...")
    await init_db()
    yield
    print("API está sendo encerrada...")


app = FastAPI(
    title="RD Desafio API",
    description="API para controlar sondas em uma malha 2D.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
