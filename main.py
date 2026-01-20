from fastapi import FastAPI ,HTTPException ,status, Depends
from models import VideoData,UserCreate,UserOut
from sqlmodel import  Session,select
from db import get_session, create_db_and_tables
import bcrypt
from schemas.user import UserTable
from schemas.videos import VideosTable
from sqlalchemy.exc import IntegrityError
import  datetime
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/connection")
async def check_connection(session :Session = Depends(get_session)):
    return "DB session is successfully created"

def validate_password(plain_password:str):
    if not isinstance(plain_password,str):
        raise TypeError("Password must be a string")
    if len(plain_password) <8:
        raise ValueError("Password must be at least 8 characters long")
    

def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str,stored_hash:str)->bool:
    plain_password_bytes = plain_password.encode('utf-8')
    stored_hash_bytes = stored_hash.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes, stored_hash_bytes)


@app.post("/create_user/")
async def create_user(user_data:UserCreate, session:Session=Depends(get_session)):
        try:
            validate_password(user_data.plain_password)
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        try:
            hashed_pw = hash_password(user_data.plain_password)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error hashing password"
            )
        db_user = UserTable(
        username = user_data.username,
        email = user_data.email,
        created_at = datetime.datetime.utcnow(),
        password = hashed_pw
        )
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
        return {
        "success": True,
        "message": "User created successfully",
        "user": {
            "user_id": db_user.user_id,
            "username": db_user.username,
            "email": db_user.email,
            "created_at": db_user.created_at,
            "is_active": db_user.is_active
        }
    }

@app.post("/login")
async def user_login(user_data:UserOut,session:Session = Depends(get_session)):
    existing_user = session.exec(
        select(UserTable).where(UserTable.username ==user_data.name)
    ).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = "Invalid username or password")
    if not verify_password(user_data.plain_password , existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = "Invalid Username or Password")
    return {
        "message" : "Login Successfully",
        "user_id" : existing_user.user_id,
        "is_active" : True
    }