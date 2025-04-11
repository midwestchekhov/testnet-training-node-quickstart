import os
from dataclasses import dataclass

import torch
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig

from dataset import SFTDataCollator, SFTDataset
from utils.constants import model2template


@dataclass
class LoraTrainingArguments:
    per_device_train_batch_size: int
    gradient_accumulation_steps: int
    num_train_epochs: int
    lora_rank: int
    lora_alpha: int
    lora_dropout: int
    # added
    learning_rate: float
    weight_decay: float


def train_lora(
    model_id: str, context_length: int, training_args: LoraTrainingArguments
):
    assert model_id in model2template, f"model_id {model_id} not supported"
    lora_config = LoraConfig(
        r=training_args.lora_rank,
        target_modules=[
            "q_proj",
            "v_proj",
        ],
        lora_alpha=training_args.lora_alpha,
        lora_dropout=training_args.lora_dropout,
        task_type="CAUSAL_LM",
        use_dora=True,  # turn off if something goes wrong
    )

    # Load model in 4-bit to do qLoRA
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    # --- DEBUGGING PRINT ---
    print(
        f"DEBUG: Type of training_args.learning_rate BEFORE SFTConfig: {type(training_args.learning_rate)}"
    )
    print(
        f"DEBUG: Value of training_args.learning_rate BEFORE SFTConfig: {training_args.learning_rate}"
    )
    # --- END DEBUGGING PRINT ---

    # Inside train_lora function in demo.py
    print(
        f"DEBUG: Received training_args object: {training_args}"
    )  # See the whole object
    print(f"DEBUG: Intending to use LR: {training_args.learning_rate}")
    print(f"DEBUG: Intending to use Weight Decay: {training_args.weight_decay}")
    print(f"DEBUG: Intending to use Epochs: {training_args.num_train_epochs}")

    training_args_sft = SFTConfig(  # Renamed variable to avoid confusion
        per_device_train_batch_size=training_args.per_device_train_batch_size,
        gradient_accumulation_steps=training_args.gradient_accumulation_steps,
        # Make SURE these lines explicitly use the values from the input object:
        learning_rate=training_args.learning_rate,
        weight_decay=training_args.weight_decay,
        num_train_epochs=training_args.num_train_epochs,
        # Keep other params like warmup_steps, logging_steps etc. as you've set them
        warmup_steps=10,  # As you modified
        logging_steps=5,  # As you modified
        bf16=True,
        output_dir="outputs",
        optim="paged_adamw_8bit",
        remove_unused_columns=False,
        max_seq_length=context_length,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        report_to="wandb",  # If using WandB
        evaluation_strategy="no",  # check with epoch, will it work?
        save_strategy="epoch",  # may need
        save_total_limits=3,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        use_fast=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token  # Common practice
        print("Set pad_token to eos_token")
    tokenizer.padding_side = "right"  # dunno should i leave this when it runs?

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map={"": 0},
        token=os.environ["HF_TOKEN"],
    )

    # Load dataset
    dataset = SFTDataset(
        file="data/training_set.jsonl",
        tokenizer=tokenizer,
        max_seq_length=context_length,
        template=model2template[model_id],
    )

    # Define trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        args=training_args,
        peft_config=lora_config,
        data_collator=SFTDataCollator(tokenizer, max_seq_length=context_length),
    )

    # Train model
    trainer.train()

    # save model
    trainer.save_model("outputs")

    # remove checkpoint folder
    # os.system("rm -rf outputs/checkpoint-*")

    # upload lora weights and tokenizer
    print("Training Completed.")


if __name__ == "__main__":
    # Define training arguments for LoRA fine-tuning
    training_args = LoraTrainingArguments(
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=2,
        lora_rank=8,
        lora_alpha=16,
        lora_dropout=0.05,
    )

    # Set model ID and context length
    model_id = "Qwen/Qwen1.5-0.5B"
    context_length = 2048

    # Start LoRA fine-tuning
    train_lora(
        model_id=model_id, context_length=context_length, training_args=training_args
    )
