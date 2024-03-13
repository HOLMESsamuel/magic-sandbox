import uuid
from .hand import Hand
from .deck import Deck
from .board import Board
from .card import Card
from .token import Token
from pydantic import BaseModel, Field

class Player(BaseModel):
    name : str
    score: int = 20
    index: int = 0
    hand: Hand = Field(default_factory=Hand)
    deck: Deck = Field(default_factory=Deck)
    board: Board = Field(default_factory=Board)

    def get_card(self, cardId) -> Card:
        for index, card in enumerate(self.hand.cards):
            if card.id == cardId:
                return card
        for index, card in enumerate(self.board.cards):
            if card.id == cardId:
                return card
        return None
        

    def draw_card(self):
        if self.deck.cards and len(self.deck.cards) > 0:
            card = self.deck.cards.pop(0)
            self.hand.cards.append(card)
        else:
            print("The deck is empty, no card to move.")

    def reset(self):
        self.score = 20
        self.hand.reset()
        self.deck.reset()
        self.board.reset()

    def play_card(self, cardId, position, max_z_index):
        for index, card in enumerate(self.hand.cards):
            if card.id == cardId:
                removed_card : Card = self.hand.cards.pop(index)
                removed_card.position = position
                removed_card.z_index = max_z_index
                self.board.cards.append(removed_card)
                break

    def mulligan(self):
        if self.deck:
            self.deck.cards.extend(self.hand.cards)
            self.hand.cards = []
            self.deck.shuffle()

    def mill_card(self):
        if self.deck:
            card = self.deck.cards.pop(0)  
            if self.index == 0:
                card.position = {'x': 2400, 'y': 610}
            elif self.index == 1:
                card.position  = {'x': 50, 'y': -890}
            elif self.index == 2:
                card.position  = {'x': -2400, 'y': -890}
            elif self.index == 3:
                card.position  = {'x': -250, 'y': 610}
            self.board.cards.append(card)
        else:
            print("The deck is empty, no card to move.")
    
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
        if self.deck:
            for index, card in enumerate(self.deck.cards):
                if card.id == cardId:
                    card = self.deck.cards.pop(index)
                    self.hand.cards.append(card)
                    break
        else:
            print("The deck is empty, no card to move.")

    def move_card_to_deck(self, cardId, cardPosition):
        if self.hand:
            for index, card in enumerate(self.hand.cards):
                if card.id == cardId:
                    card = self.hand.cards.pop(index)
                    self.deck.cards.insert(cardPosition, card)
                    break
        if self.board:
            for index, card in enumerate(self.board.cards):
                if card.id == cardId:
                    card = self.board.cards.pop(index)
                    self.deck.cards.insert(cardPosition, card)
                    break
        
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
        
        token = Token(id=str(uuid.uuid4()), text=text, position=position, max_z_index = max_z_index, type = type)
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