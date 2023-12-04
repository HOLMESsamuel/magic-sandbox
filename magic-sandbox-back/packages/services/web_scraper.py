import requests
from bs4 import BeautifulSoup
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from ..models.card import Card
from ..models.deck import Deck

class WebScraper:

    def __init__(self):
        # Set up the Selenium WebDriver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def get_dynamic_content(self, url):
        self.driver.get(url)
        time.sleep(3)  # Wait for the page to load.

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def get_deck(self, url: str):
        card_map_data, image_urls = self.get_data(url)
        return self.process_card_map_into_deck(card_map_data, image_urls)

    def get_data(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors

            soup = self.get_dynamic_content(url)

            # Find the script tag with the JSON content
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            if not script_tag:
                print("Script tag with JSON not found.")
                return None

            # Extract JSON from the script tag
            json_data = json.loads(script_tag.string)

            # Navigate to the desired data
            card_map = json_data.get('props', {}).get('pageProps', {}).get('redux', {}).get('deck', {}).get('cardMap', {})

            # Find all img tags with id "basicCardImage"
            image_tags = soup.find_all('img', {'id': 'basicCardImage'})
            #image_tags = soup.find_all('img', src=re.compile(r'https://cards.scryfall.io/.*'))
            print(image_tags)
            image_urls = {}
            for img in image_tags:
                src = img.get('src')
                if src:
                    # Extract image ID from src and store in dictionary
                    image_id = self.extract_image_id(src)
                    image_urls[image_id] = src

            return card_map, image_urls
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


    def process_card_map_into_deck(self, card_map, image_urls):
        cards = []
        for key, value in card_map.items():
            # if a card has multiple occurences there is only one entry in card map but the qty is set to the number
            for i in range(value.get('qty')):
                image_id = value.get('scryfallImageHash')
                #TODO add a default image url
                image_url = image_urls.get(image_id, 'default-image-url')
                # I recreate a unique id by adding i to the id
                card = Card(key + str(i), value.get('name'), value.get('typeCategory'), image_url)
                cards.append(card)
        deck = Deck(cards)
        return deck

    def extract_image_id(self, src):
        # Use regex to find the numerical string after the '?'
        match = re.search(r'\?(\d+)', src)
        if match:
            return match.group(1)  # Return the matched group (the number after '?')
        else:
            return None  # or some default value or raise an exception

    def close_driver(self):
        self.driver.quit()


