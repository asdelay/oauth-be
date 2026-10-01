from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Body
from starlette.responses import RedirectResponse
import aiohttp
import jwt

from config import settings
from oauth_google import generate_google_oauth_uri
from state import states

router = APIRouter(prefix="/auth")

@router.get("/google/url")
def get_google_oauth_redirect_uri():
    uri = generate_google_oauth_uri()
    return RedirectResponse(url=uri, status_code=302)

@router.post("/google/callback")
async def handle_code(code: Annotated[str, Body()], state: Annotated[str, Body()]):
    if state in states:
        print("state is ok")
    else:
        raise
    google_token_url = "https://oauth2.googleapis.com/token"
    list_url = "https://www.googleapis.com/drive/v3/files"
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
            access_token=res["access_token"]
            user_data = jwt.decode(
                jwt=res["id_token"],
                algorithms=["RS256"],
                options={"verify_signature": False}
            )
        print(access_token)
        async with session.get(
            url=list_url,
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        ) as response:
            res = await response.json()
            print(res)
            files = [file["name"] for file in res["files"]]
    return {
        "user": user_data,
        "files": files
    }