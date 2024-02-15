import uuid
import requests
from bs4 import BeautifulSoup
import json
import re
import time
from .scraper import Scraper
from ..models.card import Card
from ..models.deck import Deck

class ArchidektWebScraper(Scraper):

    def get_deck(self, url: str):
        card_map_data, soup = self.get_archidekt_data(url)
        return self.process_archidekt_card_map_into_deck(card_map_data, soup)

    def get_dynamic_content(self, url):
        self.driver.get(url)
        time.sleep(3)  # Wait for the page to load.

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def get_archidekt_data(self, url: str):
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

            return card_map, soup
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


    def process_archidekt_card_map_into_deck(self, card_map, soup):
        cards = []
        for key, value in card_map.items():
            # Construct the specific div id for the current card
            card_div_id = f'deck-card-dom-{key}'
            
            card_div = soup.find('div', id=card_div_id)
            
            if card_div:
                # Find all img tags within this div with the specific class
                img_tags = card_div.find_all('img', class_='basicCard_image__cNHMf')
                img_urls = [img['src'] for img in img_tags if img.has_attr('src')]
                
                # If there's only one img, we fetch its src for the image
                # If there are two imgs, it means the card has two sides and we need both srcs
                # Adjust the Card constructor call based on your Card class' requirements
                for i in range(value.get('qty')):
                    if len(img_urls) == 1:
                        # Assuming your Card constructor can handle a single image URL
                        card = Card(str(uuid.uuid4()), value.get('name'), value.get('type'), img_urls[0])
                    elif len(img_urls) == 2:
                        # Assuming your Card constructor can handle two image URLs for two-sided cards
                        card = Card(str(uuid.uuid4()), value.get('name'), value.get('type'), img_urls[0], img_urls[1])
                    else:
                        card = Card(str(uuid.uuid4()), value.get('name'), value.get('type'), '')
                    
                    cards.append(card)

        deck = Deck(cards)
        return deck
    

    def extract_image_id(self, src):
        # Use regex to find the numerical string after the '?'
        match = re.search(r'\?(\d+)', src)
        if match:
            if "front" in src: #two faces card will have the same number after ? so I add front or back to make it unique
                return "front" + match.group(1)
            else:
                return "back" + match.group(1) # Return the matched group (the number after '?')
        else:
            return None