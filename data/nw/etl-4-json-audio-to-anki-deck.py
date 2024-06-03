import json
import genanki
import os

def create_anki_deck(input_filename, output_filename, audio_files_dir):
    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error reading file: {e}")
        return

    # Create a unique model for the cards
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
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Translation}}<br><br>{{type:Sentence}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Sentence}}<br><br>{{Analysis}}<br>{{Audio}}<br><br>Tags: {{Tags}}<br>Datetime: {{Datetime}}',
            },
        ])

    # Create a new deck
    deck = genanki.Deck(
        2059400110,
        'nw-1'
    )

    # Add cards to the deck
    for entry in data:
        audio_filename = os.path.join(audio_files_dir, f"{entry['id']}.mp3")
        if os.path.exists(audio_filename):
            audio_field = f"[sound:{entry['id']}.mp3]"
        else:
            audio_field = ""

        note = genanki.Note(
            model=model,
            fields=[entry['sentence'], entry['translation'], entry['analysis'], audio_field, entry['tags'], entry['datetime']]
        )
        deck.add_note(note)

    # Save the deck to an .apkg file
    package = genanki.Package(deck)

    # Add audio files to the package
    audio_files = [os.path.join(audio_files_dir, f"{entry['id']}.mp3") for entry in data if os.path.exists(os.path.join(audio_files_dir, f"{entry['id']}.mp3"))]
    package.media_files = audio_files

    package.write_to_file(output_filename)
    print(f"Anki deck saved to {output_filename}")

# Replace 'etl-output-2.json' with the actual path to your input JSON file if different
# Replace 'output-anki-deck.apkg' with the desired path for your output Anki deck file
# Replace 'audio' with the actual path to your audio files directory if different
create_anki_deck('etl-output-2.json', 'output-anki-deck.apkg', 'audio')
