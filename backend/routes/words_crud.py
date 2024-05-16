import base64
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import APIRouter, Depends, FastAPI, File, UploadFile, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import JSON, Column
import databases
from contextlib import asynccontextmanager
import json
from database import engine, get_session

from models import Wordplay, WordplayDetail, WordplayRead

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 增加单词条目
@router.post("/words/", response_model=Wordplay)
async def create_word(word: Wordplay, session: Session = Depends(get_session)):
    session.add(word)
    session.commit()
    session.refresh(word)
    return word

# 上传音频文件
@router.post("/upload_audio/")
async def upload_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    return {"filename": file.filename, "content_type": file.content_type, "size": len(audio_bytes)}

# 获取所有单词条目（不包括音频字段）
@router.get("/words/", response_model=list[WordplayRead])
async def read_words(session: Session = Depends(get_session)):
    statement = select(Wordplay)
    results = session.exec(statement).all()
    return results

# 获取单个单词条目（包括音频字段）
@router.get("/word/{word_id}", response_model=WordplayDetail)
async def read_word(word_id: int, session: Session = Depends(get_session)):
    word = session.get(Wordplay, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # 使用新的方式构建WordplayDetail对象，直接分配字段
    word_detail = WordplayDetail(
        id=word.id,
        word=word.word,
        translation=word.translation,
        flag=word.flag,
        datetime=word.datetime,
        remark=word.remark,
        audio=base64.b64encode(word.audio).decode('utf-8') if word.audio else None
    )
    
    return word_detail
