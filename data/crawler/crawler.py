import os
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests

# Webdriver setting
opt = webdriver.ChromeOptions()
opt.add_argument("disable-extensions")
driver = webdriver.Chrome(options=opt)

# crawler setting
URL = "https://www.artstation.com/search?sort_by=relevance&category_ids_include=27&tags_include=CreatedWithAI"
DOWNLOAD_DIR = "downloads"
total_scrolls = 10
current_scrolls = 0
scroll_time = 3
old_height = 0
projects_list_xpath = '/html/body/div[2]/app-root/app-layout/search-artwork/div[5]/projects-list/div/projects-list-item'


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


def image_src_in_size(src, size):
    return src


def get_image_sources():
    scroll()
    links = driver.find_elements(By.XPATH, projects_list_xpath)
    sources = []
    for link in links:
        sources.append(image_src_in_size(link.find_elements(By.TAG_NAME, 'img')[1].get_attribute('src'), 'large'))
    return sources


def download_images(img_sources):
    for src in img_sources:
        print(src)
        img_name = src.split('/')[-1].split("?")[0]
        img_path = os.path.join(DOWNLOAD_DIR, img_name)
        response = requests.get(src)
        with open(img_path, 'wb') as file:
            file.write(response.content)


def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    driver.get(URL)
    img_sources = get_image_sources()
    download_images(img_sources)
    driver.close()


if __name__ == '__main__':
    main()
