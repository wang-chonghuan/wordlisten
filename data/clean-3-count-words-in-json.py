import json
import string

input_filename = "busuu-de-a1-480.json"

# 读取JSON文件
with open(input_filename, "r", encoding="utf-8") as file:
    data = json.load(file)

# 用于存储所有单词的集合（去重）
unique_words = set()

# 定义一个函数来移除标点符号并转换为小写
def clean_text(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator).lower()

# 统计所有example和word字段中的单词
for entry in data:
    word = entry.get("word", "")
    example = entry.get("example", "")
    
    # 清理文本并拆分单词
    cleaned_word = clean_text(word)
    cleaned_example = clean_text(example)
    
    # 将单词加入集合
    unique_words.update(cleaned_word.split())
    unique_words.update(cleaned_example.split())

# 去掉空字符串
unique_words.discard('')

# 输出单词总数
print(f"所有example字段和word字段中的单词总数（去重）：{len(unique_words)}")

# 打印所有单词
print("所有单词：")
print(unique_words)
