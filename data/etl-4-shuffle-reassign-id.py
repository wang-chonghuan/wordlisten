import json
import random

def shuffle_and_reassign_ids(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error reading file: {e}")
        return

    # Shuffle the items
    random.shuffle(data)

    # Reassign IDs
    for idx, entry in enumerate(data):
        entry["id"] = idx + 1

    # Save the shuffled and reassigned data to a new JSON file
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Shuffled and reassigned data saved to {output_filename}")

# Replace 'output-etl-3-words.json' with the actual path to your input JSON file if different
# Replace 'output-etl-4-words.json' with the desired path for your output JSON file
shuffle_and_reassign_ids('output-etl-3-words.json', 'output-etl-4-words.json')
