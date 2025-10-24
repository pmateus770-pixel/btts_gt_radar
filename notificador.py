import aiohttp
from typing import Optional
from config import BOT_TOKEN, CHAT_ID

API = "https://api.telegram.org/bot{token}/sendMessage"

async def send(message: str, chat_id: Optional[str] = None):
    if not BOT_TOKEN:
        print("[WARN] BOT_TOKEN ausente — não enviando mensagem")
        return
    cid = chat_id or CHAT_ID
    if not cid:
        print("[WARN] CHAT_ID ausente — não enviando mensagem")
        return
    url = API.format(token=BOT_TOKEN)
    payload = {"chat_id": cid, "text": message, "disable_web_page_preview": False}
    async with aiohttp.ClientSession() as sess:
        async with sess.post(url, json=payload, timeout=20) as resp:
            if resp.status != 200:
                txt = await resp.text()
                print(f"[TELEGRAM][{resp.status}] {txt}")
