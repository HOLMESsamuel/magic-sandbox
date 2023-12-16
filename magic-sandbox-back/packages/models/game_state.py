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

def move_card_from_deck_to_board(player):
    if player["deck"]:
        card = player["deck"]["cards"].pop(0)  # Remove the first card from the deck
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
