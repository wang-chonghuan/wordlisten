import json

def remove_duplicates(json_file, output_file):
    # Load the JSON data from the file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Dictionary to hold the first occurrence of each word
    unique_items = {}
    
    # Populate the dictionary with the first occurrence of each word
    for item in data:
        word = item['word']
        if word not in unique_items:
            unique_items[word] = item

    # Convert the dictionary values back to a list
    unique_data = list(unique_items.values())

    # Save the unique items back to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(unique_data, output_file, ensure_ascii=False, indent=4)

# Usage
remove_duplicates('busuu-de-a1-480-all-examples.json', 'busuu-de-a1-480-all-examples-no-duplicates.json')
