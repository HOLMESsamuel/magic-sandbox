import uuid
from .hand import Hand
from .deck import Deck
from .board import Board
from .card import Card
from .token import Token
from .graveyard import Graveyard
from pydantic import BaseModel, Field
import copy

class Player(BaseModel):
    name : str
    score: int = 40
    index: int = 0
    hand: Hand = Field(default_factory=Hand)
    deck: Deck = Field(default_factory=Deck)
    board: Board = Field(default_factory=Board)
    graveyard: Graveyard = Field(default_factory=Graveyard)
    background: str = ""
    background_width: int = 3000
    background_height: int = 1500

    def get_card(self, cardId) -> Card:
        hand_card : Card = self.hand.get_card(cardId)
        if hand_card:
            return hand_card
        board_card : Card = self.board.get_card(cardId)
        if board_card:
            return board_card
        return None
    
    def pop_card(self, cardId) -> Card:
        if self.hand:
            for index, card in enumerate(self.hand.cards):
                if card.id == cardId:
                    return self.hand.cards.pop(index)
                    
        if self.board:
            for index, card in enumerate(self.board.cards):
                if card.id == cardId:
                    return self.board.cards.pop(index)
        

    def draw_card(self):
        if self.deck and self.deck.cards and len(self.deck.cards) > 0:
            card = self.deck.cards.pop(0)
            self.hand.cards.append(card)
        else:
            print("The deck is empty, no card to move.")

    def draw_commander(self):
        if self.deck and self.deck.cards and len(self.deck.cards) > 0:
            for index, card in enumerate(self.deck.cards):
                if card.commander == True:   
                    if self.index == 0:
                        card.position = {'x': 800, 'y': 200}
                    if self.index == 1:
                        card.position = {'x': 1650, 'y': -480}
                    if self.index == 2:
                        card.position = {'x': -800, 'y': -480}
                    if self.index == 3:
                        card.position = {'x': -1850, 'y': 200}  
                    self.board.cards.append(self.deck.cards.pop(index) )
                    return
        else:
            print("The deck is empty, no card to move.")        

    def reset(self):
        self.score = 20
        self.hand.reset()
        self.deck.reset()
        self.graveyard.reset()
        self.board.reset()

    def play_card(self, cardId, position, max_z_index):
        for index, card in enumerate(self.hand.cards):
            if card.id == cardId:
                removed_card : Card = self.hand.cards.pop(index)
                removed_card.position = position
                removed_card.z_index = max_z_index
                self.board.cards.append(removed_card)
                break

    def copy_card(self, cardId, max_z_index):
        for index, card in enumerate(self.board.cards):
            if card.id == cardId:
                copied_card : Card = copy.deepcopy(self.board.cards[index])
                copied_card.id = str(uuid.uuid4())
                copied_card.position['x'] = copied_card.position['x'] + 250
                copied_card.z_index = max_z_index
                copied_card.is_copy = True
                self.board.cards.append(copied_card)
                break

    def mulligan(self):
        if self.deck:
            self.deck.cards.extend(self.hand.cards)
            self.hand.cards = []
            self.deck.shuffle()

    def mill_card(self):
        if self.deck:
            card = self.deck.cards.pop(0)  
            self.graveyard.cards.append(card)
    
    def flip_card(self, cardId):
        board_card = self.board.get_card(cardId)
        if board_card:
            board_card.flip()
            return
        
        hand_card = self.hand.get_card(cardId)
        if hand_card:
            hand_card.flip()
            return
        
    def move_card_from_deck_to_hand(self, cardId):
        card = self.deck.pop_card(cardId)
        if card:
            self.hand.cards.append(card)

    def move_card_to_deck(self, cardId, cardPosition):
        card = self.pop_card(cardId)
        card.tapped = False
        if card:
            self.deck.cards.insert(cardPosition, card)
        
    def create_token(self, text, type, max_z_index):
        #set the position to the center of the player's board
        if self.index == 0:
            position = {"x": 1410, "y": 614}
        elif self.index == 1:
            position = {"x": 964, "y": -820}
        elif self.index == 2:
            position = {"x": -1416, "y": -820}
        else:
            position = {"x": -1196, "y": 614}
        
        token = Token(id=str(uuid.uuid4()), text=text, position=position, z_index = max_z_index, type = type)
        self.board.tokens.append(token)

    def delete_token(self, tokenId):
        if self.board:
            for index, token in enumerate(self.board.tokens):
                if token.id == tokenId:
                    del self.board.tokens[index]
                    break
        else:
            print("The board is empty, no token to delete.")

    def modify_token(self, tokenId, text, type):
        if self.board:
            for index, token in enumerate(self.board.tokens):
                if token.id == tokenId:
                    self.board.tokens[index].text = text
                    self.board.tokens[index].type = type
                    break
        else:
            print("The board is empty, no token to delete.")

    def copy_token(self, tokenId):
        if self.board:
            for index, token in enumerate(self.board.tokens):
                if token.id == tokenId:
                    copy_token = copy.deepcopy(self.board.tokens[index])
                    copy_token.id = str(uuid.uuid4())
                    copy_token.position['x'] = copy_token.position['x'] + 250
                    self.board.tokens.append(copy_token)
                    break
        else:
            print("The board is empty, no token to delete.")

    def add_background(self, file_path, width, height):
        self.background = file_path
        self.background_width = width
        self.background_height = height

    def remove_background(self):
        self.background = ''