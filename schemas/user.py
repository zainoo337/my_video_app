from typing import Optional
from sqlmodel import SQLModel, Field
import datetime

class UserTable(SQLModel, table = True):
    user_id : Optional[int] = Field(default=None, primary_key=True)
    username :str = Field(unique= True,index=True)
    email: str = Field(unique = True, index = True)
    password: str
    created_at: datetime.datetime
    is_active:bool = Field(default = True)
    