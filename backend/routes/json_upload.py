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

    datetime_now = datetime.now()

    try:
        for entry in data:
            logger.warning(f"Processing entry2: {entry}")
            if "ori" not in entry or "trans" not in entry:
                logger.warning(f"Skipping invalid entry2: {entry}")
                continue  # Skip invalid entry
            word = entry["ori"]
            translation = entry["trans"]
            tags = entry.get("tags", None)
            remark = entry.get("remark", {})

            new_word = Wordplay(
                word=word,
                translation=translation,
                tags=tags,
                datetime=datetime_now,
                remark=remark
            )
            session.add(new_word)
        session.commit()
        logger.info("Data imported successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting data into database: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    return {"status": "success", "detail": "Data imported successfully"}