from fastapi import APIRouter
from starlette.responses import RedirectResponse

from oauth_google import generate_google_oauth_uri

router = APIRouter(prefix="/auth")

@router.get("/google/url")
def get_google_oauth_redirect_uri():
    uri = generate_google_oauth_uri()
    return RedirectResponse(url=uri, status_code=302)