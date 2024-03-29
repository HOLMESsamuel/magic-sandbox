import os
import shutil
from click import File
from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import JSONResponse
from ..services.game_service import GameService

router = APIRouter()
game_service = GameService()

@router.post("/room/{room_id}/player/{user_name}/background")
async def upload_background(room_id: str, user_name: str, file: UploadFile = File(...), width: int = Form(...), height: int = Form(...)):
    file_location = f"uploads/{room_id}/{user_name}/"

    # Check if the directory exists, remove it if it does
    if os.path.exists(file_location):
        shutil.rmtree(file_location)
    
    # Create the directory again
    os.makedirs(file_location, exist_ok=True)
    
    full_file_path = os.path.join(file_location, file.filename)

    # Write the uploaded file to the new location
    with open(full_file_path, "wb+") as file_object:
        file_object.write(await file.read())

    file_exposed_location = f"static/{room_id}/{user_name}/{file.filename}"

    await game_service.add_player_background(room_id, user_name, file_exposed_location,width, height)

    return JSONResponse(status_code=200, content={"message": "File uploaded successfully", "file_path": full_file_path})

@router.delete("/room/{room_id}/player/{user_name}/background")
async def delete_background(room_id: str, user_name: str):
    response = await game_service.remove_player_background(room_id, user_name)
    return response