import json
from collections import defaultdict

def find_and_remove_duplicate_words(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error reading file: {e}")
        return

    word_dict = defaultdict(list)
    for entry in data:
        word_dict[entry['words']].append(entry)

    duplicates = {word: entries for word, entries in word_dict.items() if len(entries) > 1}

    if duplicates:
        print("Duplicate words found:")
        for word, entries in duplicates.items():
            print(f"\nWord: {word}")
            for entry in entries:
                print(json.dumps(entry, indent=4))
    else:
        print("No duplicate words found.")

    # Remove duplicates, keeping only one instance
    unique_data = []
    seen_words = set()

    for entry in data:
        word = entry['words']
        if word not in seen_words:
            unique_data.append(entry)
            seen_words.add(word)

    # Save the unique data to a new JSON file
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)

    print(f"Unique data saved to {output_filename}")

# Replace 'output-etl-2-words.json' with the actual path to your input JSON file if different
# Replace 'output-etl-3-words.json' with the desired path for your output JSON file
find_and_remove_duplicate_words('output-etl-2-words.json', 'output-etl-3-words.json')
