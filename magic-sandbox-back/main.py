from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from src.services.websocket_manager import WebSocketManager
from src.services.state_manager import StateManager
from src.models.game_state import *
from src.routes.board_routes import router as board_router
from src.routes.deck_routes import router as deck_router
from src.routes.card_routes import router as card_router
from src.routes.token_routes import router as token_router
from src.routes.hand_routes import router as hand_router
from src.routes.graveyard_routes import router as graveyard_router

app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# includes endpoints from routes package
app.include_router(board_router)
app.include_router(deck_router)
app.include_router(card_router)
app.include_router(token_router)
app.include_router(hand_router)
app.include_router(graveyard_router)

state_manager = StateManager()
websocket_manager = WebSocketManager()


@app.websocket("/ws/{group_id}/{name}")
async def websocket_endpoint(websocket: WebSocket, group_id: str, name: str):
    await websocket.accept()

    websocket_manager.add_connection(group_id, websocket)

    game_state = state_manager.get_group_state(group_id)

    if game_state is None:
        game_state = GameState()

    game_state.add_player_if_not_exist(name)

    state_manager.update_group_state(group_id, game_state)

    await websocket_manager.broadcast(group_id, game_state)

    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_json()
            game_state = GameState.model_validate(data)
            state_manager.update_group_state(group_id, game_state)
            await websocket_manager.broadcast(group_id, game_state)
    except WebSocketDisconnect:
        # triggered when the ws is closed
        print(f"{name} disconnected")
        websocket_manager.remove_connection(group_id, websocket)

@app.delete("/room/{roomId}/player/{playerId}")
async def disconnect_player(roomId: str, playerId: str):
    game_state : GameState = state_manager.get_group_state(roomId)
    game_state.remove_player(playerId)
    await websocket_manager.broadcast(roomId, game_state)




