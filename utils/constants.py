qwen_template = {
    "system_format": "<|im_start|>system\n{content}<|im_end|>\n",
    "user_format": "<|im_start|>user\n{content}<|im_end|>\n<|im_start|>assistant\n",
    "assistant_format": "{content}<|im_end|>\n",
    "tool_format": "{content}",
    "function_format": "{content}",
    "observation_format": "<|im_start|>tool\n{content}<|im_end|>\n<|im_start|>assistant\n",
    "system": "You are a helpful assistant.",
}

gemma_template = {
    "system_format": "<bos>",
    "user_format": "<start_of_turn>user\n{content}<end_of_turn>\n<start_of_turn>model\n",
    "assistant_format": "{content}<eos>\n",
    "tool_format": "{content}",
    "function_format": "{content}",
    "observation_format": "<start_of_turn>tool\n{content}<end_of_turn>\n<start_of_turn>model\n",
    "system": None,
}

mistral_template = {
    "system_format": "<s>[INST] {content} [/INST]",
    "user_format": "<s>[INST] {content} [/INST]",
    "assistant_format": " {content} </s>",
    "system": "You are a helpful assistant.",
}

llama2_template = {
    "system_format": "<<SYS>>\n{content}\n<</SYS>>\n\n",
    "user_format": "<s>[INST] {system_prompt}{content} [/INST]",
    "assistant_format": " {content} </s>",
    "system": "You are a helpful assistant.",
}

model2template = {
    "Qwen/Qwen1.5-0.5B": qwen_template,
    "Qwen/Qwen1.5-1.8B": qwen_template,
    "Qwen/Qwen1.5-7B": qwen_template,
    "google/gemma-2b": gemma_template,
    "google/gemma-7b": gemma_template,
    "Qwen/Qwen1.5-14B-Chat": qwen_template,
    "google/gemma-2-9b-it": gemma_template,
    "mistralai/Mistral-7B-instruct-v0.3": mistral_template,
    "meta-llama/Llama-2-13b-chat-hf": llama2_template
}

model2size = {
    "Qwen/Qwen1.5-0.5B": 620_000_000,
    "Qwen/Qwen1.5-1.8B": 1_840_000_000,
    "Qwen/Qwen1.5-7B": 7_720_000_000,
    "google/gemma-2b": 2_510_000_000,
    "google/gemma-7b": 8_540_000_000,
    "Qwen/Qwen1.5-14B-Chat": 14_300_000_000,
    "google/gemma-2-9b-it": 9_000_000_000,
    "mistralai/Mistral-7B-instruct-v0.3": 7_250_000_000,
    "meta-llama/Llama-2-13b-chat-hf": 13_000_000_000
}

model2base_model = {
    "Qwen/Qwen1.5-0.5B": "qwen1.5",
    "Qwen/Qwen1.5-1.8B": "qwen1.5",
    "Qwen/Qwen1.5-7B": "qwen1.5",
    "google/gemma-2b": "gemma",
    "google/gemma-7b": "gemma",
    "Qwen/Qwen1.5-14B-Chat": "qwen1.5",
    "google/gemma-2-9b-it": "gemma2",
    "mistralai/Mistral-7B-instruct-v0.3": "mistral",
    "meta-llama/Llama-2-13b-chat-hf": "llama"
}