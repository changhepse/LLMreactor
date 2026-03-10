import json
import bert_score
from keras.src.legacy.backend import update
import tensorflow as tf
import re

def read_jsonl(file_path):
    """读取JSONL文件并返回所有字典组成的列表"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 解析每一行JSON数据
            data.append(json.loads(line))
    return data

def extract_last_number(text):
    # 匹配所有浮点数
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    return float(numbers[-1]) if numbers else None

def extract_last_number_2(text):
    # 匹配所有浮点数
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    return float(numbers[-2]) if numbers else None

model_dict = {
    "qwen2.5_Omni" : {
        "input_json":"test_json/qwen2.5_Omni_generated_predictions.jsonl",
        "output_json":"test_result/qwen2.5_Omni_eval_result.jsonl"
    },
    "DeepSeek-R1":{
        "input_json":"test_json/DeepSeek-R1_generated_predictions.jsonl",
        "output_json":"test_result/DeepSeek-R1_eval_result.jsonl"
    },
    "qwen2.5_math":{
        "input_json":"test_json/qwen2.5_math_generated_predictions.jsonl",
        "output_json":"test_result/qwen2.5_math_eval_result.jsonl"
    },
    "llama3.2":{
        "input_json":"test_json/llama3.2_generated_predictions.jsonl",
        "output_json":"test_result/llama3.2_eval_result.jsonl"
    },
    "gemma3":{
        "input_json":"test_json/gemma3_generated_predictions.jsonl",
        "output_json":"test_result/gemma3_eval_result.jsonl"
    },
    "real_qwen2.5_Omni": {
        "input_json": "test_json/real_qwen2.5_Omni_generated_predictions.jsonl",
        "output_json": "test_result/real_qwen2.5_Omni_eval_result.jsonl"
    },
    "real_DeepSeek-R1": {
        "input_json": "test_json/real_DeepSeek-R1_generated_predictions.jsonl",
        "output_json": "test_result/real_DeepSeek-R1_eval_result.jsonl"
    },
    "real_qwen2.5_math": {
        "input_json": "test_json/real_qwen2.5_math_generated_predictions.jsonl",
        "output_json": "test_result/real_qwen2.5_math_eval_result.jsonl"
    },
    "real_llama3.2": {
        "input_json": "test_json/real_llama3.2_generated_predictions.jsonl",
        "output_json": "test_result/real_llama3.2_eval_result.jsonl"
    },
    "real_gemma3": {
        "input_json": "test_json/real_gemma3_generated_predictions.jsonl",
        "output_json": "test_result/real_gemma3_eval_result.jsonl"
    },
    "original_virtual_qwen2.5_Omni": {
        "input_json": "test_json/original_virtual_qwen2.5_Omni_generated_predictions.jsonl",
        "output_json": "test_result/original_virtual_qwen2.5_Omni_eval_result.jsonl"
    },
    "original_virtual_DeepSeek-R1":{
        "input_json": "test_json/original_virtual_deepseek-r1_generated_predictions.jsonl",
        "output_json": "test_result/original_virtual_deepseek-r1_eval_result.jsonl"
    },
    "original_virtual_qwen2.5_math": {
        "input_json": "test_json/original_virtual_qwen2.5_math_generated_predictions.jsonl",
        "output_json": "test_result/original_virtual_qwen2.5_math_eval_result.jsonl"
    },
    "original_virtual_llama3.2": {
        "input_json": "test_json/original_virtual_llama3.2_generated_predictions.jsonl",
        "output_json": "test_result/original_virtual_llama3.2_eval_result.jsonl"
    },
    "original_virtual_gemma3": {
        "input_json": "test_json/original_virtual_gemma3_generated_predictions.jsonl",
        "output_json": "test_result/original_virtual_gemma3_eval_result.jsonl"
    },
    "original_real_qwen2.5_Omni": {
        "input_json": "test_json/original_real_qwen2.5_Omni_generated_predictions.jsonl",
        "output_json": "test_result/original_real_qwen2.5_Omni_eval_result.jsonl"
    },
    "original_real_DeepSeek-R1": {
        "input_json": "test_json/original_real_deepseek-r1_generated_predictions.jsonl",
        "output_json": "test_result/original_real_deepseek-r1_eval_result.jsonl"
    },
    "original_real_qwen2.5_math": {
        "input_json": "test_json/original_real_qwen2.5_math_generated_predictions.jsonl",
        "output_json": "test_result/original_real_qwen2.5_math_eval_result.jsonl"
    },
    "original_real_llama3.2": {
        "input_json": "test_json/original_real_llama3.2_generated_predictions.jsonl",
        "output_json": "test_result/original_real_llama3.2_eval_result.jsonl"
    },
    "original_real_gemma3": {
        "input_json": "test_json/original_real_gemma3_generated_predictions.jsonl",
        "output_json": "test_result/original_real_gemma3_eval_result.jsonl"
    },
    "generalization_deepseek": {
        "input_json": "test_json/generalization_deepseek.jsonl",
        "output_json": "test_result/generalization_deepseek_result.jsonl"
    },
    "generalization_qwen-omni": {
        "input_json": "test_json/generalization_qwen-omni.jsonl",
        "output_json": "test_result/generalization_qwen-omni_result.jsonl"
    },
    "generalization_qwen-math": {
        "input_json": "test_json/generalization_qwen-math.jsonl",
        "output_json": "test_result/generalization_qwen-math_result.jsonl"
    },
}

# 修改模型名称进行使用
model_name = "generalization_qwen-math"

# 使用示例
all_dicts = read_jsonl(model_dict[model_name]["input_json"])
print(f"共读取 {len(all_dicts)} 个字典")
prediction = []
label = []
P_list = []
R_list = []
F1_list = []
for i in all_dicts:
    # print(i)
    prediction.append(i['predict'])
    label.append(i['label'])
for i in range(len(all_dicts)):
    cand = []
    ref = []
    cand.append(prediction[i])
    ref.append(label[i])
    P, R, F1 = bert_score.score(cand, ref, lang="en", verbose=True, model_type="bert-large-uncased")
    print(f"P: {P}, R: {R}, F1: {F1}")
    P_list.append(P.item())
    R_list.append(R.item())
    F1_list.append(F1.item())

with open(model_dict[model_name]["input_json"], 'r') as file:
    lines = file.readlines()
i = 0
update_lines = []
for line in lines:
    data = json.loads(line)
    data['P'] =P_list[i]
    data['R'] =R_list[i]
    data['F1'] =F1_list[i]
    i = i+1
    update_lines.append(json.dumps(data)+'\n')
with open(model_dict[model_name]["output_json"], 'w') as file:
    file.writelines(update_lines)
print("BERTScore打分完成")

with open(model_dict[model_name]["output_json"],'r') as file:
    lines = file.readlines()
reerror_list = []
update_lines = []
for line in lines:
    data = json.loads(line)
    predict_value = extract_last_number(data['predict'])
    if predict_value is None:
        predict_value = 0
    label_value = extract_last_number(data['label'])
    relative_error = abs(predict_value - label_value) / label_value
    data['relative_error'] = relative_error
    update_lines.append(json.dumps(data)+'\n')
with open(model_dict[model_name]["output_json"], 'w') as file:
    file.writelines(update_lines)
print("相对误差计算完成")






# print(prediction)
# print(label)