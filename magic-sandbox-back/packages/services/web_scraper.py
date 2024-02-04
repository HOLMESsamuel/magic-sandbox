import uuid
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
        print("initializing web scraper")
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
    
    def get_archidekt_deck(self, url: str):
        card_map_data, image_urls = self.get_archidekt_data(url)
        return self.process_archidekt_card_map_into_deck(card_map_data, image_urls)
    
    def get_tapped_out_deck(self, url: str):
        card_map_data = self.get_tapped_out_data(url)
        return self.process_tapped_out_card_map_into_deck(card_map_data)
    
    def get_deck(self, url: str):
        if("archidekt" in url):
            return self.get_archidekt_deck(url)
        elif("tappedout" in url):
            return self.get_tapped_out_deck(url)
        else:
            raise ValueError("The url must be from either archidekt or tapped out")

    def get_tapped_out_data(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors

            soup = BeautifulSoup(response.content, 'html.parser')

            cards_info = []

            # Find all 'li' elements with the class 'member' which represents each card entry
            for li in soup.find_all('li', class_='member'):
                # Find the 'a' tag within each 'li' for quantity
                qty_tag = li.find('a', class_='qty')
                if qty_tag:
                    qty = qty_tag['data-qty']  # Extract the quantity
                else:
                    qty = 1  # Default quantity

                # Now find the 'span' with class 'card' for card details
                card_span = li.find('span', class_='card')
                if card_span:
                    # Find the 'a' tag within the 'span' for card details
                    card_link = card_span.find('a', class_='card-link')
                    if card_link:
                        card_name = card_link['data-name']
                        card_image = card_link['data-image']
                        if card_image.startswith('//'):
                            card_image = 'https:' + card_image  
                        # Append a dictionary with card details and quantity to the cards_info list
                        cards_info.append({
                            'name': card_name,
                            'image_url': card_image,
                            'quantity': qty
                        })
            
            return cards_info
        except Exception as e:
            print(f"Error: {e}")

    def get_archidekt_data(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors

            #static_content = BeautifulSoup(response.content, 'html.parser')
            #print(static_content)

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

            # Find all img tags with id "basicCardImage they are containing the srcs to card images"
            image_tags = soup.find_all('img', {'id': 'basicCardImage'})
            #image_tags = soup.find_all('img', src=re.compile(r'https://cards.scryfall.io/.*'))
            
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


    def process_archidekt_card_map_into_deck(self, card_map, image_urls):
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
    
    def process_tapped_out_card_map_into_deck(self, card_map):
        try:
            cards = []
            for card_data in card_map:
                # if a card has multiple occurences there is only one entry in card map but the qty is set to the number
                for i in range(int(card_data["quantity"])):
                    card = Card(str(uuid.uuid4()), card_data["name"], "type", card_data["image_url"])
                    cards.append(card)
            deck = Deck(cards)
            return deck
        except Exception as e:
            print(e)

    def extract_image_id(self, src):
        # Use regex to find the numerical string after the '?'
        match = re.search(r'\?(\d+)', src)
        if match:
            return match.group(1)  # Return the matched group (the number after '?')
        else:
            return None  # or some default value or raise an exception

    def close_driver(self):
        self.driver.quit()


