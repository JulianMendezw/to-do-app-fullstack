import bcrypt
from typing import Union
from pydantic import BaseModel
from typing_extensions import Annotated
from datetime import datetime, timedelta
from app.models import User, UserLogging
from db.supabase import create_supabase_client
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

app = FastAPI()

# Initialize supabase client
supabase = create_supabase_client()

oauth2_scheme = OAuth2PasswordBearer("/token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "27bc57a3b8df8d18c14f3d59278857e5ddc2bfd812b89ef444ce39a56e39895c"
ALGORITHM = "HS256"


def user_exists(key: str = "user_name", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_user_data(username: str):
    user = (
        supabase.from_("users")
        .select("name", "user_name", "password")
        .eq("user_name", username)
        .execute()
    )
    return user


def authenticate_user(username: str, password: str):
    if not user_exists(value=username):
        raise HTTPException(
            status_code=401,
            detail="User does not exist ",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_data = get_user_data(username)

    if not verify_password(password, user_data.data[0]["password"]):
        raise HTTPException(
            status_code=401,
            detail="Password error",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.now() + timedelta(minutes=15)
    else:
        expires = datetime.now() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_exp':False})
        username = token_decode.get("sub")
        if username == None:
            raise HTTPException(
                status_code=401,
                detail="Not username",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        print(JWTError)
        raise HTTPException(
            status_code=401,
            detail="JWT error decoding",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_data = get_user_data(username)
    if not user_data:
        raise HTTPException(
            status_code=401,
            detail="User not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_decode


# Create token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": form_data.username}, access_token_expires)

    return {"access_token": access_token_jwt, "token_type": "bearer"}


# Create a new user
@app.post("/user")
def create_user(user: User):
    try:
        # Convert email to lowercase
        user_name = user.username.lower()
        # Hash password
        hased_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

        # Check if user already exists
        if user_exists(value=user_name):
            return {"message": "User already exists"}

        # Add user to users table
        user = (
            supabase.from_("users")
            .insert(
                {
                    "name": user.name,
                    "user_name": user_name,
                    "password": hased_password.decode("utf-8"),
                }
            )
            .execute()
        )

        # Check if user was added
        if user:
            return {"message": "User created successfully"}
        else:
            return {"message": "User creation failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "User creation failed"}


# Retrieve a user
@app.get("/user")
def get_user(user: User = Depends(get_current_user)):
    return user


# logging
@app.post("/login")
async def login(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        # Convert email to lowercase
        user_email = user.email.lower()

        # Check if user already exists
        if user_exists(value=user_email):
            user_from_db = (
                supabase.from_("users").select("*").eq("email", user_email).execute()
            )
            if user_from_db.data[0]["password"] == user.password:
                return {"message": "User Authenticated"}
            else:
                raise HTTPException(status_code=404, detail="email or password error")

    except Exception as e:
        print("Error: ", e)
        return {"message": "User authentication failed"}
