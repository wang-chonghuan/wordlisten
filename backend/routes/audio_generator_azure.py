from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig, ResultReason, CancellationReason
from pydub import AudioSegment
import os
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

# Helper function to convert text to speech using Azure Cognitive Services
def azure_text_to_speech(text, lang='de'):
    speech_key = "c4db500f6e5e4c6ca166d8fd507b6e34"  # 替换为你的 Azure 订阅密钥
    service_region = "germanywestcentral"  # 替换为你的服务区域
    
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = AudioConfig(filename="temp.wav")

    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == CancellationReason.Error:
            logger.error(f"Error details: {cancellation_details.error_details}")
        raise HTTPException(status_code=500, detail="Failed to generate speech")

    # 使用上下文管理器处理音频文件
    with open("temp.wav", "rb") as audio_file:
        audio = AudioSegment.from_file(audio_file, format="wav")
    
    return audio

# Route to generate audio for records with empty audio fields using Azure Cognitive Services
@router.post("/generate_audio_azure/")
async def generate_audio_azure(session: Session = Depends(get_session)):
    try:
        statement = select(Wordplay).where(Wordplay.audio == None)
        results = session.exec(statement).all()
        for record in results:
            audio = azure_text_to_speech(record.word)
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
    return {"status": "success", "detail": "Audio generated and saved for records with empty audio fields using Azure Cognitive Services."}
