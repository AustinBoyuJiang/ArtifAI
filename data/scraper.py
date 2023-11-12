import os
import json
import requests

# scraper setting
DATA_FILE = "data\\imageDataInfo.json"

category = "created_with_ai"
raw_data_dir = "data\\raw\\created_with_ai"


def download(data):
    for i, img in enumerate(data[category]):
        if img["id"]:  # not repeated
            continue

        # file path generation
        data["data_id"] += 1
        file_name = str(data["data_id"]) + ".jpg"
        file_path = os.path.join(raw_data_dir, file_name)

        # download
        response = requests.get(img["img_url"])
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # update
        data[category][i]["id"] = data["data_id"]
        data[category][i]["raw_data_path"] = file_path

        print(f"The image from the link '{img['img_url']}' has been saved as a file at '{file_path}'.")
    write_json_file(data, DATA_FILE)


def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


def write_json_file(content, file_path):
    with open(file_path, 'w') as file:
        json.dump(content, file, indent=4)


def download_imgs(tp, dir):
    global category, raw_data_dir
    category = tp
    raw_data_dir = dir
    data = read_json_file(DATA_FILE)
    download(data)


# if __name__ == '__main__':
#     download_imgs(category, raw_data_dir)