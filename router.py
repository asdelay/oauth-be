from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Body
from starlette.responses import RedirectResponse
import aiohttp
import jwt

from config import settings
from oauth_google import generate_google_oauth_uri

router = APIRouter(prefix="/auth")

@router.get("/google/url")
def get_google_oauth_redirect_uri():
    uri = generate_google_oauth_uri()
    return RedirectResponse(url=uri, status_code=302)

@router.post("/google/callback")
async def handle_code(code: Annotated[str, Body(embed=True)]):
    print("hello from post")
    google_token_url = "https://oauth2.googleapis.com/token"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=google_token_url,
            data={
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:3000/auth/google"
            }
        ) as response:
            res = await response.json()
            print(res)
            user_data = jwt.decode(
                jwt=res["id_token"],
                algorithms=["RS256"],
                options={"verify_signature": False}
            )
    return {
        "user": user_data
    }