from fastapi import FastAPI
from app.db import engine
from app.models import Base
from contextlib import asynccontextmanager
import logging

app = FastAPI(title="Weather Forecast")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables created.")
    
@app.get("/")
async def read_root():
    return {"message": "init main"}