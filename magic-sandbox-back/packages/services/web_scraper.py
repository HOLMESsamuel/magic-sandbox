import requests
from bs4 import BeautifulSoup
import json
import re

from ..models.card import Card
from ..models.deck import Deck

class WebScraper:

    def get_deck(self, url: str):
        card_map_data, image_urls = self.get_data(url)
        return self.process_card_map_into_deck(card_map_data, image_urls)

    def get_data(self, url: str):
        try:
            print(url)
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors

            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup)

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
            #image_tags = soup.find_all('img', {'id': 'basicCardImage'})
            image_tags = soup.find_all('img', src=re.compile(r'https://cards.scryfall.io/.*'))
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


