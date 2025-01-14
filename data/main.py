import os
import json
import init
import crawler
import scraper
import processor

# setting
CONFIG_FILE = "config.json"


def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}


def write_json_file(content, file_path):
    with open(file_path, 'w') as file:
        json.dump(content, file, indent=4)


def collect_data(category):
    print(f"Commencing data collection for the \"{category}\" category.")

    total_scrolls = config[category]["total_scrolls"]
    image_size = config["image_size"]
    raw_data_dir = config[category]["raw_data_dir"]

    crawler.get_urls(category, total_scrolls, image_size)
    scraper.download_imgs(category, raw_data_dir)


def process_data(category):
    print(f"Commencing data processing for the \"{category}\" category.")

    processed_training_data_dir = config[category]["processed_training_data_dir"]
    processed_testing_data_dir = config[category]["processed_testing_data_dir"]
    processor.process_imgs(category,
                           config["test_size"],
                           config["random_state"],
                           processed_training_data_dir,
                           processed_testing_data_dir)


if __name__ == '__main__':
    config = read_json_file(CONFIG_FILE)
    if config["clear"]:
        init.clear()
        config["clear"] = False
        write_json_file(config, CONFIG_FILE)
    collect_data("created_with_ai")
    # collect_data("not_created_with_ai")
    process_data("created_with_ai")
    # process_data("not_created_with_ai")
    print("Data collection process has been successfully completed.")
