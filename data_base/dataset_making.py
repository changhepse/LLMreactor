from split_data import split_data
from data.data_1 import samples
#
# # 设置训练集比例 (0.0 - 1.0)
# TRAIN_RATIO = 0.9  # 80% 训练集, 20% 验证集
#
# # 分割数据集
# train_count, val_count = split_data(
#     samples,
#     train_ratio=TRAIN_RATIO,
#     output_train="data/virtual_train.json",
#     output_val="data/virtual_val.json"
# )
# print(f"数据集分割完成!")
# print(f"训练集样本数: {train_count}")
# print(f"验证集样本数: {val_count}")

# 设置训练集比例 (0.0 - 1.0)
TRAIN_RATIO = 0.9  # 80% 训练集, 20% 验证集

# 分割数据集
train_count, val_count = split_data(
    samples,
    train_ratio=TRAIN_RATIO,
    output_train="data/real_train.json",
    output_val="data/real_val.json"
)
print(f"数据集分割完成!")
print(f"训练集样本数: {train_count}")
print(f"验证集样本数: {val_count}")