import json
import os

import requests
import yaml
from loguru import logger

from demo import LoraTrainingArguments, train_lora
from utils.constants import model2size
from utils.flock_api import get_task  # submit_task 부분은 제거할 예정

HF_USERNAME = os.environ["HF_USERNAME"]

# def split_training_data(src_file, train_file, val_file, split_ratio=0.8):
# 데이터 파일을 라인별로 읽어서 섞고 분할하기
# with open(src_file, "r", encoding="utf-8") as f:
#    lines = f.readlines()
# random.shuffle(lines)
# split_index = int(len(lines) * split_ratio)
# train_lines = lines[:split_index]
# val_lines = lines[split_index:]
#
# 분할된 데이터를 각각 저장
# with open(train_file, "w", encoding="utf-8") as f:
#    f.writelines(train_lines)
# with open(val_file, "w", encoding="utf-8") as f:
#    f.writelines(val_lines)
# logger.info(f"Data split completed: {len(train_lines)} training examples, {len(val_lines)} validation examples.")

if __name__ == "__main__":
    task_id = os.environ["TASK_ID"]
    # load training args
    current_folder = os.path.dirname(os.path.realpath(__file__))
    with open(f"{current_folder}/training_args.yaml", "r") as f:
        all_training_args = yaml.safe_load(f)

    task = get_task(task_id)
    logger.info(json.dumps(task, indent=4))
    # download data from the presigned url
    data_url = task["data"]["training_set_url"]
    context_length = task["data"]["context_length"]
    max_params = task["data"]["max_params"]

    # filter out the model within the max_params
    model2size = {k: v for k, v in model2size.items() if v <= max_params}
    all_training_args = {k: v for k, v in all_training_args.items() if k in model2size}
    logger.info(f"Models within the max_params: {list(all_training_args.keys())}")

    # download training data in chunks
    os.makedirs("data", exist_ok=True)
    response = requests.get(data_url, stream=True)
    training_data_path = "data/training_set.jsonl"
    with open(training_data_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # split the downloaded data into train and validation sets
    train_file = "data/train.jsonl"
    val_file = "data/val.jsonl"
    split_training_data(training_data_path, train_file, val_file, split_ratio=0.8)

    # Optionally, update each model's training arguments to include train/val file paths.
    for model_id in all_training_args.keys():
        # 기존 arguments에 추가하는 방식:
        # 주의: LoraTrainingArguments 클래스가 train_file, eval_file를 받을 수 있어야 합니다.
        all_training_args[model_id]["train_file"] = train_file
        all_training_args[model_id]["eval_file"] = val_file

    # Train all feasible models and perform validation; submission to FLock is skipped
    for model_id in all_training_args.keys():
        logger.info(f"Start to train the model {model_id}...")
        try:
            train_lora(
                model_id=model_id,
                context_length=context_length,
                training_args=LoraTrainingArguments(**all_training_args[model_id]),
            )
        except RuntimeError as e:
            logger.error(f"Error during training {model_id}: {e}")
            logger.info("Proceed to the next model...")
            continue

        # 여기까지 오면 모델 학습 및 내부 validation이 완료된 것으로 가정
        logger.info(
            f"Model {model_id} trained and validated successfully. (Submission skipped)"
        )

        # (기존 코드는 모델 저장 및 제출 관련 코드가 있으나, 제출 부분은 제거)
        # cleanup merged_model and outputs
        os.system("rm -rf merged_model")
        os.system("rm -rf outputs")
        continue
