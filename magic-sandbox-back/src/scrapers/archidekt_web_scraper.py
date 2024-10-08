from concurrent.futures import ThreadPoolExecutor
import uuid
import asyncio
import requests
from bs4 import BeautifulSoup
import json
import re
import time
from .scraper import Scraper
from ..models.card import Card
from ..models.deck import Deck

executor = ThreadPoolExecutor()

class ArchidektWebScraper(Scraper):

    async def get_deck(self, url: str):
        loop = asyncio.get_event_loop()
        try:
            card_map_data, soup = await loop.run_in_executor(executor, self.get_archidekt_data, url)
            return self.process_archidekt_card_map_into_deck(card_map_data, soup)
        except Exception as e:
            print(f"Error: {e}")

    def get_dynamic_content(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for the page to load.

            # Get the page source and parse it with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            return soup
        except Exception as e:
            print(f"Error: {e}")


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
        except Exception as e:
            print(f"Error: {e}")


    def process_archidekt_card_map_into_deck(self, card_map, soup):
        try:
            card_image_divs = soup.find_all('img', id='basicCardImage')
            cards = []
            command_terms = {"Commander", "commander", "commandant", "Commandant"}
            maybe_terms = {"Maybeboard", "maybeboard", "sideboard", "Sideboard"}
            for key, value in card_map.items():
                if not any(term in value["categories"] for term in maybe_terms): #filter cards that are in the maybeboard
                    
                    matching_divs = self.find_best_matching_image_divs(value.get('name'), card_image_divs)
                    
                    if matching_divs:
                        img_urls = [img['src'] for img in matching_divs if img.has_attr('src')]
                        # If there's only one img, we fetch its src for the image
                        # If there are two imgs, it means the card has two sides and we need both srcs
                        # Adjust the Card constructor call based on your Card class' requirements
                        for i in range(value.get('qty')): 
                            card = Card(id=str(uuid.uuid4()), name=value.get('name'), image='', types=value.get("types"))  
                            if len(img_urls) == 1:
                                card.image = img_urls[0]
                            if len(img_urls) == 2:
                                card.flip_image = img_urls[1]
                            #for basic lands if there are multiples differents images it is not a double side card
                            if len(img_urls) > 2:
                                card.image = img_urls[0]
                            # adding commander if it exists
                            if any(term in value["categories"] for term in command_terms):
                                card.commander = True
                            cards.append(card)
            deck = Deck(cards=cards)
            return deck
        except Exception as e:
            print(e)

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
        
    def find_best_matching_image_divs(self, name, card_image_divs):
        best_matches = []
        max_score = 0
        for div in card_image_divs:
            name_words = name.lower().split()
            title_words = div['title'].lower().split()
            score = 0
            # Use a sliding window to match word sequences
            for i in range(len(title_words) - len(name_words) + 1):
                if title_words[i:i+len(name_words)] == name_words:
                    score = len(name_words)  # Score by the number of matched words in sequence
                    break
            if score > max_score:
                max_score = score
                best_matches = [div]  # Reset the best_matches list with the new best match
            elif score == max_score and score != 0:
                best_matches.append(div)  # Append to best_matches only if score equals max_score and is not zero
        return best_matches