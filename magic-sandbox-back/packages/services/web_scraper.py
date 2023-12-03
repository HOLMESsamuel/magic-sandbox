import requests
from bs4 import BeautifulSoup
import json

from ..models.card import Card
from ..models.deck import Deck

class WebScraper:

    def get_deck(self, url: str):
        card_map_data = self.get_data(url)
        return self.process_card_map_into_deck(card_map_data)

    def get_data(self, url: str):
        try:
            print(url)
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors

            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the script tag with the JSON content
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            if not script_tag:
                print("Script tag with JSON not found.")
                return None

            # Extract JSON from the script tag
            json_data = json.loads(script_tag.string)

            # Navigate to the desired data
            card_map = json_data.get('props', {}).get('pageProps', {}).get('redux', {}).get('deck', {}).get('cardMap', {})
            return card_map
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def process_card_map_into_deck(self, card_map):
        cards = []
        for key, value in card_map.items():
            cards.append(Card(key, value.get('name'), value.get('typeCategory'), value.get('scryfallImageHash')))
        deck = Deck(cards)
        return deck


