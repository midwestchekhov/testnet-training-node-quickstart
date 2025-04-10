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
    # Represents the system prompt, likely used as the very first instruction turn.
    # The actual Jinja logic for placement is complex, this is an approximation.
    "system_format": "<s>[INST] {content} [/INST]",

    # Standard user turn format
    "user_format": "<s>[INST] {content} [/INST]", # Assuming BOS needed per turn based on Jinja structure

    # Standard assistant turn format
    "assistant_format": " {content} </s>",

    "system": "You are a helpful assistant.", # Default system prompt content

    # --- UPDATED Tool/Function/Observation Formats ---
    # Based on official chat template structures. These are simplified representations.
    # Represents the assistant generating a tool call.
    "tool_format": "[TOOL_CALLS] {content} </s>",
    # Represents the details of a function within a tool call (approximation)
    "function_format": "{content}",
    # Represents the tool results being fed back.
    "observation_format": "[TOOL_RESULTS] {content} [/TOOL_RESULTS]",
}

llama2_template = {
    # Captures the system prompt structure. Needs careful handling by the training script.
    "system_format": "<<SYS>>\n{content}\n<</SYS>>\n\n", # Note: BOS/INST are handled below/by script logic

    # Standard user turn. Assumes BOS is prepended by script, includes INST.
    # The content might include the system prompt based on Jinja logic for the first turn.
    "user_format": "[INST] {content} [/INST]",

    # Standard assistant turn format
    "assistant_format": " {content} </s>", # Includes leading space and EOS

    "system": "You are a helpful assistant.", # Default system prompt content

    # --- Placeholders for Tools ---
    "tool_format": "{content}",
    "function_format": "{content}",
    "observation_format": "{content}",
}

# Microsoft Phi 계열
# phi3 그룹: Phi-3.5-mini-instruct, Phi-3-mini-4k-instruct, Phi-3-medium-4k-instruct
phi3_template = {
    "system_format": "<|phi3_start|>system\n{content}<|phi3_end|>\n",
    "user_format": "<|phi3_start|>user\n{content}<|phi3_end|>\n<|phi3_start|>assistant\n",
    "assistant_format": "{content}<|phi3_end|>\n",
    "tool_format": "{content}",
    "function_format": "{content}",
    "observation_format": "<|phi3_start|>tool\n{content}<|phi3_end|>\n<|phi3_start|>assistant\n",
    "system": "You are a helpful assistant.",
}

# phi4 그룹: Phi-4-mini-instruct, phi-4
phi4_template = {
    "system_format": "<|phi4_start|>system\n{content}<|phi4_end|>\n",
    "user_format": "<|phi4_start|>user\n{content}<|phi4_end|>\n<|phi4_start|>assistant\n",
    "assistant_format": "{content}<|phi4_end|>\n",
    "tool_format": "{content}",
    "function_format": "{content}",
    "observation_format": "<|phi4_start|>tool\n{content}<|phi4_end|>\n<|phi4_start|>assistant\n",
    "system": "You are a helpful assistant.",
}

# DeepSeek 계열 (Distill된 Qwen/Llama 모델)
deepseek_template = {
    "system_format": "<|ds_start|>system\n{content}<|ds_end|>\n",
    "user_format": "<|ds_start|>user\n{content}<|ds_end|>\n<|ds_start|>assistant\n",
    "assistant_format": "{content}<|ds_end|>\n",
    "tool_format": "{content}",
    "function_format": "{content}",
    "observation_format": "<|ds_start|>tool\n{content}<|ds_end|>\n<|ds_start|>assistant\n",
    "system": "You are a helpful assistant.",
}

# Zephyr 계열 (예: zephyr-7b-alpha, zephyr-7b-beta)
zephyr_template = {
    "system_format": "<|zephyr_start|>system\n{content}<|zephyr_end|>\n",
    "user_format": "<|zephyr_start|>user\n{content}<|zephyr_end|>\n<|zephyr_start|>assistant\n",
    "assistant_format": "{content}<|zephyr_end|>\n",
    "tool_format": "{content}",
    "function_format": "{content}",
    "observation_format": "<|zephyr_start|>tool\n{content}<|zephyr_end|>\n<|zephyr_start|>assistant\n",
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
    "mistralai/Mistral-7B-Instruct-v0.3": mistral_template,
    "meta-llama/Llama-2-13b-chat-hf": llama2_template,
    # Microsoft Phi 계열
    "microsoft/Phi-3.5-mini-instruct": phi3_template,
    "microsoft/Phi-3-mini-4k-instruct": phi3_template,
    "microsoft/Phi-3-medium-4k-instruct": phi3_template,
    "microsoft/Phi-4-mini-instruct": phi4_template,
    "microsoft/phi-4": phi4_template,

    # DeepSeek 계열
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": deepseek_template,
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B": deepseek_template,
    "deepseek-ai/DeepSeek-R1-Distill-Llama-8B": deepseek_template,
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B": deepseek_template,
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B": deepseek_template,
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B": deepseek_template,

    # Zephyr 계열
    "HuggingFaceH4/zephyr-7b-alpha": zephyr_template,
    "HuggingFaceH4/zephyr-7b-beta": zephyr_template
}

model2size = {
    "Qwen/Qwen1.5-0.5B": 620_000_000,
    "Qwen/Qwen1.5-1.8B": 1_840_000_000,
    "Qwen/Qwen1.5-7B": 7_720_000_000,
    "google/gemma-2b": 2_510_000_000,
    "google/gemma-7b": 8_540_000_000,
    "Qwen/Qwen1.5-14B-Chat": 14_300_000_000,
    "google/gemma-2-9b-it": 9_000_000_000,
    "mistralai/Mistral-7B-Instruct-v0.3": 7_250_000_000,
    "meta-llama/Llama-2-13b-chat-hf": 13_000_000_000
     # Microsoft Phi 계열 (예시 값)
    "microsoft/Phi-3.5-mini-instruct": 1_500_000_000,
    "microsoft/Phi-3-mini-4k-instruct": 1_200_000_000,
    "microsoft/Phi-3-medium-4k-instruct": 3_000_000_000,
    "microsoft/Phi-4-mini-instruct": 1_600_000_000,
    "microsoft/phi-4": 4_000_000_000,

    # DeepSeek 계열 (예시 값)
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": 1_500_000_000,
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B": 7_000_000_000,
    "deepseek-ai/DeepSeek-R1-Distill-Llama-8B": 8_000_000_000,
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B": 14_000_000_000,
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B": 32_000_000_000,
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B": 70_000_000_000,

    # Zephyr 계열 (예시 값)
    "HuggingFaceH4/zephyr-7b-alpha": 7_000_000_000,
    "HuggingFaceH4/zephyr-7b-beta": 7_000_000_000,
}

model2base_model = {
    "Qwen/Qwen1.5-0.5B": "qwen1.5",
    "Qwen/Qwen1.5-1.8B": "qwen1.5",
    "Qwen/Qwen1.5-7B": "qwen1.5",
    "google/gemma-2b": "gemma",
    "google/gemma-7b": "gemma",
    "Qwen/Qwen1.5-14B-Chat": "qwen1.5",
    "google/gemma-2-9b-it": "gemma",
    "mistralai/Mistral-7B-Instruct-v0.3": "mistral",
    "meta-llama/Llama-2-13b-chat-hf": "llama2",
    
    "microsoft/Phi-3.5-mini-instruct": "phi",
    "microsoft/Phi-3-mini-4k-instruct": "phi",
    "microsoft/Phi-3-medium-4k-instruct": "phi",
    "microsoft/Phi-4-mini-instruct": "phi",
    "microsoft/phi-4": "phi",

    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B": "qwen1.5",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B": "qwen1.5",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-8B": "llama",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B": "qwen1.5",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B": "qwen1.5",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B": "llama",

    "HuggingFaceH4/zephyr-7b-alpha": "zephyr",
    "HuggingFaceH4/zephyr-7b-beta": "zephyr",
}
