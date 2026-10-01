import secrets

from config import settings
from state import states


def generate_google_oauth_uri():
    state = secrets.token_urlsafe(16)
    states.add(state)
    base_url="https://accounts.google.com/o/oauth2/v2/auth"
    redirect_uri="http://localhost:3000/auth/google"
    # add state query param
    return f"{base_url}?client_id={settings.CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope=https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/calendar openid email profile&access_type=offline&state={state}"