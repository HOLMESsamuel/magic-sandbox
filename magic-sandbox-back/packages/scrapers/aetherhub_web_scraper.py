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
        # All cards can be found under the tab_visual div
        print(soup.select('div[id*="tab_visual_"]'))

        # the img tag provides everything we need
        # every img of a card is repeated if it has multiple occurences
        for card in soup.select('div[id*="tab_visual_"] img'):
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

            # todo: flipside

            # Append the card_info to cards_info
            cards_info.append(card_info)
    
    def process_aetherhub_card_map_into_deck(self, card_map):
        try:
            cards = []
            for card_data in card_map:
                # if a card has multiple occurences there is only one entry in card map but the qty is set to the number
                card = Card(str(uuid.uuid4()), card_data["name"], "type", card_data["image_url"], card_data['flip_image_url'])
                cards.append(card)
            deck = Deck(cards)
            return deck
        except Exception as e:
            print("exception" + e)