import json
from collections import defaultdict

def find_duplicates(json_file):
    # Load the JSON data from the file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Dictionary to hold lists of items for each word
    word_dict = defaultdict(list)

    # Populate the dictionary with items grouped by word
    for item in data:
        word_dict[item['word']].append(item)

    # Filter out the words that have duplicates
    duplicates = {word: items for word, items in word_dict.items() if len(items) > 1}

    return duplicates

# Usage
duplicates = find_duplicates('busuu-de-a1-480-all-examples.json')

# Print the duplicates
for word, items in duplicates.items():
    print(f"Word: {word}")
    for item in items:
        print(json.dumps(item, ensure_ascii=False, indent=4))
    print("\n")

# Save duplicates to a file
with open('duplicates.json', 'w', encoding='utf-8') as output_file:
    json.dump(duplicates, output_file, ensure_ascii=False, indent=4)
