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
from pydantic import BaseModel, ValidationError
from models import WordJson, Wordplay
from database import engine, get_session

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Route to process JSON file and insert data into the database
@router.post("/import_json/")
async def import_json(file: UploadFile = File(...), session: Session = Depends(get_session)):
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

    try:
        for entry in data:
            logger.warning(f"Processing entry: {entry}")
            try:
                word_entry = WordJson(**entry)
            except ValidationError as e:
                logger.warning(f"Skipping invalid entry: {entry} - Error: {e}")
                continue  # Skip invalid entry

            datetime_obj = datetime.strptime(word_entry.datetime, "%Y%m%d%H%M%S")

            new_word = Wordplay(
                id=word_entry.id,
                words=word_entry.words,
                translation=word_entry.translation,
                tags=word_entry.tags,
                datetime=datetime_obj
            )
            session.add(new_word)

        session.commit()
        logger.info("Data imported successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting data into database: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    return {"status": "success", "detail": "Data imported successfully"}
