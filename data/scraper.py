import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.artstation.com"

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        return None

def extract_image_links(soup):
    # This function needs to be tailored based on the actual structure of Artstation's HTML
    # For this example, I'm using a generic placeholder
    img_tags = soup.find_all('img', class_='some_class_name')
    return [img['src'] for img in img_tags if 'src' in img.attrs]

def get_next_page(soup):
    # Again, this is a generic placeholder
    next_page_tag = soup.find('a', class_='next_page_class_name')
    if next_page_tag:
        return BASE_URL + next_page_tag['href']
    return None
