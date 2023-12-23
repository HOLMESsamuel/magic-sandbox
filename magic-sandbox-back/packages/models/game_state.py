import random

def create_game_state():
    return {
        "players": []
    }

def add_player_to_game_state_if_not_exist(game_state, player_name):
    for player in game_state["players"]:
        if player["name"] == player_name:
            return
    game_state["players"].append(create_player(player_name))

def get_player_from_game_state(game_state, player_name):
    for player in game_state["players"]:
        if player["name"] == player_name:
            return player
    return None

def create_player(name):
    return {
        "name": name,
        "hand": [],
        "deck": [],
        "board": []
    }

def move_card_from_deck_to_board(player, playerIndex):
    if player["deck"]:
        card = player["deck"]["cards"].pop(0)  
        if playerIndex == 0:
            card["position"] = {'x': 2400, 'y': 610}
        elif playerIndex == 1:
            card["position"] = {'x': 50, 'y': -890}
        elif playerIndex == 2:
            card["position"] = {'x': -2400, 'y': -890}
        elif playerIndex == 3:
            card["position"] = {'x': -250, 'y': 610}
        player["board"].append(card)  # Add the card to the board
    else:
        print("The deck is empty, no card to move.")

def move_card_from_deck_to_hand(player):
    if player["deck"]:
        card = player["deck"]["cards"].pop(0)  # Remove the first card from the deck
        player["hand"].append(card)  # Add the card to the hand
    else:
        print("The deck is empty, no card to move.")

def update_player_score(player, score):
    player['score'] = score

def tap_card(player, cardId):
    for index, card in enumerate(player["board"]):
        if card["id"] == cardId:
            player["board"][index]["tapped"] = True
            break

def untap_card(player, cardId):
    for index, card in enumerate(player["board"]):
        if card["id"] == cardId:
            player["board"][index]["tapped"] = False
            break

def get_player_index(game_state, player_id):
    for index, player in enumerate(game_state["players"]):
        if player["name"] == player_id:
            return index
    return None

def play_card(player, cardId, position):
    for index, card in enumerate(player["hand"]):
        if card["id"] == cardId:
            removed_card = player["hand"].pop(index)
            removed_card["position"] = position
            player["board"].append(removed_card)
            break

def shuffle_deck(player):
    random.shuffle(player["deck"]["cards"])
