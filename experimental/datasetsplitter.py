import json
import os
from collections import defaultdict
import random # Needed for shuffling later, but not for this specific split code

# --- Configuration ---
input_jsonl_file = 'data/training_set.jsonl'  # <--- CHANGE THIS to your input file path
output_dir = 'data'           # <--- Directory where split files will be saved

# Define the exact system messages as keys for mapping
system_message_map = {
    "You are a solidity expert, and you are helping a developer to fix the vulnerability in the code.": "system_code_fixer.jsonl",
    "You are a Web3 and smart contract security expert. You are answering user's questions about smart contract security issues.": "system_security_qa.jsonl",
    "You are a Web3 and smart contract expert, and you are helping users to understand the security issues in the blockchain and smart contract.": "system_security_explainer.jsonl"
}
unknown_system_file = "system_unknown.jsonl" # File for any unexpected system messages

# --- Main Splitting Logic ---

print(f"Starting dataset split for: {input_jsonl_file}")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory: {output_dir}")

# Dictionary to hold file handles {filename: file_handle}
output_files = {}
# Dictionary to count lines per output file
line_counts = defaultdict(int)
processed_lines = 0
error_lines = 0
unknown_lines = 0

try:
    # Open output files (lazily, only when needed, or open all upfront)
    # Let's open them upfront for simplicity here
    for filename in list(system_message_map.values()) + [unknown_system_file]:
        filepath = os.path.join(output_dir, filename)
        # Initialize empty files even if no lines match
        with open(filepath, 'w', encoding='utf-8') as f:
            pass # Just create/clear the file

    # Re-open files for appending within the main loop context
    output_file_handles = {
        filename: open(os.path.join(output_dir, filename), 'a', encoding='utf-8')
        for filename in list(system_message_map.values()) + [unknown_system_file]
    }


    # Open and read the input file
    with open(input_jsonl_file, 'r', encoding='utf-8') as infile:
        for i, line in enumerate(infile):
            processed_lines += 1
            line = line.strip()
            if not line:
                continue # Skip empty lines

            try:
                data = json.loads(line)
                system_msg = data.get("system")

                if system_msg in system_message_map:
                    target_filename = system_message_map[system_msg]
                    output_file_handles[target_filename].write(line + '\n')
                    line_counts[target_filename] += 1
                else:
                    # Handle unknown system messages
                    target_filename = unknown_system_file
                    output_file_handles[target_filename].write(line + '\n')
                    line_counts[target_filename] += 1
                    unknown_lines += 1
                    if unknown_lines == 1: # Warn only once initially
                        print(f"  - WARNING: Found at least one line with an unknown system message. Writing to {unknown_system_file}")
                    if unknown_lines <= 5: # Print first few unknown messages
                         print(f"    - Line {i+1}: Unknown system message: '{system_msg}'")


            except json.JSONDecodeError:
                error_lines += 1
                print(f"  - WARNING: Skipping invalid JSON on line {i+1}: {line[:100]}...")
            except Exception as e:
                error_lines += 1
                print(f"  - ERROR: Unexpected error processing line {i+1}: {e}")

finally:
    # Ensure all file handles are closed
    for f_handle in output_file_handles.values():
        if f_handle:
            f_handle.close()

print("\n--- Split Summary ---")
print(f"Total lines processed: {processed_lines}")
if error_lines > 0:
    print(f"Lines with errors (skipped): {error_lines}")

for filename, count in line_counts.items():
    if count > 0: # Only report files that received lines
      print(f"File '{filename}': {count} lines")

total_written = sum(line_counts.values())
print(f"Total lines written to output files: {total_written}")
print("--------------------")
print(f"Splitting complete. Files saved in '{output_dir}' directory.")