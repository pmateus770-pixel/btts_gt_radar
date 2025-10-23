import asyncio
from config import POLL_SECONDS, LEAGUE_FILTER
from datasource import get_live_matches
from logic import classify_btssignal, match_key, build_match_url, pretty_name
from notifier import send
from estado import was_sent, mark_sent

async def loop():
    print("[BTTS-RADAR] Iniciado. Coletando a cada", POLL_SECONDS, "s")
    # Mensagem de boot (opcional)
    try:
        await send("BTTS Radar online ✔️")
    except Exception as e:
        print("[WARN] Falha no envio de boot:", e)

    while True:
        try:
            matches = await get_live_matches()

            for m in matches:
                # Liga
                if (m.get("league") or "").upper() != LEAGUE_FILTER:
                    continue

                # Classificação do sinal
                lvl, resume = classify_btssignal(m)
                if lvl not in ("FORTE", "OK"):
                    continue

                # Um alerta por jogo
                mk = match_key(m)
                if was_sent(mk):
                    continue

                # Texto
                liga  = m.get("league_name") or m.get("league") or "Liga"
                home  = pretty_name(m, "home")
                away  = pretty_name(m, "away")
                minute = int(m.get("minute") or 0)
                score = f"{m.get('score_home',0)}-{m.get('score_away',0)}"
                link  = build_match_url(m)

                title = f"BTTS {lvl} - {liga}"
                line1 = f"{home} x {away}"
                line2 = f"{minute}' | {score}"
                linkl = f"\nVer partida: {link}" if link else ""

                msg = f"{title}\n{line1}\n{line2}\n{resume}{linkl}"

                await send(msg)
                mark_sent(mk)

        except Exception as e:
            print("[ERROR][main loop]", e)

        await asyncio.sleep(POLL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(loop())
    except KeyboardInterrupt:
        print("Saindo...")
