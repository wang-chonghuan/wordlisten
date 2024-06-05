from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
import os
import json
import genanki
from pydub import AudioSegment
from database import get_session
from models import Wordplay
import random
import io
import logging
from datetime import datetime

# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter()

anki_files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../data/nw', 'anki_files')
audio_files_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../data', 'audio_files')

if not os.path.exists(anki_files_path):
    os.makedirs(anki_files_path)

def build_tag_filter_expression(tag_list):
    # Build filter expression for SQLModel ORM
    return [Wordplay.tags.contains(tag) for tag in tag_list]

# Define the model for Anki cards
model = genanki.Model(
    1607392319,
    'Enhanced Model',
    fields=[
        {'name': 'Sentence'},
        {'name': 'Translation'},
        {'name': 'Analysis'},
        {'name': 'Audio'},
        {'name': 'Tags'},
        {'name': 'Datetime'},
        {'name': 'ID'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Translation}}<br><br>{{type:Sentence}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Sentence}}<br><br>{{Analysis}}<br>{{Audio}}<br><br>Tags: {{Tags}}<br>Datetime: {{Datetime}}<br>ID: {{ID}}',
        },
    ],
    css='.card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }',
)

# Fixed ID for the deck
DECK_ID = 2059400110

@router.get("/generate_anki/", response_model=dict)
async def generate_anki(tags: str, session: Session = Depends(get_session)):
    tag_list = tags.split(',')

    # Query to filter words by tags
    tag_filter_expression = build_tag_filter_expression(tag_list)
    statement = select(Wordplay).where(*tag_filter_expression)
    words = session.exec(statement).all()

    if not words:
        raise HTTPException(status_code=404, detail="No matching words found")

    # Create a new Anki deck with a fixed ID
    deck = genanki.Deck(
        DECK_ID,  # Fixed ID for the deck
        'Nicos-Weg-1'
    )

    audio_files = []

    for word in words:
        audio_filename = f"{word.id}.mp3"
        audio_file_path = os.path.join(audio_files_path, audio_filename)

        # Check if the audio file exists
        if os.path.exists(audio_file_path):
            audio_files.append(audio_file_path)
            audio_field = f"[sound:{audio_filename}]"
        else:
            audio_field = ""

        note = genanki.Note(
            model=model,
            fields=[
                word.sentence,
                word.translation,
                word.analysis,
                audio_field,
                word.tags,
                word.datetime.isoformat() if word.datetime else "",
                str(word.id)
            ]
        )
        deck.add_note(note)

    # Generate the package filename based on tags and current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    package_filename = f"{'_'.join(tag_list)}-{timestamp}.apkg"
    package_path = os.path.join(anki_files_path, package_filename)

    # Save the deck to an .apkg file
    package = genanki.Package(deck)
    package.media_files = audio_files
    package.write_to_file(package_path)

    return {"status": "success", "detail": "Anki package generated successfully.", "package_path": package_path}
