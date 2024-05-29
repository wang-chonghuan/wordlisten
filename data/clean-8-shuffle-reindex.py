import json
import random

def shuffle_and_reindex(json_file, output_file):
    # Load the JSON data from the file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Shuffle the data
    random.shuffle(data)

    # Reindex the data with id starting from 1
    for new_id, item in enumerate(data, start=1):
        item['id'] = new_id

    # Save the shuffled and reindexed data back to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)

# Usage
shuffle_and_reindex('busuu-de-a1-480-all-examples-no-duplicates.json', 'busuu-de-a1-480-final-shuffled.json')
