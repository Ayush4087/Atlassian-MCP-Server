import base64
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("ATLASSIAN_EMAIL")
API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN")
BASE_URL = os.getenv("ATLASSIAN_BASE_URL")


def get_auth_header():
    if not all([EMAIL, API_TOKEN]):
        raise ValueError("Missing Atlassian credentials")
    token = f"{EMAIL}:{API_TOKEN}"
    encoded = base64.b64encode(token.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
