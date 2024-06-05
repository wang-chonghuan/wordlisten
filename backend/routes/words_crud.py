import base64
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import APIRouter, Depends, FastAPI, File, UploadFile, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import JSON, Column
from sqlalchemy import and_
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
        sentence=word.sentence,
        translation=word.translation,
        analysis=word.analysis,
        tags=word.tags,
        datetime=word.datetime,
        remark=word.remark,
        audio=base64.b64encode(word.audio).decode('utf-8') if word.audio else None
    )
    
    return word_detail

# Helper function to build tag filtering expression
def build_tag_filter_expression(tag_list):
    return and_(*[Wordplay.tags.like(f"%{tag}%") for tag in tag_list])

# New endpoint to get words by tags
@router.get("/words", response_model=list[WordplayDetail])
async def read_words_by_tags(tags: str, session: Session = Depends(get_session)):
    tag_list = tags.split(',')

    # Query to filter words by tags
    tag_filter_expression = build_tag_filter_expression(tag_list)
    statement = select(Wordplay).where(tag_filter_expression)
    words = session.exec(statement).all()

    matching_words = []
    for word in words:
        word_detail = WordplayDetail(
            id=word.id,
            sentence=word.sentence,
            translation=word.translation,
            analysis=word.analysis,
            tags=word.tags,
            datetime=word.datetime,
            remark=word.remark,
            audio=base64.b64encode(word.audio).decode('utf-8') if word.audio else None
        )
        matching_words.append(word_detail)
    
    if not matching_words:
        raise HTTPException(status_code=404, detail="No matching words found")

    return matching_words