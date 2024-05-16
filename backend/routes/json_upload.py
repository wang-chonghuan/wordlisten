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
from models import Wordplay
from database import engine, get_session

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Route to process JSON file and insert data into the database
@router.post("/import_json/")
async def import_json(file: UploadFile = File(...), session: Session = Depends(get_session)):
    logger = logging.getLogger(__name__)
    logger.info("Received file upload request.")
    try:
        file_contents = await file.read()
        data = json.loads(file_contents)
        logger.info("Successfully read and parsed JSON file.")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {e}")
    except Exception as e:
        logger.error(f"Unexpected error reading file: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    datetime_now = datetime.now()

    try:
        for entry in data:
            if len(entry) != 3:
                logger.warning(f"Skipping invalid entry: {entry}")
                continue  # 跳过无效条目
            word = entry[1]
            translation = entry[2]
            new_word = Wordplay(
                word=word,
                translation=translation,
                datetime=datetime_now,
                audio=None  # 明确设置 audio 字段为 None
            )
            session.add(new_word)
        session.commit()
        logger.info("Data imported successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting data into database: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    return {"status": "success", "detail": "Data imported successfully"}