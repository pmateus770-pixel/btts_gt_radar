import aiohttp, urllib.parse
from typing import Optional
from config import BOT_TOKEN, CHAT_ID

API = "https://api.telegram.org/bot{token}/sendMessage"

def _search_link(league, home, away):
    q = f"{league} {home} x {away}"
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(q)

def _fmt_line(m):
    h,a = m["score_home"], m["score_away"]
    return f"{m['minute']}' | {h}-{a}"

def _fmt_stats(m, resumo):
    return f"SOT:{int(m['shots_on_target_home'])+int(m['shots_on_target_away'])} Final:{int(m['shots_total_home'])+int(m['shots_total_away'])} {resumo}"

def render_message(nivel: str, m: dict, resumo: str) -> str:
    t1, t2 = m["home"], m["away"]
    title = f"BTTS {nivel} - {m['league']}"
    linha = _fmt_line(m)
    stats = _fmt_stats(m, resumo)
    link = m.get("link") or _search_link(m['league'], t1, t2)
    return (
        f"{title}\n"
        f"{t1} x {t2}\n"
        f"{linha}\n"
        f"{stats}\n"
        f"Ver partida: {link}"
    )

async def send(message: str, chat_id: Optional[str] = None):
    if not BOT_TOKEN: 
        print("[WARN] BOT_TOKEN ausente"); return
    cid = chat_id or CHAT_ID
    if not cid:
        print("[WARN] CHAT_ID ausente"); return
    url = API.format(token=BOT_TOKEN)
    payload = {"chat_id": cid, "text": message, "disable_web_page_preview": False}
    async with aiohttp.ClientSession() as sess:
        async with sess.post(url, json=payload, timeout=20) as resp:
            if resp.status != 200:
                txt = await resp.text()
                print(f"[TELEGRAM][{resp.status}] {txt}")
