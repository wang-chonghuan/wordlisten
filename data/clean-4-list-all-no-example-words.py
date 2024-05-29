import json

# 读取 JSON 文件
with open('busuu-de-a1-480.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 筛选 example 为空字符串的字典
no_example_items = [item for item in data if item.get('example', '') == '']

# 将筛选结果写入新的 JSON 文件
with open('busuu-de-a1-480-no-example-items.json', 'w', encoding='utf-8') as output_file:
    json.dump(no_example_items, output_file, ensure_ascii=False, indent=4)

print("处理完成，已生成 busuu-de-a1-480-no-example-items.json 文件。")
