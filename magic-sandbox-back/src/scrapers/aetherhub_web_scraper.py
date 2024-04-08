from bs4 import BeautifulSoup
import requests
import uuid
from .scraper import Scraper
from ..models.card import Card
from ..models.deck import Deck
from ..constants import DEFAULT_CARD_BACK_URL

class AetherhubWebScraper(Scraper):

    def get_deck(self, url: str):
        card_map_data = self.get_aetherhub_data(url)
        return self.process_aetherhub_card_map_into_deck(card_map_data)

    def get_aetherhub_data(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors

            soup = BeautifulSoup(response.content, 'html.parser')

            cards_info = []

            self.add_cards_from_aetherhub(cards_info, soup)
            
            return cards_info
        except Exception as e:
            print(f"Error: {e}")

    def add_cards_from_aetherhub(self, cards_info, soup):
        # Find the first 'h5' with "Maybeboard" or "Sideboard"
        stop_section = soup.find('h5', string=lambda text: "maybeboard" in text.lower() or "sideboard" in text.lower())

        # If such a section exists, create a new soup from the beginning up to this point to exclude cards from maybeboard or sideboard
        if stop_section:
            stop_index = str(soup).find(str(stop_section))
            new_html = str(soup)[:stop_index]
            soup = BeautifulSoup(new_html, 'html.parser')

        # the img tag provides everything we need
        # every img of a card is repeated if it has multiple occurences
        card_map = soup.select('div[id*="tab_visual_"] img')
        for idx,card in enumerate(card_map):
            # Image alt for card name, data-src for the url
            card_name = card['alt']
            card_image = card['data-src']
            
            # Initialize card_info with details from the first side
            card_info = {
                'name': card_name,
                'image_url': card_image,
                'quantity': 1,
                'flip_image_url': DEFAULT_CARD_BACK_URL
            }

            # commander is always first in scrapped cards
            if len(card_map) >= 100 and idx==0:
                card_info['commander'] = True

            # todo: flipside

            cards_info.append(card_info)
    
    def process_aetherhub_card_map_into_deck(self, card_map):
        try:
            cards = []
            for card_data in card_map:
                card = Card(id=str(uuid.uuid4()), name=card_data["name"], image=card_data["image_url"], flip_image=card_data['flip_image_url'])
                # adding commander on the top of the deck if it exists
                if "commander" in card_data:
                    card.commander = True
                    cards.insert(0,card)
                    print("commander found")
                else:    
                    cards.append(card)
            deck = Deck(cards=cards)
            return deck
        except Exception as e:
            print("exception" + e)