import os
import json
from scraper import fetch_page, extract_image_links, get_next_page
from processor import process_image
import urllib.request


STATE_FILE = "state.json"
RAW_DATA_DIR = "./raw_data"
PROCESSED_DATA_DIR = "./processed_data"


def save_image(url, category):
    response = urllib.request.urlopen(url)
    filename = os.path.join(RAW_DATA_DIR, category, url.split('/')[-1])
    with open(filename, 'wb') as file:
        file.write(response.read())
    process_image(filename.split('/')[-1], category)  # Process the image once saved


def save_state(state):
    with open(STATE_FILE, 'w') as file:
        json.dump(state, file)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as file:
            return json.load(file)
    return {
        "ai_url": "https://www.artstation.com/search?sort_by=relevance&category_ids_include=27&tags_include=CreatedWithAI",
        "non_ai_url": "https://www.artstation.com/search?sort_by=relevance&category_ids_include=27&tags_exclude=CreatedWithAI"
    }


def main():
    state = load_state()

    # For each category
    for category, start_url in [("created_with_ai", state["ai_url"]), ("not_created_with_ai", state["non_ai_url"])]:
        current_url = start_url

        while current_url:
            print(f"Fetching: {current_url}")
            soup = fetch_page(current_url)

            if not soup:
                break

            for img_url in extract_image_links(soup):
                save_image(img_url, category)

            current_url = get_next_page(soup)
            state[f"{category}_url"] = current_url
            save_state(state)


if __name__ == "__main__":
    main()
