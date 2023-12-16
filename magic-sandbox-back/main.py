import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from packages.services.websocket_manager import WebSocketManager
from packages.services.state_manager import StateManager
from packages.models.game_state import *
from packages.services.rest import router as rest_router
from fastapi.encoders import jsonable_encoder

app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# includes endpoints from rest.py in /services
app.include_router(rest_router)

state_manager = StateManager()
websocket_manager = WebSocketManager()


@app.websocket("/ws/{group_id}/{name}")
async def websocket_endpoint(websocket: WebSocket, group_id: str, name: str):
    await websocket.accept()

    websocket_manager.add_connection(group_id, websocket)

    # Initialize or update the game state
    if not state_manager.get_group_state(group_id):
        # Initialize new game state and add player
        game_state = create_game_state()
        add_player_to_game_state_if_not_exist(game_state, name)
        state_manager.update_group_state(group_id, game_state)
    else:
        # Update existing game state
        state = state_manager.get_group_state(group_id)
        add_player_to_game_state_if_not_exist(state, name)

    # Broadcast the current state
    await websocket_manager.broadcast(group_id, jsonable_encoder(state_manager.get_group_state(group_id)))

    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_json()
            state_manager.update_group_state(group_id, data)
            await websocket_manager.broadcast(group_id, jsonable_encoder(state_manager.get_group_state(group_id)))
    except Exception as e:
        print(e)
        pass


