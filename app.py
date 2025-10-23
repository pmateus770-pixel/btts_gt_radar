import asyncio
from config import POLL_SECONDS, LEAGUE_FILTER
from datasource import get_live_matches
from notifier import send

async def loop():
    print("[BTTS-RADAR] Booting...")
    try:
        await send("BTTS Radar online ✔️")
    except Exception as e:
        print("[WARN] Falha ao enviar teste:", e)

    while True:
        try:
            # só coleta e imprime qntd para ver se ciclo está ok
            matches = await get_live_matches()
            print(f"[BTTS-RADAR] Lig: {LEAGUE_FILTER} | jogos: {len(matches)}")
        except Exception as e:
            print("[ERROR][loop]", e)

        await asyncio.sleep(POLL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(loop())
    except KeyboardInterrupt:
        print("Saindo...")
