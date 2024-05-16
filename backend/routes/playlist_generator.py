from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from gtts import gTTS
from pydub import AudioSegment
import os
from typing import List
from models import WordIdList, Wordplay
from database import get_session
import logging

router = APIRouter()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 确保音频文件目录存在
audio_files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'audio_files')
if not os.path.exists(audio_files_path):
    os.makedirs(audio_files_path)

# Helper function to generate silence
def generate_silence(duration_ms):
    return AudioSegment.silent(duration=duration_ms)

# Helper function to convert text to speech
def text_to_speech(text, lang='de'):
    tts = gTTS(text=text, lang=lang)
    tts.save("temp.mp3")
    audio = AudioSegment.from_mp3("temp.mp3")
    os.remove("temp.mp3")
    return audio

# Helper function to convert translation to speech
def translation_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("temp.mp3")
    audio = AudioSegment.from_mp3("temp.mp3")
    os.remove("temp.mp3")
    return audio

@router.post("/generate_custom_audio/")
async def generate_custom_audio(word_id_list: WordIdList, session: Session = Depends(get_session)):
    try:
        # 提取 word_ids
        word_ids = word_id_list.word_ids
        # 打印完整的 word_ids 列表
        logger.error(f"word_ids: {word_ids}")
        
        # 查询对应的 Wordplay 记录
        statement = select(Wordplay).where(Wordplay.id.in_(word_ids))
        results = session.exec(statement).all()

        # 初始化空的 AudioSegment 对象
        combined_audio = AudioSegment.empty()

        for record in results:
            german_audio = text_to_speech(record.word, lang='de')
            english_audio = translation_to_speech(record.translation, lang='en')

            # 拼接：德语 -> 1秒停顿 -> 德语 -> 1秒停顿 -> 英语 -> 1秒停顿
            combined_audio += german_audio + generate_silence(1000) + english_audio + generate_silence(1000) + german_audio + generate_silence(1000)

        # 生成文件名：YY-MM-DD-HH-MM-SS
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        output_audio_filename = os.path.join(audio_files_path, f"{current_datetime}.mp3")

        # 保存最终的音频文件
        combined_audio.export(output_audio_filename, format="mp3")

        logger.info(f"Audio file saved: {output_audio_filename}")

        return {"status": "success", "detail": f"Audio file generated: {output_audio_filename}"}
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
