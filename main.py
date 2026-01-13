from typing import Union
from fastapi import FastAPI ,HTTPException
from models import videoData,UserCreate
from typing import List

app = FastAPI()

video_db = []
users_db = []

@app.post("/create_user/")
async def create_user(user_data:UserCreate):
    id = user_data.id
    name = user_data.name
    users_db.append(user_data)
    
    return {
        "user": "successfully created",
        "user_id" : id,
        "username": name,
    }
@app.post("/upload/")
async def video_upload(vid_data:videoData):
    title = vid_data.title
    video_id = vid_data.video_id
    playback_url = vid_data.playback_url
    video_db.append(vid_data)
    return{
        "msg": "video successfully upload",
        "video_title": title,
        "video_id" : video_id,
        "playback_url" : playback_url
    }

@app.get("/videos/{video_id}")
async def get_video(video_id:int):
    