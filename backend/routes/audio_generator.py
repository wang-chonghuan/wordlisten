from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
import os
import json
import logging
from models import Wordplay
from database import get_session

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 确保音频文件目录存在
audio_files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'audio_files')
if not os.path.exists(audio_files_path):
    os.makedirs(audio_files_path)

# Helper function to convert text to speech
def text_to_speech(text, lang='de'):
    tts = gTTS(text=text, lang=lang)
    tts.save("temp.mp3")
    audio = AudioSegment.from_mp3("temp.mp3")
    os.remove("temp.mp3")
    return audio

# Route to generate audio for records with empty audio fields
@router.post("/generate_audio/")
async def generate_audio(session: Session = Depends(get_session)):
    try:
        statement = select(Wordplay)#.where(Wordplay.audio == None)
        results = session.exec(statement).all()
        for record in results:
            audio = text_to_speech(record.word)
            audio_file_path = os.path.join(audio_files_path, f"{record.id}.mp3")
            audio.export(audio_file_path, format="mp3")
            logger.info(f"Audio file saved: {audio_file_path}")

            # 读取音频文件内容
            with open(audio_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
                record.audio = audio_data

            # 更新数据库
            session.add(record)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    return {"status": "success", "detail": "Audio generated and saved for records with empty audio fields."}
