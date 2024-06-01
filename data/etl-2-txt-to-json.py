import json
import random
from datetime import datetime

def determine_tags(german_sentence, base_tag):
    # Determine tags based on the given conditions
    if len(german_sentence.split()) <= 2 or '/' in german_sentence or '(' in german_sentence or ')' in german_sentence:
        return f"{base_tag},word"
    else:
        return f"{base_tag},sentence"

def process_file(input_filename, base_tag):
    output_filename = 'output-etl-2-' + input_filename.replace('output-etl-1-', '').replace('.txt', '.json')
    
    with open(input_filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split content by double newlines to get pairs of lines
    segments = content.split('\n\n')
    items = []
    id_counter = 1

    for segment in segments:
        lines = segment.strip().split('\n')
        if len(lines) == 2:
            german_sentence = lines[0].strip()
            english_translation = lines[1].strip()
            tags = determine_tags(german_sentence, base_tag)
            item = {
                "id": id_counter,
                "words": german_sentence,
                "translation": english_translation,
                "tags": tags,
                "datetime": datetime.now().strftime("%Y%m%d%H%M%S")
            }
            items.append(item)
            id_counter += 1

    # Shuffle the items NOT suffle here
    #random.shuffle(items)

    # Reassign IDs
    for idx, item in enumerate(items):
        item["id"] = idx + 1

    # Write the items to a JSON file
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(items, json_file, ensure_ascii=False, indent=4)

# Get the base tag from the user
base_tag = input("Please input words category tag: ")

# Replace 'etl-1-output-busuu-de-a1-480.txt' with the path to your actual file if different
process_file('output-etl-1-words.txt', base_tag)
