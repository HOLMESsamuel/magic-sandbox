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
        card_map_data, soup = self.get_archidekt_data(url)
        return self.process_archidekt_card_map_into_deck(card_map_data, soup)
    
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

            self.add_cards_from_tapped_out(cards_info, soup)
            self.add_commander_from_tapped_out(cards_info, soup)
            
            return cards_info
        except Exception as e:
            print(f"Error: {e}")

    def add_cards_from_tapped_out(self, cards_info, soup):
        # Find all 'li' elements with the class 'member' which represents each card entry
        for li in soup.find_all('li', class_='member'):
            if 'maybe' not in li.get('id', '') and 'side' not in li.get('id', ''):  # checks if the card is not from the sideboard
                # Find the 'a' tag within each 'li' for quantity
                qty_tag = li.find('a', class_='qty')
                if qty_tag:
                    qty = qty_tag['data-qty']  # Extract the quantity
                else:
                    qty = 1  # Default quantity

                # Find the first 'span' with class 'card' for the main card details
                card_span = li.find('span', class_='card')
                if card_span:
                    card_link = card_span.find('a', class_='card-link')
                    if card_link:
                        card_name = card_link['data-name']
                        card_image = card_link['data-image']
                        if card_image.startswith('//'):
                            card_image = 'https:' + card_image
                        
                        # Initialize card_info with details from the first side
                        card_info = {
                            'name': card_name,
                            'image_url': card_image,
                            'quantity': qty,
                            'flip_image_url': ''
                        }

                        # Attempt to find the flip side image directly within the next 'span'
                        next_span = card_span.find_next_sibling('span', class_='card')
                        if next_span:
                            flip_link = next_span.find('a') 
                            if flip_link:
                                flip_image_url = flip_link.get('data-image', '')
                                if flip_image_url:
                                    flip_image = 'https:' + flip_image_url if flip_image_url.startswith('//') else flip_image_url
                                    card_info['flip_image_url'] = flip_image

                        # Append the card_info to cards_info
                        cards_info.append(card_info)

    def add_commander_from_tapped_out(self, cards_info, soup):
        for div in soup.find_all('div', class_='row'):
                card_span = div.find('span')
                if card_span:
                    card_link = card_span.find('a', class_='card-hover')
                    if card_link and card_link.find('img', class_='commander-img'):
                        card_name = card_link['data-name']
                        card_image = card_link['data-image']
                        if card_image.startswith('//'):
                            card_image = 'https:' + card_image
                        cards_info.append({
                            'name': card_name,
                            'image_url': card_image,
                            'quantity': 1,
                            'flip_image_url': ''
                        })


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
    
    def process_tapped_out_card_map_into_deck(self, card_map):
        try:
            cards = []
            for card_data in card_map:
                # if a card has multiple occurences there is only one entry in card map but the qty is set to the number
                for i in range(int(card_data["quantity"])):
                    card = Card(str(uuid.uuid4()), card_data["name"], "type", card_data["image_url"], card_data['flip_image_url'])
                    cards.append(card)
            deck = Deck(cards)
            return deck
        except Exception as e:
            print("exception" + e)

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

    def close_driver(self):
        self.driver.quit()


