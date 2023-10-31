import os
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# crawler setting
URL = "https://www.artstation.com/search?sort_by=relevance&category_ids_include=27&tags_include=CreatedWithAI"
JSON_FILE = "raw data\\image urls.json"
total_scrolls = 30  # number of images = total_scrolls * 10
image_size = "smaller_square"  # smaller_square/small/medium/large

# initialization
current_scrolls = 0
scroll_time = 3
old_height = 0
projects_list_xpath = '/html/body/div[2]/app-root/app-layout/search-artwork/div[5]/projects-list/div/projects-list-item'

# Webdriver setting
opt = webdriver.ChromeOptions()
opt.add_argument("disable-extensions")
driver = webdriver.Chrome(options=opt)


def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


def scroll():
    global old_height, current_scrolls

    while current_scrolls < total_scrolls:
        old_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height())
        current_scrolls += 1


def replace_image_size(url, size):
    base_url, query_string = url.split('?')
    new_url = base_url.replace('smaller_square', size) + '?' + query_string
    return new_url


def get_image_urls():
    scroll()
    links = driver.find_elements(By.XPATH, projects_list_xpath)
    img_urls = []
    for link in links:
        url = replace_image_size(link.find_elements(By.TAG_NAME, 'img')[1].get_attribute('src'), image_size)
        img_urls.append(url)
        print(f"Successfully crawled the image link: {url}")
    return img_urls


def read_json_file():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return {}


def write_json_file(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def update_image_urls(img_urls, data):
    for url in img_urls:
        if url not in data:
            data[url] = None
    write_json_file(data)


def main():
    driver.get(URL)
    data = read_json_file()
    img_urls = get_image_urls()
    update_image_urls(img_urls, data)
    driver.close()


if __name__ == '__main__':
    main()
