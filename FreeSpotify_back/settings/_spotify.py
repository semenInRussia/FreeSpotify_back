import os as _os

from dotenv import load_dotenv as _load_dotenv

_load_dotenv()

SPOTIFY_CLIENT_ID = _os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = _os.getenv("SPOTIFY_CLIENT_SECRET")
