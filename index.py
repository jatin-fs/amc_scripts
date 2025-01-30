import subprocess

def main():
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

if __name__ == "__main__":
    main()
