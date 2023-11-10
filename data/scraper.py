import os
import json
import requests

# scraper setting
DATA_FILE = "data\\data.json"

category = "created_with_ai"
download_dir = "data\\raw\\created_with_ai"


def download(data):
    for i, item in enumerate(data[category]):
        if item["id"]:  # not repeated
            continue

        # file path generation
        data["data_id"] += 1
        file_name = str(data["data_id"]) + ".jpg"
        file_path = os.path.join(download_dir, file_name)

        # download
        response = requests.get(item["img_url"])
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # update
        data[category][i]["id"] = data["data_id"]
        data[category][i]["file_path"] = file_path

        print(f"The image from the link '{item['img_url']}' has been saved as a file at '{file_path}'.")
    write_json_file(data, DATA_FILE)


def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


def write_json_file(content, file_path):
    with open(file_path, 'w') as file:
        json.dump(content, file, indent=4)


def download_imgs(cate, dir):
    global category, download_dir
    category = cate
    download_dir = dir
    data = read_json_file(DATA_FILE)
    download(data)


if __name__ == '__main__':
    data = read_json_file(DATA_FILE)
    download_imgs(data)
