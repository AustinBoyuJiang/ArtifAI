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
    download_dir = config[category]["download_dir"]

    crawler.get_urls(category, total_scrolls, image_size)
    scraper.download_imgs(category, download_dir)


if __name__ == '__main__':
    config = read_json_file(CONFIG_FILE)
    if config["clear"]:
        init.clear()
        config["clear"] = False
        write_json_file(config, CONFIG_FILE)
    collect_data("created_with_ai")
    collect_data("not_created_with_ai")
    print("Data collection process has been successfully completed.")
