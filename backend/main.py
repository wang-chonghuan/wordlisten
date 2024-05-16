from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from sqlmodel import SQLModel, Field, create_engine, select
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import JSON, Column
import databases
from contextlib import asynccontextmanager
import json
from database import engine, get_session

from routes.audio_generator import router as audio_generator_router
from routes.json_upload import router as json_upload_router
from routes.words_crud import router as words_crud_router
from routes.playlist_generator import router as playlist_generator_router

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 生命周期事件处理
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine, checkfirst=True)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

# 挂载路由
app.include_router(words_crud_router)
app.include_router(json_upload_router)
app.include_router(audio_generator_router)
app.include_router(playlist_generator_router)


# 运行应用
if __name__ == "__main__":
    logger.error("__main__")
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
