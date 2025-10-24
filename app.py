import asyncio
from config import POLL_SECONDS, LEAGUE_FILTER, MODE
from notificador import send
from logica import classify_btssignal
from estado import was_sent, mark_sent
from fonte_de_dados import get_live_matches, match_key, pretty_name, bet365_link

def _ok_to_alert(nivel: str) -> bool:
    return nivel in ("FORTE", "OK")

async def worker():
    print("BTTS Radar online ✅")
    while True:
        try:
            jogos = await get_live_matches()
            if LEAGUE_FILTER:
                jogos = [j for j in jogos if str(j.get("league","")).upper() == LEAGUE_FILTER.upper()]

            for j in jogos:
                nivel, resumo = classify_btssignal(j)
                if not _ok_to_alert(nivel):
                    continue

                key = match_key(j)
                if was_sent(key):
                    continue

                home = pretty_name(j, "home")
                away = pretty_name(j, "away")
                minute = j.get("minute", 0)
                score = f"{int(j.get('score_home',0))}-{int(j.get('score_away',0))}"

                url = bet365_link(j)
                msg = (
                    f"BTTS {nivel} – {j.get('league','N/D')}\n"
                    f"{home} x {away}\n"
                    f"{minute}' | {score}\n"
                    f"{resumo}\n"
                    f"Ver partida: {url}"
                )
                if MODE != "demo":
                    await send(msg)
                else:
                    print("[DEMO] ", msg.replace("\n", " | "))

                mark_sent(key)

        except Exception as e:
            print("[ERR] LOOP:", e)

        await asyncio.sleep(POLL_SECONDS)

if __name__ == "__main__":
    asyncio.run(worker())
