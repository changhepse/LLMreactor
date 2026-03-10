import json
import csv

# 打开JSON文件并加载数据
with open('qwen2.5_eval_result.jsonl', 'r', encoding='utf-8') as file:
    data_list = []
    i=0
    for line in file.readlines():
        data_list.append(json.loads(line))

# 获取列名
columns = list(data_list[0].keys())
print(columns)
# 创建CSV文件，并写入列名

with open('qwen2.5_eval_result.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(columns)
    # 写入JSON数据到CSV
    for item in data_list:
        row = list(item.values())
        csv_writer.writerow(row)

print("转换完成")