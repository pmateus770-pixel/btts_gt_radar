
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()
LEAGUE_FILTER = os.getenv("LEAGUE_FILTER", "GT").upper()
MODE = os.getenv("MODE", "demo").lower()  # demo | live
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "30"))
import os
BETSAPI_KEY = os.getenv("BETSAPI_KEY", "")
