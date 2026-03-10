from transformers import AutoTokenizer
import json
import os


def append_dict_to_json(new_dict, filename):
    # 如果文件不存在，创建新文件并写入
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump([new_dict], file, ensure_ascii=False, indent=4)
    else:
        # 如果文件存在，读取现有数据，追加新字典，再写回
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

        # 确保数据是列表形式
        if not isinstance(existing_data, list):
            existing_data = [existing_data]

        # 追加新字典
        existing_data.append(new_dict)

        # 写回文件
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    print(f"字典已追加到 {filename}")

model_dict = {
    "qwen2.5_Omni" : {
        "model":"/home/ub/wohen/test/models/Qwen2.5-Omni-3B",
        "text_json":"real_qwen2.5_Omni_eval_result.jsonl"
    },
    "qwen2.5_math": {
        "model": "/home/ub/wohen/test/models/Qwen2.5-Math-1.5B-Instruct",
        "text_json": "real_qwen2.5_math_eval_result.jsonl"
    },
    "llama3.2": {
        "model": "/home/ub/wohen/test/models/Llama-3.2-3B",
        "text_json": "real_llama3.2_eval_result.jsonl"
    },
    "gemma3": {
        "model": "/home/ub/wohen/test/models/gemma-3-1b-it",
        "text_json": "real_gemma3_eval_result.jsonl"
    },
    "deepseek-r1": {
        "model": "/home/ub/wohen/test/models/DeepSeek-R1-Distill-Qwen-1.5B",
        "text_json": "real_DeepSeek-R1_eval_result.jsonl"
    },
    "original_qwen2.5_Omni": {
        "model": "/home/ub/wohen/test/models/Qwen2.5-Omni-3B",
        "text_json": "original_real_qwen2.5_Omni_eval_result.jsonl"
    },
    "original_qwen2.5_math": {
        "model": "/home/ub/wohen/test/models/Qwen2.5-Math-1.5B-Instruct",
        "text_json": "original_real_qwen2.5_math_eval_result.jsonl"
    },
    "original_llama3.2": {
        "model": "/home/ub/wohen/test/models/Llama-3.2-3B",
        "text_json": "original_real_llama3.2_eval_result.jsonl"
    },
    "original_gemma3": {
        "model": "/home/ub/wohen/test/models/gemma-3-1b-it",
        "text_json": "original_real_gemma3_eval_result.jsonl"
    },
    "original_deepseek-r1": {
        "model": "/home/ub/wohen/test/models/DeepSeek-R1-Distill-Qwen-1.5B",
        "text_json": "original_real_deepseek-r1_eval_result.jsonl"
    },
}
model = "original_deepseek-r1"

with open(model_dict[model]["text_json"], 'r') as file:
    lines = file.readlines()
text_list = []
for line in lines:
    line = json.loads(line)
    text_list.append(line["predict"])

print(len(text_list))
model_name = model_dict[model]["model"]
tokenizer = AutoTokenizer.from_pretrained(model_name)

# text = "这是一段测试文本"
token_list = []
for i in range(len(text_list)):
    tokens = tokenizer.tokenize(text_list[i])
    num_token = len(tokens)
    # print(num_token)
    token_list.append(num_token)
sum_tokens = sum(token_list)
print(sum_tokens)
average_tokens = sum_tokens / len(token_list)
print(average_tokens)

# 示例使用
new_dict = {"model_name": model, "sum_token": sum_tokens, "average_tokens": average_tokens}
append_dict_to_json(new_dict, "num_token计算结果.json")

print("token计算完成")
