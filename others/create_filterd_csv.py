import os
import json
import csv

# Path to the filtered JSON file
filtered_json_path = "mergedresult/filtered_data.json"

# Path for the output CSV file
csv_output_path = "mergedresult/filtered_data.csv"

# Load filtered JSON data
try:
    with open(filtered_json_path, "r", encoding="utf-8") as f:
        filtered_data = json.load(f)

    # Ensure there is data to process
    if not filtered_data:
        print("No data found in filtered_data.json")
        exit()

    # Get the header (keys from the first dictionary)
    headers = filtered_data[0].keys()

    # Write to CSV
    with open(csv_output_path, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=headers)
        csv_writer.writeheader()
        csv_writer.writerows(filtered_data)

    print(f"CSV file saved to {csv_output_path}")

    # Print CSV data
    with open(csv_output_path, "r", encoding="utf-8") as csvfile:
        print("\nCSV File Content:\n")
        print(csvfile.read())

except FileNotFoundError:
    print(f"Error: {filtered_json_path} not found. Please ensure the filtered file exists.")

except json.JSONDecodeError:
    print(f"Error: Unable to decode JSON in {filtered_json_path}. Please check the file format.")
