from contextlib import asynccontextmanager
import os
import shutil
import asyncio
import logging
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import validator
from src.services.websocket_manager import WebSocketManager
from src.services.state_manager import StateManager
from src.models.game_state import *
from src.routes.board_routes import router as board_router
from src.routes.deck_routes import router as deck_router
from src.routes.card_routes import router as card_router
from src.routes.token_routes import router as token_router
from src.routes.hand_routes import router as hand_router
from src.routes.graveyard_routes import router as graveyard_router
from src.routes.player_routes import router as player_router

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from src.services import WebScraperService
from src.services import GameService

driver = None


app = FastAPI()


@app.on_event("startup")
def startup_event():
    global driver
    logging.info("load the webdriver before start up")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    logging.info("webdriver loaded")

@app.on_event("shutdown")
def shutdown_event():
    global driver
    driver.quit()

def get_driver():
    global driver
    if driver is None:
        raise HTTPException(status_code=500, detail="WebDriver not initialized")
    return driver

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
app.include_router(player_router)

def mount_empty_uploads_folder(upload_folder_name: str):
    if os.path.exists(upload_folder_name):
        shutil.rmtree(upload_folder_name)
    os.makedirs(upload_folder_name, exist_ok=True)
    # Mount a static files directory, accessible at '/static' URL path
    app.mount("/static", StaticFiles(directory=upload_folder_name), name="static")

mount_empty_uploads_folder("uploads")

state_manager = StateManager()
websocket_manager = WebSocketManager()
web_scraper_service = WebScraperService()
game_service = GameService()

class DeckInput(BaseModel):
    url: str

    @validator('url')
    def url_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('URL must not be empty')
        return v

@app.post("/room/{roomId}/player/{playerId}/deck")
async def scrap_deck(playerId: str, roomId: str, deck_input: DeckInput, driver: webdriver.Chrome = Depends(get_driver)):
    try:
        web_scraper = web_scraper_service.get_scraper(deck_input.url, driver)
        get_deck_task = asyncio.create_task(web_scraper.get_deck(deck_input.url))
        deck = await get_deck_task
        response = await game_service.add_deck(playerId, roomId, deck)
        return response
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")


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

    remove_player_background_image(roomId, playerId)

    await websocket_manager.broadcast(roomId, game_state)

def remove_player_background_image(roomId, playerId):
    file_location = f"uploads/{roomId}/{playerId}/"
    if os.path.exists(file_location):
        shutil.rmtree(file_location)

