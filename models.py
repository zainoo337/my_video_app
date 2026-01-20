from pydantic import BaseModel ,EmailStr
   

class VideoData(BaseModel):
    video_id: int
    title: str
    playback_url: str
    owner_id: int
    is_published: bool = False
    
class UserCreate(BaseModel):
    username:str
    email : EmailStr
    plain_password : str

class UserOut(BaseModel):
    id : int
    name :str
    email : EmailStr
    is_active : bool
    plain_password :str
    
class VideoOut(BaseModel):
    video_id : int
    owner_id : int
    title : str
    playback_url : str
    is_published : bool
