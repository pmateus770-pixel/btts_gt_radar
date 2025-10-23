
import asyncio
from config import POLL_SECONDS, LEAGUE_FILTER
from datasource import get_live_matches
from logic import classify_btssignal
from notifier import send
from state import already_alerted

def bucket_from_minute(minute: int) -> str:
    # para limitar alertas repetidos, agrupamos por janelas de 5 min
    base = max(0, (minute // 5) * 5)
    return f"{base:02d}-{base+4:02d}"

async def loop():
    print("[BTTS-RADAR] Iniciado. Coletando a cada", POLL_SECONDS, "s")
    while True:
        try:
            matches = await get_live_matches()
            for m in matches:
                if (m.get("league") or "").upper() != LEAGUE_FILTER:
                    continue
                lvl, resume = classify_btssignal(m)
                if lvl not in ("FORTE", "OK"):
                    continue
                minute = int(m.get("minute") or 0)
                bucket = bucket_from_minute(minute)
                if already_alerted(m["id"], bucket):
                    continue
                title = f"⚽️ BTTS {lvl} – Liga {LEAGUE_FILTER}"
                line1 = f"{m.get('home','?')} x {m.get('away','?')}"
                line2 = f"""{minute}' | {m.get('score_home',0)}-{m.get('score_away',0)}"""
                stats = f"""{resume}"""
                msg = f"""{title}
{line1}
{line2}
{stats}"""
                await send(msg)
        except Exception as e:
            print("[ERROR]", e)
        await asyncio.sleep(POLL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(loop())
    except KeyboardInterrupt:
        print("Saindo...")
