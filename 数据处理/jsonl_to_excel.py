import json
import pandas as pd

# 定义要处理的 JSONL 文件列表
jsonl_files = {
    # 'real_qwen2.5_Omni': 'real_qwen2.5_Omni_eval_result.jsonl',  # 键是工作表名称，值是文件路径
    # 'real_qwen2.5_math': 'real_qwen2.5_math_eval_result.jsonl',
    # 'real_llama3.2':'real_llama3.2_eval_result.jsonl',
    # 'real_gemma3':'real_gemma3_eval_result.jsonl',
    # 'real_deepseek_r1':'real_DeepSeek-R1_eval_result.jsonl',
    # 'original_virtual_DeepSeek-R1':'original_virtual_deepseek-r1_eval_result.jsonl',
    # 'original_virtual_gemma3':'original_virtual_gemma3_eval_result.jsonl',
    # 'original_virtual_llama3.2':'original_virtual_llama3.2_eval_result.jsonl',
    # 'original_virtual_qwen2.5_math':'original_virtual_qwen2.5_math_eval_result.jsonl',
    # 'original_virtual_qwen2.5_Omni':'original_virtual_qwen2.5_Omni_eval_result.jsonl',
    # 'original_real_deepseek-r1':'original_real_deepseek-r1_eval_result.jsonl',
    # 'original_real_gemma3': 'original_real_gemma3_eval_result.jsonl',
    # 'original_real_llama3.2': 'original_real_llama3.2_eval_result.jsonl',
    # 'original_real_qwen2.5_math': 'original_real_qwen2.5_math_eval_result.jsonl',
    # 'original_real_qwen2.5_Omni': 'original_real_qwen2.5_Omni_eval_result.jsonl',
    # 'production_eval_deepseek-r1':'deepseek-r1_production.jsonl',
    # 'production_eval_gemma3':'gemma3_production.jsonl',
    # 'production_eval_llama3.2':'llama3.2_production.jsonl',
    # 'production_eval_qwen2.5_math':'qwen2.5_math_production.jsonl',
    # 'production_eval_qwen2.5_omni':'qwen2.5_omni_production.jsonl',
    # 'generalization_deepseek-r1':'泛化测试/deepseek/generated_predictions.jsonl',
    # 'generalization_qwen-omni':'泛化测试/qwen-omni/generated_predictions.jsonl',
    # 'generalization_qwen-math':'泛化测试/qwen-math/generated_predictions.jsonl',
    # 'generalization_deepseek-r1_result':'泛化测试/generalization_deepseek_result.jsonl',
    # 'generalization_qwen-omni_result':'泛化测试/generalization_qwen-omni_result.jsonl',
    # 'generalization_qwen-math_result':'泛化测试/generalization_qwen-math_result.jsonl',
    # 'OOD_deepseek-r1_result': '泛化测试/deepseek_OOD.jsonl',
    # 'OOD_qwen-omni_result': '泛化测试/generalization_qwen-omni_result.jsonl',
    # 'OOD_qwen-math_result': '泛化测试/generalization_qwen-math_result.jsonl',
    # 'SBA_deepseek-r1_result': '泛化测试/SBA_deepseek-r1_result.jsonl',
    'SBA_deepseek-r1_result': '泛化测试/deepseek-r1_SBA.jsonl',
    # 可以继续添加更多
}

# 使用 pandas 的 ExcelWriter
with pd.ExcelWriter('泛化测试/SBA_result_1.xlsx', engine='openpyxl') as writer:
    for sheet_name, file_path in jsonl_files.items():
        try:
            # 读取 JSONL 文件
            data_list = []
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    data_list.append(json.loads(line.strip()))

            # 创建 DataFrame 并写入 Excel
            df = pd.DataFrame(data_list)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"已处理文件: {file_path} -> 工作表: {sheet_name}")

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

print("转换完成")