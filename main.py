from fastapi import FastAPI ,HTTPException ,status, Depends
from models import VideoData,UserCreate
from sqlmodel import  Session,select
from db import get_session, create_db_and_tables
from passlib.context import CryptContext
from schemas.user import UserTable
from schemas.videos import VideosTable
from sqlalchemy.exc import IntegrityError
import  datetime
app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/connection")
async def check_connection(session :Session = Depends(get_session)):
    return "DB session is successfully created"

def hash_password(plain_password:UserCreate) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password:UserCreate,stored_hash:str)-> bool:
    return pwd_context.verify(plain_password,stored_hash)

@app.post("/create_user/")
async def create_user(user_data:UserCreate, session:Session=Depends(get_session)):
    db_user = UserTable(
        username = user_data.username,
        email = user_data.email,
        created_at = datetime.datetime.utcnow(),
        password = 
    )
    existing_username = session.exec(
        select(UserTable).where(UserTable.username==user_data.username)
    ).first
    if existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = "Username already taken")
    existing_email = session.exec(
        select(UserTable).where(UserTable.email == user_data.email)
    ).first
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = "Email already taken")
    
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = "Username or Email already exists",
        )

@app.get("/")
@app.post("/upload/")
async def video_upload(vid_data:VideoData):
    

@app.get("/videos/{video_id}")
async def get_video(video_id:int):
    for video in video_db:
        if video.get(video_id) == video_id:
            return {"vid_id": video_id}
