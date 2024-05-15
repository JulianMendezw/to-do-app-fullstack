import bcrypt
from typing import Union
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import  HTTPException, Depends
from db.supabase import create_supabase_client
from fastapi.security import OAuth2PasswordBearer



# Initialize supabase client
supabase = create_supabase_client()

oauth2_scheme = OAuth2PasswordBearer("/login")

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
        token_decode = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}
        )
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
