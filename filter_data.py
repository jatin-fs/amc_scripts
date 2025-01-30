import os
import json

# Path to the merged JSON file
merged_file_path = "result_data/merged_data.json"

# Path for the filtered output file
filtered_output_file = "result_data/filtered_data.json"

# Fields to keep
fields_to_keep = [
    "Id", "DepartmentName", "DepartmentId", "DocumentNumber",
    "Description", "FileUpload", "CreatedDateSTR", "GTypeText",
    "CircularDOCNAME", "OrderDateSTR", "EffectiveDateSTR", "Remarks"
]

# Load merged data
try:
    with open(merged_file_path, "r", encoding="utf-8") as f:
        merged_data = json.load(f)

    # Filter each object in the data array
    filtered_data = [{key: item[key] for key in fields_to_keep if key in item} for item in merged_data]

    # Save the filtered data to a new JSON file
    with open(filtered_output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)

    print(f"Filtered data saved to {filtered_output_file}")

except FileNotFoundError:
    print(f"Error: {merged_file_path} not found. Please ensure the merged file exists.")

except json.JSONDecodeError:
    print(f"Error: Unable to decode JSON in {merged_file_path}. Please check the file format.")
