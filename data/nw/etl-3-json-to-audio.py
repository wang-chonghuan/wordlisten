import json
import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig, ResultReason, CancellationReason
from pydub import AudioSegment
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 确保音频文件目录存在
audio_files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'audio')
if not os.path.exists(audio_files_path):
    os.makedirs(audio_files_path)

# Helper function to convert text to speech using Azure Cognitive Services
def azure_text_to_speech(text, lang='de'):
    speech_key = "c4db500f6e5e4c6ca166d8fd507b6e34"  # 替换为你的 Azure 订阅密钥
    service_region = "germanywestcentral"  # 替换为你的服务区域
    
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "de-DE-KatjaNeural"  # 设置语音为 Katja

    audio_config = AudioConfig(filename="temp.wav")

    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == CancellationReason.Error:
            logger.error(f"Error details: {cancellation_details.error_details}")
        raise Exception("Failed to generate speech")

    # 使用上下文管理器处理音频文件
    with open("temp.wav", "rb") as audio_file:
        audio = AudioSegment.from_file(audio_file, format="wav")
    
    return audio

# 读取JSON文件并生成音频
def generate_audio_from_json(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        text = entry['sentence']
        audio = azure_text_to_speech(text)
        audio_file_path = os.path.join(audio_files_path, f"{entry['id']}.mp3")
        audio.export(audio_file_path, format="mp3")
        logger.info(f"Audio file saved: {audio_file_path}")

if __name__ == "__main__":
    input_json_file = 'etl-output-2.json'
    generate_audio_from_json(input_json_file)
