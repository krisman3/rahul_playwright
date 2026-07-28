"""Central credential lookup.

Credentials come from environment variables (loaded from a local .env file if
present, or injected by CI). If the env vars are not set, we fall back to
data/credentials.json so local runs keep working without any setup.

Env vars:
    API_USER_EMAIL / API_USER_PASSWORD   - API login used by APIUtils
    UI_USER_EMAIL  / UI_USER_PASSWORD    - primary UI login user
    UI_USER_EMAIL_2 / UI_USER_PASSWORD_2 - optional second UI login user
"""
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_CREDENTIALS_FILE = Path(__file__).parent / "data" / "credentials.json"


def _file_users() -> list[dict]:
    with _CREDENTIALS_FILE.open() as f:
        return json.load(f)["user_credentials"]


def api_credentials() -> dict:
    """Payload for the API login. Prefers env vars, falls back to the first
    user in credentials.json."""
    email = os.getenv("API_USER_EMAIL")
    password = os.getenv("API_USER_PASSWORD")
    if not (email and password):
        first = _file_users()[0]
        email, password = first["user_email"], first["password"]
    return {"userEmail": email, "userPassword": password}


def ui_credentials() -> list[dict]:
    """UI login users for the parametrized e2e test. Prefers env vars (primary
    plus an optional second user); falls back to every user in
    credentials.json when no env vars are set."""
    email = os.getenv("UI_USER_EMAIL")
    password = os.getenv("UI_USER_PASSWORD")
    if not (email and password):
        return _file_users()

    users = [{"user_email": email, "password": password}]
    email_2 = os.getenv("UI_USER_EMAIL_2")
    password_2 = os.getenv("UI_USER_PASSWORD_2")
    if email_2 and password_2:
        users.append({"user_email": email_2, "password": password_2})
    return users