import bcrypt
from typing_extensions import Annotated
from typing import Union
from fastapi import FastAPI, HTTPException, Depends
from app.models import User, UserLogging
from db.supabase import create_supabase_client
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize supabase client
supabase = create_supabase_client()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# def authenticate_user(db, username, password):
    

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

#test endpoint
@app.get("/users/me")
def user(token: str = Depends(oauth2_scheme)):
    print(token)
    return "Im a user"

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    return {
        "access_token": "my_token",
        "token_type": "bearer"
    }

# Create a new user
@app.post("/user")
def create_user(user: User):
    try:
        # Convert email to lowercase
        user_email = user.email.lower()
        # Hash password
        hased_password = bcrypt.hashpw(user.password, bcrypt.gensalt())

        # Check if user already exists
        if user_exists(value=user_email):
            return {"message": "User already exists"}

        # Add user to users table
        user = supabase.from_("users")\
            .insert({"name": user.name, "email": user_email, "password": hased_password})\
            .execute()

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
def get_user(user_id: Union[str, None] = None):
    try:
        if user_id:
            user = supabase.from_("users")\
                .select("id", "name", "email")\
                .eq("id", user_id)\
                .execute()

            if user:
                return user
        else:
            users = supabase.from_("users")\
                .select("id", "email", "name")\
                .execute()
            if users:
                return users
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "User not found"}


#logging
@app.post("/login")
async def login(user: UserLogging):
    try:
        # Convert email to lowercase
        user_email = user.email.lower()

        # Check if user already exists
        if user_exists(value=user_email):
            user_from_db = supabase.from_("users").select("*").eq('email', user_email).execute()
            print(user.password)
            if user_from_db.data[0]["password"] == user.password:            
               return {"message": "User Authenticated"}
            else:
                raise HTTPException(status_code=404, detail="email or password error")

    except Exception as e:
        print("Error: ", e)
        return {"message": "User authentication failed"}