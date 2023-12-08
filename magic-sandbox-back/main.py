from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from packages.services.rest import router as rest_router
from typing import Dict, List

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# includes endpoints from rest.py in /services
app.include_router(rest_router)

# Dictionary mapping group IDs to lists of WebSocket connections
connected_groups: Dict[str, List[WebSocket]] = {}

# Dictionary to store the state for each group
group_states: Dict[str, Dict[str, int]] = {}


@app.websocket("/ws/{group_id}")
async def websocket_endpoint(websocket: WebSocket, group_id: str):
    await websocket.accept()

    # Initialize the list and state for new group IDs
    if group_id not in connected_groups:
        connected_groups[group_id] = []
        group_states[group_id] = {"x": 100, "y": 100}  # Default state, can be changed

    # Add the current websocket to the list of connected clients for this group
    connected_groups[group_id].append(websocket)

    # Send the current state to the newly connected client
    await websocket.send_json(group_states[group_id])

    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_json()
            if "x" in data and "y" in data:
                # Update the position for the group and broadcast it
                group_states[group_id] = {"x": data["x"], "y": data["y"]}
                await broadcast_position(group_id, group_states[group_id])
    except Exception as e:
        print(e)
        pass
    finally:
        # Remove client from the list upon disconnection
        connected_groups[group_id].remove(websocket)
        if not connected_groups[group_id]:
            # Remove the group_id key if no more connected clients
            del connected_groups[group_id]
            del group_states[group_id]  # Also remove the state for the group


async def broadcast_position(group_id: str, position: Dict[str, int]):
    # Broadcast the current state to all connected clients in the same group
    for client in connected_groups.get(group_id, []):
        try:
            await client.send_json(position)
        except Exception:
            # Handle failed send (e.g., client disconnected)
            pass
