import json
import datetime

input_filename = "filtered_busuu-de-a1-480.txt"
output_filename = "busuu-de-a1-480.json"

# 读取文件内容
with open(input_filename, "r", encoding="utf-8") as file:
    lines = file.readlines()

# 处理文件内容
entries = []
entry = {}
current_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
entry_id = 1

for line in lines:
    stripped_line = line.strip()
    if stripped_line:
        if "word" not in entry:
            entry["word"] = stripped_line
        elif "word-translation" not in entry:
            entry["word-translation"] = stripped_line
        elif "example" not in entry:
            entry["example"] = stripped_line
        elif "example-translation" not in entry:
            entry["example-translation"] = stripped_line
    else:
        if entry:
            entry_with_id = {
                "id": entry_id,
                "word": entry.get("word", ""),
                "word-translation": entry.get("word-translation", ""),
                "example": entry.get("example", ""),
                "example-translation": entry.get("example-translation", ""),
                "date": current_date
            }
            entries.append(entry_with_id)
            entry = {}
            entry_id += 1

# 最后一个词条（如果存在）
if entry:
    entry_with_id = {
        "id": entry_id,
        "word": entry.get("word", ""),
        "word-translation": entry.get("word-translation", ""),
        "example": entry.get("example", ""),
        "example-translation": entry.get("example-translation", ""),
        "date": current_date
    }
    entries.append(entry_with_id)

# 输出JSON文件
with open(output_filename, "w", encoding="utf-8") as outfile:
    json.dump(entries, outfile, ensure_ascii=False, indent=4)

print(f"处理后的JSON文件已保存为 {output_filename}")
