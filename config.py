import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
LEAGUE_FILTER = os.getenv("LEAGUE_FILTER", "").strip()  # ex: "GT"
MODE = os.getenv("MODE", "demo")                        # demo | prod
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "30"))
