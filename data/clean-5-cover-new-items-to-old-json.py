import json

def update_json(json1, json2):
    # Load the JSON data from the files
    with open(json1, 'r', encoding='utf-8') as file1, open(json2, 'r', encoding='utf-8') as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)

    # Create a dictionary for quick lookup by id from the second JSON data
    data2_dict = {item['id']: item for item in data2}

    # Update the first JSON data with the values from the second JSON data
    for item in data1:
        if item['id'] in data2_dict:
            item.update(data2_dict[item['id']])

    # Save the updated JSON data back to a file
    with open('busuu-de-a1-480-all-examples.json', 'w', encoding='utf-8') as updated_file:
        json.dump(data1, updated_file, ensure_ascii=False, indent=4)

# Usage
update_json('busuu-de-a1-480.json', 'busuu-de-a1-480-no-example-items.json')
