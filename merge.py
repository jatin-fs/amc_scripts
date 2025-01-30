import os
import json

# Directory containing the JSON files
json_dir = "sampledata"  # Change this to your directory path

# Directory to store the merged JSON file
output_dir = "result_data"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# List to store all combined data items
merged_data_list = []

# Read and process all JSON files
for file_name in os.listdir(json_dir):
    if file_name.endswith(".json"):
        file_path = os.path.join(json_dir, file_name)

        # Read JSON file
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                json_content = json.load(f)
                merged_data_list.extend(json_content.get("data", []))  # Merge only "data" lists
            
            except json.JSONDecodeError:
                print(f"Error reading {file_name}")

# Path for the merged output file
output_file = os.path.join(output_dir, "merged_data.json")

# Save merged data into the output file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data_list, f, indent=4, ensure_ascii=False)

print(f"Merged data saved to {output_file}")
