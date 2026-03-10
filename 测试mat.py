
'''
CUDA_VISIBLE_DEVICES=0 GRADIO_SHARE=1 GRADIO_SERVER_PORT=7860 llamafactory-cli webui

'''
'''
export HF_ENDPOINT="https://hf-mirror.com"
huggingface-cli download google-bert/bert-large-uncased --local-dir ./models
huggingface-cli download openai-community/gpt2 --local-dir ./models
huggingface-cli download medmekk/llama-3.2-1b-hf --local-dir ./models/Llama-3.2-1B
huggingface-cli download Qwen/Qwen2.5-Math-1.5B-Instruct --local-dir ./models/Qwen2.5-Math-1.5B-Instruct
huggingface-cli download openai-community/gpt2-medium --local-dir ./models/openai-community-gpt2
google/gemma-3-4b-it
unsloth/Llama-3.2-3B-Instruct-bnb-4bit
huggingface-cli download unsloth/Llama-3.2-3B-Instruct-bnb-4bit --local-dir ./models/Llama-3.2-3B
huggingface-cli download google/gemma-3-1b-it --local-dir ./models/gemma-3-1b-it
'''
