import os
import json
import random
import numpy as np
from PIL import Image

DATA_FILE = "data\\imageDataInfo.json"

category = "created_with_ai"
test_size = 0.2
processed_training_data_dir = "data\\processed\\training\\created_with_ai"
processed_testing_data_dir = "data\\processed\\testing\\created_with_ai"


def process(img):
    raw_file_path = img["raw_data_path"]

    image = Image.open(raw_file_path)  # Load the image
    image = image.resize((256, 256))  # Resize the image to 256x256 pixels
    image_array = np.asarray(image) / 255.0  # Normalization

    file_name = str(img["id"]) + ".npy"
    img["training"] = random.random() > test_size
    if img["training"]:
        file_dir = processed_training_data_dir
    else:
        file_dir = processed_testing_data_dir
    file_path = os.path.join(file_dir, file_name)
    np.save(file_path, image_array)
    img["processed_data_path"] = file_path
    return img


def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


def write_json_file(content, file_path):
    with open(file_path, 'w') as file:
        json.dump(content, file, indent=4)


def process_imgs(tp, ratio, seed, dir1, dir2):
    global category, test_size, processed_training_data_dir, processed_testing_data_dir
    category = tp
    test_size = ratio
    processed_training_data_dir = dir1
    processed_testing_data_dir = dir2

    random.seed(seed)
    data = read_json_file(DATA_FILE)
    tot = len(data[category])
    for i, img in enumerate(data[category]):
        data[category][i] = process(img)
        print(f"({i+1}/{tot}) Image with ID {img['id']} has been successfully processed.")
    write_json_file(data, DATA_FILE)


if __name__ == '__main__':
    process_imgs(category, processed_training_data_dir, processed_testing_data_dir)
