import subprocess
import time

def main():
    start_time = time.time()  # Start timing

    print("Script started\n")

    # Run merge.py script
    subprocess.run(["python", "merge.py"], check=True)
    print("Data merging done\n")

    # Run filter_data.py script
    subprocess.run(["python", "filter_data.py"], check=True)
    print("Data filtering done\n")

    # Run lang_detect.py script
    subprocess.run(["python", "lang_detect.py"], check=True)
    print("Language detection done\n")

    # Run create_csv.py script
    subprocess.run(["python", "create_csv.py"], check=True)
    print("CSV creation done\n")

    print("Script ended\n")

     # Calculate time taken
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_minutes = elapsed_time / 60  # Convert seconds to minutes

    print(f"Total execution time in seconds: {elapsed_time:.2f} seconds\n")
    print(f"Total execution time in muinets: {elapsed_minutes:.2f} minutes\n")

if __name__ == "__main__":
    main()
