import os

BOT_TOKEN   = os.getenv("BOT_TOKEN", "")
CHAT_ID     = os.getenv("CHAT_ID", "")

# Provedor de dados: "betsapi" ou "scraper"
PROVIDER    = os.getenv("PROVIDER", "betsapi").lower()

# ---- BetsAPI (pago) ----
BETSAPI_TOKEN   = os.getenv("BETSAPI_TOKEN", "")
# sport_id do FIFA/Esoccer na sua conta (confirme nos docs do seu plano)
BETSAPI_SPORT_ID = os.getenv("BETSAPI_SPORT_ID", "151")  # ajuste se necessário

# Intervalo de varredura (segundos)
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "30"))
