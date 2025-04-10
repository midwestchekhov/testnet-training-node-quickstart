import json
import os
import random
from collections import defaultdict
import logging # Use logging instead of print for better practice

# --- Configuration ---
input_jsonl_file = 'data/training_set.jsonl'  # <--- CHANGE THIS
output_dir = 'data'          # <--- Directory for final train/val files
intermediate_dir = 'data/temp' # Temp dir for system splits
split_ratio = 0.7                        # 70% for training
random.seed(42)                          # For reproducible shuffles

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the exact system messages as keys for mapping intermediate filenames
system_message_map = {
    "You are a solidity expert, and you are helping a developer to fix the vulnerability in the code.": "intermediate_code.jsonl",
    "You are a Web3 and smart contract security expert. You are answering user's questions about smart contract security issues.": "intermediate_qa.jsonl",
    "You are a Web3 and smart contract expert, and you are helping users to understand the security issues in the blockchain and smart contract.": "intermediate_explain.jsonl"
}
unknown_system_file = "intermediate_unknown.jsonl"

# Define final output filenames
final_train_file = os.path.join(output_dir, 'train_merged.jsonl')
final_val_map = {
    "intermediate_code.jsonl": os.path.join(output_dir, 'val_code.jsonl'),
    "intermediate_qa.jsonl": os.path.join(output_dir, 'val_qa.jsonl'),
    "intermediate_explain.jsonl": os.path.join(output_dir, 'val_explain.jsonl'),
    unknown_system_file: os.path.join(output_dir, 'val_unknown.jsonl') # Handle unknowns too
}


# --- Helper Function (Modified from your snippet) ---
def split_lines(lines, split_ratio=0.7):
    """Shuffles lines and splits them into train and validation lists."""
    if not lines:
        return [], []
    random.shuffle(lines)
    split_index = int(len(lines) * split_ratio)
    train_lines = lines[:split_index]
    val_lines = lines[split_index:]
    return train_lines, val_lines

# --- Main Logic ---

# 1. Create directories
os.makedirs(output_dir, exist_ok=True)
os.makedirs(intermediate_dir, exist_ok=True)
logger.info(f"Output directory: {output_dir}")
logger.info(f"Intermediate directory: {intermediate_dir}")

# 2. Split by System Message into Intermediate Files
logger.info(f"Step 1: Splitting '{input_jsonl_file}' by system message...")
intermediate_files = list(system_message_map.values()) + [unknown_system_file]
intermediate_handles = {}
lines_per_intermediate = defaultdict(int)
unknown_count = 0

try:
    # Open intermediate files
    for filename in intermediate_files:
        filepath = os.path.join(intermediate_dir, filename)
        intermediate_handles[filename] = open(filepath, 'w', encoding='utf-8')

    # Read input and distribute lines
    with open(input_jsonl_file, 'r', encoding='utf-8') as infile:
        for i, line in enumerate(infile):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                system_msg = data.get("system")
                target_filename = system_message_map.get(system_msg, unknown_system_file)

                if target_filename == unknown_system_file and system_msg not in system_message_map:
                     unknown_count+=1
                     if unknown_count == 1: logger.warning(f"Found unknown system message(s). Writing to {unknown_system_file}")

                intermediate_handles[target_filename].write(line + '\n')
                lines_per_intermediate[target_filename] += 1

            except json.JSONDecodeError:
                logger.warning(f"Skipping invalid JSON on line {i+1} in input file.")
            except Exception as e:
                logger.error(f"Error processing line {i+1} in input file: {e}")

finally:
    # Close all intermediate file handles
    for handle in intermediate_handles.values():
        handle.close()

logger.info("Step 1 finished. Lines per intermediate file:")
for fname, count in lines_per_intermediate.items():
     logger.info(f"  - {fname}: {count} lines")

# 3. Split each Intermediate File into Train/Val, Merge Train, Save Val
logger.info(f"\nStep 2: Splitting intermediate files ({split_ratio*100:.0f}% train / {(1-split_ratio)*100:.0f}% val)...")
all_train_lines = []
total_train_count = 0
total_val_count = 0

for intermediate_filename, count in lines_per_intermediate.items():
    if count == 0:
        logger.info(f"  - Skipping empty intermediate file: {intermediate_filename}")
        continue

    intermediate_filepath = os.path.join(intermediate_dir, intermediate_filename)
    final_val_filepath = final_val_map.get(intermediate_filename) # Get corresponding final val path

    if not final_val_filepath:
         logger.warning(f"  - No final validation file defined for {intermediate_filename}, skipping validation output for this file.")
         continue # Should not happen with current setup, but safety check

    logger.info(f"  - Processing: {intermediate_filename} -> {os.path.basename(final_val_filepath)}")

    # Read lines from the intermediate file
    with open(intermediate_filepath, "r", encoding="utf-8") as f:
        lines = f.readlines() # Read lines including newline characters

    # Split the lines from this category
    train_lines, val_lines = split_lines(lines, split_ratio)

    # Append train lines to the master list
    all_train_lines.extend(train_lines)

    # Write validation lines directly to their final destination
    with open(final_val_filepath, "w", encoding="utf-8") as f_val:
        f_val.writelines(val_lines)

    logger.info(f"    - Split: {len(train_lines)} train, {len(val_lines)} val")
    total_train_count += len(train_lines)
    total_val_count += len(val_lines)


# 4. Shuffle and Save Merged Training Data
logger.info("\nStep 3: Shuffling and saving merged training data...")
random.shuffle(all_train_lines) # Shuffle the combined training data

with open(final_train_file, "w", encoding="utf-8") as f_train:
    f_train.writelines(all_train_lines)

logger.info(f"Merged training data saved to: {final_train_file}")

# 5. Final Summary
logger.info("\n--- Final Summary ---")
logger.info(f"Total Training Examples: {total_train_count} (saved in {os.path.basename(final_train_file)})")
logger.info(f"Total Validation Examples: {total_val_count} (split into category files below)")
for intermediate_filename, final_val_filepath in final_val_map.items():
     # Check if the validation file actually exists and has content
     val_count = lines_per_intermediate.get(intermediate_filename, 0) - int(lines_per_intermediate.get(intermediate_filename, 0) * split_ratio)
     if os.path.exists(final_val_filepath) and val_count > 0 :
         logger.info(f"  - Validation set '{os.path.basename(final_val_filepath)}': ~{val_count} examples")

logger.info(f"\nSplitting complete. Final files are in '{output_dir}'.")

# Optional: Clean up intermediate directory
# import shutil
# try:
#     shutil.rmtree(intermediate_dir)
#     logger.info(f"Cleaned up intermediate directory: {intermediate_dir}")
# except Exception as e:
#     logger.error(f"Could not remove intermediate directory {intermediate_dir}: {e}")