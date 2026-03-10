import json
import re

# 提取字符串中最后一个数值（不依赖固定文本）
def extract_last_number(text):
    # 匹配所有浮点数
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    return float(numbers[-1]) if numbers else None

with open('qwen2.5_eval_result.jsonl','r') as file:
    lines = file.readlines()
reerror_list = []
update_lines = []
for line in lines:
    data = json.loads(line)
    predict_value = extract_last_number(data['predict'])
    label_value = extract_last_number(data['label'])
    relative_error = abs(predict_value - label_value) / label_value
    data['relative_error'] = relative_error
    update_lines.append(json.dumps(data)+'\n')
with open('qwen2.5_eval_result.jsonl', 'w') as file:
    file.writelines(update_lines)
