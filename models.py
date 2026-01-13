from pydantic import BaseModel

class videoData(BaseModel):
    title:str
    video_id:int
    is_published:bool = False
    playback_url : str
    
class UserCreate(BaseModel):
    name:str
    id:int
    is_active:bool = False
