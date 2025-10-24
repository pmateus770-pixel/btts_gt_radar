# config.py
import os

def _env(name, default=None, cast=str):
    v = os.getenv(name)
    if v is None or v == "":
        return default
    try:
        return cast(v)
    except Exception:
        return v

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID   = os.getenv("CHAT_ID", "")

# Modo & janela de varredura
MODE         = _env("MODE", "live")            # "live" ou "demo"
POLL_SECONDS = _env("POLL_SECONDS", 30, int)   # intervalo de polling

# Filtro de liga (opcional). Aceita ambos nomes de env:
LEAGUE_FILTER = os.getenv("LEAGUE_FILTER") or os.getenv("FILTRO_DA_LIGA") or ""

# Provedor de dados
PROVIDER = (_env("PROVIDER", "betsapi") or "betsapi").lower()

# Credenciais BetsAPI (se usar)
BETSAPI_TOKEN    = os.getenv("BETSAPI_TOKEN", "")
BETSAPI_SPORT_ID = _env("BETSAPI_SPORT_ID", None, int)  # pode ficar None
