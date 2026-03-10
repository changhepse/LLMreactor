import json
import random

def split_data(input_data, train_ratio=0.8, output_train="train.jsonl", output_val="val.jsonl"):
    """
    将数据集分割为训练集和验证集

    参数:
    input_data -- 包含所有样本的列表
    train_ratio -- 训练集比例 (0-1之间的浮点数)
    output_train -- 训练集输出文件名
    output_val -- 验证集输出文件名
    """
    # 打乱数据以确保随机分布
    random.shuffle(input_data)

    # 计算分割点
    split_index = int(len(input_data) * train_ratio)

    # 分割数据集
    train_set = input_data[:split_index]
    val_set = input_data[split_index:]

    # 保存训练集
    with open(output_train, 'w', encoding='utf-8') as f:
        f.write("[\n")
        for sample in train_set:
            json_sample = json.dumps(sample, ensure_ascii=False)
            f.write(json_sample + ',\n')
        f.write("]")

    # 保存验证集
    with open(output_val, 'w', encoding='utf-8') as f:
        f.write("[\n")
        for sample in val_set:
            json_line = json.dumps(sample, ensure_ascii=False)
            f.write(json_line + ',\n')
        f.write("]")

    return len(train_set), len(val_set)
#
# # 设置训练集比例 (0.0 - 1.0)
# TRAIN_RATIO = 0.8  # 80% 训练集, 20% 验证集
#
# # 分割数据集
# train_count, val_count = split_data(
#     samples,
#     train_ratio=TRAIN_RATIO,
#     output_train="train.jsonl",
#     output_val="val.jsonl"
# )
#
# print(f"数据集分割完成!")
# print(f"训练集样本数: {train_count}")
# print(f"验证集样本数: {val_count}")
# print(f"训练集比例: {TRAIN_RATIO * 100:.0f}%")