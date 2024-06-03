import json
from datetime import datetime

# 定义文件路径
input_file = 'etl-output-1.json'
output_file = 'etl-output-2.json'

# 读取输入文件内容
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提示用户输入tags
tags = input("Please enter tags for the entries: ")

# 生成输出内容
output_data = []
for idx, entry in enumerate(data, start=1):
    entry['id'] = idx
    entry['tags'] = tags
    entry['datetime'] = datetime.now().strftime('%Y%m%d%H%M%S')
    output_data.append(entry)

# 写入输出文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"Output written to {output_file}")
