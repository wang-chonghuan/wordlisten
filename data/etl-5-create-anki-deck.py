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
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'Audio'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}<br><br>{{type:Answer}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br>{{Audio}}',
            },
        ])

    # Create a new deck
    deck = genanki.Deck(
        2059400110,
        'My Deck'
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
            fields=[entry['translation'], entry['words'], audio_field]
        )
        deck.add_note(note)

    # Save the deck to an .apkg file
    package = genanki.Package(deck)

    # Add audio files to the package
    audio_files = [os.path.join(audio_files_dir, f"{entry['id']}.mp3") for entry in data if os.path.exists(os.path.join(audio_files_dir, f"{entry['id']}.mp3"))]
    package.media_files = audio_files

    package.write_to_file(output_filename)
    print(f"Anki deck saved to {output_filename}")

# Replace 'output-etl-4-words.json' with the actual path to your input JSON file if different
# Replace 'output-anki-deck.apkg' with the desired path for your output Anki deck file
# Replace 'audio_files' with the actual path to your audio files directory if different
create_anki_deck('output-etl-3-words.json', 'output-anki-deck.apkg', 'audio_files')
