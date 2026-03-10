# LLMreactor

本项目是基于 `LLaMA-Factory` 的本地实验仓库，包含训练/推理命令示例与自定义的反应工程数据生成脚本。

## 项目结构

```text
LLMreactor/
├── LLaMA-Factory/   # 上游框架代码
├── data_base/       # 反应工程相关数据生成与求解脚本
├── 数据处理/         # 结果整理与格式转换脚本
├── result_eval/     # 评测脚本（BERTScore/相对误差/token统计）
├── instruction.py       # 模型下载与测试命令记录
└── README.md
```

## data_base 程序作用

`data_base` 目录主要用于构造化工反应器计算任务数据（用于模型训练/验证）：

- `data_base/PFR_data.py`：核心求解器，按反应器类型（BR/PFR/CSTR）和动力学参数计算停留时间/体积等结果。
- `data_base/data_test_1.py`：批量随机生成“题目-解答”样本，并写入 `data/data_1.py` 等数据文件。
- `data_base/real_reaction.py`：基于真实反应场景生成多类数据集（如皂化、酯化、WGS 泛化数据）。
- `data_base/real_reaction_test.py`：固定参数/区间下的测试数据生成脚本，便于对比和验证。
- `data_base/split_data.py`：将样本按比例切分为训练集和验证集。
- `data_base/dataset_making.py`：组合调用切分流程，生成训练/验证数据文件。
- `data_base/data/`：已生成的数据文件目录（json/jsonl）。

## 数据处理 程序作用

`数据处理` 目录主要用于结果文件整理和导出：

- `数据处理/jsonl_to_excel.py`：将多个 `.jsonl` 结果文件批量转换为 Excel 工作表，便于人工对比。
- `数据处理/get_value.py`：将 `.jsonl` 转为 `.csv`，用于后续统计或可视化处理。
- `数据处理/泛化测试/`：保存泛化测试相关的输入、预测结果、日志与配置文件。
- `数据处理/*_eval_result.jsonl`、`*_production.jsonl`：不同模型/场景的评测结果与生产场景输出样本。

## result_eval 程序作用

`result_eval` 目录主要用于自动化评估：

- `result_eval/BERTScore.py`：对预测结果计算 BERTScore（P/R/F1），并回写到评测结果文件。
- `result_eval/relative_error.py`：从文本中提取数值并计算相对误差，回写到结果文件。
- `result_eval/caculate_token.py`：加载 tokenizer 统计输出 token 数，并写入 `num_token计算结果.json`。
- `result_eval/test_json/`：待评测预测文件。
- `result_eval/test_result/`：评测后结果文件。

备注：由于部分模型生成内容未完全按预期格式输出，`result_eval/relative_error.py` 提取数值时会产生错误；因此 MARE 最终采用 Excel 统计并人工核查得到，实际未使用该脚本结果。

## 模型文件说明

由于模型体积较大，本仓库**未上传模型权重文件**。

模型下载指令已整理在 `测试mat.py` 中，可按其中命令下载到本地 `models` 目录后再进行测试。

另外，`result_eval/BERTScore.py` 使用 `bert-large-uncased` 作为评分模型，该模型也需要自行下载（首次运行通常会自动从 Hugging Face 拉取，或手动预下载后离线使用）。

## 常用命令

以下命令在 `LLaMA-Factory` 目录下执行：

```bash
# 查看帮助
llamafactory-cli help

# 训练
llamafactory-cli train examples/train_lora/llama3_lora_sft.yaml

# 命令行聊天
llamafactory-cli chat examples/inference/llama3_lora_sft.yaml

# 导出模型
llamafactory-cli export examples/merge_lora/llama3_lora_sft.yaml

# 启动 Web UI
llamafactory-cli webui

# 启动 OpenAI 风格 API（示例）
API_PORT=8000 llamafactory-cli api examples/inference/llama3.yaml infer_backend=vllm vllm_enforce_eager=true
```

## 上游文档

- 中文文档入口：`LLaMA-Factory/README_zh.md`
- 英文文档入口：`LLaMA-Factory/README.md`
- 在线文档：https://llamafactory.readthedocs.io/zh-cn/latest/
