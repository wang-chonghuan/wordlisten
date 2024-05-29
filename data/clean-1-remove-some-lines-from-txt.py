# 定义文件名
input_filename = "busuu-de-a1-480.txt"
output_filename = "filtered_" + input_filename

# 需要移除的单词
words_to_remove = {"Strong", "Example", "Play"}

# 读取文件内容
with open(input_filename, "r", encoding="utf-8") as file:
    lines = file.readlines()

# 过滤行
filtered_lines = [line for line in lines if line.strip() not in words_to_remove]

# 将过滤后的内容写回文件
with open(output_filename, "w", encoding="utf-8") as file:
    file.writelines(filtered_lines)

print(f"过滤后的文件已保存为 {output_filename}")
