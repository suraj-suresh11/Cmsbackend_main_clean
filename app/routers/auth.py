from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.db.database import get_db
from app.models.user import User
from sqlalchemy.future import select
import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

# OAuth config
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    },
)

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.get("/auth/google")
async def login_google(request: Request):
    redirect_uri = os.getenv("REDIRECT_URI")
    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
        access_type="offline",
        prompt="consent"
    )

@router.get("/auth/callback/google")
async def auth_google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        resp = await oauth.google.get("https://www.googleapis.com/oauth2/v2/userinfo", token=token)
        user_info = resp.json()

        result = await db.execute(select(User).where(User.email == user_info["email"]))
        existing_user = result.scalars().first()

        if not existing_user:
            new_user = User(
                email=user_info["email"],
                name=user_info.get("name"),
                picture=user_info.get("picture"),
                provider="google"
            )
            db.add(new_user)
            await db.commit()

        access_token = create_access_token(
            data={"sub": user_info["email"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        refresh_token = token.get("refresh_token")

        return JSONResponse({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user_info
        })

    except OAuthError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
