from bs4 import BeautifulSoup
import requests
import uuid
from .scraper import Scraper
from ..models.card import Card
from ..models.deck import Deck
from ..constants import DEFAULT_CARD_BACK_URL

class TappedOutWebScraper(Scraper):

    def get_deck(self, url: str):
        card_map_data = self.get_tapped_out_data(url)
        return self.process_tapped_out_card_map_into_deck(card_map_data)

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
                            'flip_image_url': DEFAULT_CARD_BACK_URL
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
                            'flip_image_url': DEFAULT_CARD_BACK_URL
                        })
    
    def process_tapped_out_card_map_into_deck(self, card_map):
        try:
            cards = []
            for card_data in card_map:
                # if a card has multiple occurences there is only one entry in card map but the qty is set to the number
                for i in range(int(card_data["quantity"])):
                    card = Card(id=str(uuid.uuid4()), name=card_data["name"], image=card_data["image_url"], flip_image=card_data['flip_image_url'])
                    cards.append(card)
            deck = Deck(cards=cards)
            return deck
        except Exception as e:
            print("exception" + e)