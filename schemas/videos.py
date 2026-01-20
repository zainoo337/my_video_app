from typing import Optional
from sqlmodel import SQLModel, Field
from user import UserTable
import datetime


class VideosTable(SQLModel,table = True):
    video_id : Optional[int] = Field(primary_key=True, default = None,index = True)
    owner_id : int = Field(foreign_key= "UserTable.id" , default = None)
    title : str = Field(unique = True, index = True )
    video_description: str
    uploaded_at : datetime.datetime
    playback_url: str = Field (unique = True)
    is_published: bool = Field(default = True)
    