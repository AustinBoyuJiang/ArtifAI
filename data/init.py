import os
import json
import shutil

DATA_FILE = "data\\imageDataInfo.json"
BASE_DIR = 'data'

paths = [
    'processed/training/created_with_ai',
    'processed/training/not_created_with_ai',
    'processed/testing/created_with_ai',
    'processed/testing/not_created_with_ai',
    'raw/created_with_ai',
    'raw/not_created_with_ai'
]

data = {
    "data_id": -1,
    "created_with_ai": [],
    "not_created_with_ai": []
}


def clear_and_create_dir(path):
    # Check if the directory already exists
    if os.path.exists(path):
        # Clear all the contents of the directory
        shutil.rmtree(path)
    # Create the directory
    os.makedirs(path)


def setup_directory_structure(base_path):
    # Loop through the paths and create/clear them
    for path in paths:
        full_path = os.path.join(base_path, path)
        clear_and_create_dir(full_path)
        print(f"Directory created: {full_path}")


def write_json_file(content, file_path):
    with open(file_path, 'w') as file:
        json.dump(content, file, indent=4)


def clear():
    print("Initiating the data collection program.")
    setup_directory_structure(BASE_DIR)
    write_json_file(data, DATA_FILE)


if __name__ == '__main__':
    clear()
