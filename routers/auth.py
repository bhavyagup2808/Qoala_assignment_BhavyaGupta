from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta, datetime
import pymongo
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated, Optional
from models.request_models import CreateUserRequest
from models.response_models import TokenResponse
from jose import jwt, JWTError
from models.db_models import User
import os
from dotenv import load_dotenv
load_dotenv()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

SECRET_KEY=os.environ["SECRET_KEY"]
ALGORITHM=os.environ["ALGORITHM"]

def get_mongo_client():
    uri = os.environ["MONGODB_URL"]
    return pymongo.MongoClient(uri)

client = get_mongo_client()
USER_COLLECTION = client[os.environ["DATABASE"]]["user"]

try:
    client.admin.command('ping')
    print("Auth connected to MongoDB!")
except Exception as e:
    print(e)

@router.post("/sign-up", status_code=status.HTTP_201_CREATED) 
async def sign_up_user(createUserRequest: CreateUserRequest):
    user = USER_COLLECTION.find_one({'email': createUserRequest.email})
    if user:
        raise HTTPException(status_code=401, detail="user already exists")
    user = User(
        name=createUserRequest.name,
        email=createUserRequest.email,
        hashed_password=bcrypt_context.hash(createUserRequest.password),
        role="user"
    )
    if user.name=="" or user.email=="":
        raise HTTPException(detail="name or email can not empty", status_code=status.HTTP_400_BAD_REQUEST)
    USER_COLLECTION.insert_one(user.__dict__)


