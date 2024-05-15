import bcrypt
from app.models.users import User
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from db.supabase import create_supabase_client
from app.auth import user_exists, authenticate_user, create_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

# Initialize supabase client
supabase = create_supabase_client()


# Create a new user
@router.post("/user", tags=["Users"])
def create_user(user: User):
    try:
        # Convert user to lowercase
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


# Create token
@router.post("/login", tags=["Users"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": form_data.username}, access_token_expires)

    return {"access_token": access_token_jwt, "token_type": "bearer"}
