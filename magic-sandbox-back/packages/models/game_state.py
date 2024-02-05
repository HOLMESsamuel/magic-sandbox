import random
import uuid

def create_game_state():
    return {
        "players": [],
        "max_z_index": 1,
        "alertMessage": ""
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
        "deck": {"cards": []},
        "board": {"cards": [], "tokens": []}
    }

def reset_player(player):
    player["deck"]["cards"] = []
    player["hand"] = []
    player["board"]["cards"] = []
    player["board"]["tokens"] = []

def add_deck(player, deck):
    player["deck"]["cards"] = deck.cards_to_dict()

def throw_dice(game_state, player, dice_result, dice_value):
    game_state["alertMessage"] = player["name"] + " threw a dice: " + str(dice_result) + "/" + str(dice_value)

def mill_card(player, playerIndex):
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
        player["board"]["cards"].append(card)  # Add the card to the board
    else:
        print("The deck is empty, no card to move.")

def draw_card(player):
    if player["deck"]:
        card = player["deck"]["cards"].pop(0)  # Remove the first card from the deck
        player["hand"].append(card)  # Add the card to the hand
    else:
        print("The deck is empty, no card to move.")

def move_card_from_deck_to_hand(player, cardId):
    if player["deck"]:
        for index, card in enumerate(player["deck"]["cards"]):
            if card["id"] == cardId:
                card = player["deck"]["cards"].pop(index)
                player["hand"].append(card)
                break
    else:
        print("The deck is empty, no card to move.")

def move_card_from_board_to_hand(player, cardId, target_player):
    if player["board"]:
        for index, card in enumerate(player["board"]["cards"]):
            if card["id"] == cardId:
                card = player["board"]["cards"].pop(index)
                card["tapped"] = False
                target_player["hand"].append(card)
                break
    else:
        print("The board is empty, no card to move.")

def move_card_from_hand_to_hand(player, cardId, target_player):
    if player["hand"]:
        for index, card in enumerate(player["hand"]):
            if card["id"] == cardId:
                card = player["hand"].pop(index)
                target_player["hand"].append(card)
                break
    else:
        print("The hand is empty, no card to move.")

def move_card_to_deck(player, cardId, cardPosition):
    if player["hand"]:
        for index, card in enumerate(player["hand"]):
            if card["id"] == cardId:
                card = player["hand"].pop(index)
                player["deck"]["cards"].insert(cardPosition, card)
                break
    else:
        print("The hand is empty, no card to move.")

def update_player_score(player, score):
    player['score'] = score

def tap_card(player, cardId):
    for index, card in enumerate(player["board"]["cards"]):
        if card["id"] == cardId:
            player["board"]["cards"][index]["tapped"] = True
            break

def untap_card(player, cardId):
    for index, card in enumerate(player["board"]["cards"]):
        if card["id"] == cardId:
            player["board"]["cards"][index]["tapped"] = False
            break

def tap_token(player, tokenId):
    for index, token in enumerate(player["board"]["tokens"]):
        if token["id"] == tokenId:
            player["board"]["tokens"][index]["tapped"] = True
            break

def untap_token(player, tokenId):
    for index, token in enumerate(player["board"]["tokens"]):
        if token["id"] == tokenId:
            player["board"]["tokens"][index]["tapped"] = False
            break

def detap_all(player):
    for index, card in enumerate(player["board"]["cards"]):
        player["board"]["cards"][index]["tapped"] = False
    for index, token in enumerate(player["board"]["tokens"]):
        player["board"]["tokens"][index]["tapped"] = False

def mulligan(player):
    if player["deck"]:
        player["deck"]["cards"].extend(player["hand"])
        player["hand"] = []
        shuffle_deck(player)

def get_player_index(game_state, player_id):
    for index, player in enumerate(game_state["players"]):
        if player["name"] == player_id:
            return index
    return None

def play_card(player, cardId, position, max_z_index):
    for index, card in enumerate(player["hand"]):
        if card["id"] == cardId:
            removed_card = player["hand"].pop(index)
            removed_card["position"] = position
            removed_card["z_index"] = max_z_index
            player["board"]["cards"].append(removed_card)
            break

def shuffle_deck(player):
    random.shuffle(player["deck"]["cards"])

def create_token(player, text, type, max_z_index, player_index):
    #set the position to the center of the player's board
    if player_index == 0:
        position = {"x": 1410, "y": 614}
    elif player_index == 1:
        position = {"x": 964, "y": -820}
    elif player_index == 2:
        position = {"x": -1416, "y": -820}
    else:
        position = {"x": -1196, "y": 614}
    token = {
        "id": str(uuid.uuid4()),
        "text": text,
        "position": position,
        "z_index": max_z_index,
        "type": type
    }
    player["board"]["tokens"].append(token)

def delete_token(player, id):
    if player["board"]:
        for index, token in enumerate(player["board"]["tokens"]):
            if token["id"] == id:
                del player["board"]["tokens"][index]
                break
    else:
        print("The board is empty, no token to delete.")

def modify_token(player, id, text, type):
    if player["board"]:
        for index, token in enumerate(player["board"]["tokens"]):
            if token["id"] == id:
                player["board"]["tokens"][index]["text"] = text
                player["board"]["tokens"][index]["type"] = type
                break
    else:
        print("The board is empty, no token to delete.")


