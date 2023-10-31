import os
import json
import requests

# scraper setting
DOWNLOAD_DIR = "raw data\\created with ai"
JSON_FILE = "raw data\\image urls.json"

# initialization
file_id = 0

'''
status.json:
{
  "created_with_ai": [
    {
      "id": "unique_id",
      "img_url": "http://example.com/image.jpg",
      "file_path": "/path/to/saved/image.jpg",
      "processed": false,
      "training_or_testing": "training"
    },
    // ... more objects
  ],
  "not_created_with_ai": [
    // ... objects
  ]
  
# Preprocess filename to generate id 
}

'''


def download_images(data):
    global file_id
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    file_paths = data.values()
    for img_url in data:
        if data[img_url]:
            continue
        img_name = str(file_id) + ".jpg"
        file_path = os.path.join(DOWNLOAD_DIR, img_name)
        while file_path in file_paths:
            file_id += 1
            img_name = str(file_id) + ".jpg"
            file_path = os.path.join(DOWNLOAD_DIR, img_name)
        response = requests.get(img_url)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        data[img_url] = file_path
        print(f"The image from the link '{img_url}' has been saved as a file at '{file_path}'.")
    return data


def read_json_file():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return {}


def write_json_file(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    data = read_json_file()
    new_data = download_images(data)
    write_json_file(new_data)


if __name__ == '__main__':
    main()
