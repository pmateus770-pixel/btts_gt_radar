import asyncio
from config import POLL_SECONDS, LEAGUE_FILTER
from datasource import get_live_matches
from logic import classify_btssignal, match_key, build_match_url, pretty_name
from notifier import send
from state import already_alerted                   # limita spam por janela de 5'
from estado import was_sent, mark_sent             # garante 1 alerta por jogo

def bucket_from_minute(minute: int) -> str:
    base = max(0, (minute // 5) * 5)
    return f"{base:02d}-{base+4:02d}"

async def loop():
    print("[BTTS-RADAR] Iniciado. Coletando a cada", POLL_SECONDS, "s")
    while True:
        try:
            matches = await get_live_matches()

            for m in matches:
                # Filtro por liga
                if (m.get("league") or "").upper() != LEAGUE_FILTER:
                    continue

                # Classificação pelo protocolo BTTS
                lvl, resume = classify_btssignal(m)
                if lvl not in ("FORTE", "OK"):
                    continue

                # ===== Só 1 alerta por jogo =====
                mk = match_key(m)
                if was_sent(mk):
                    continue  # já avisamos este jogo; pula

                # (Opcional) Evitar spam por janela de 5'
                minute = int(m.get("minute") or 0)
                bucket = bucket_from_minute(minute)
                if already_alerted(m.get("id", mk), bucket):
                    continue
                # ===== Fim da checagem =====

                # Texto amigável (com nomes e link se disponível)
                liga  = m.get("league_name") or m.get("league") or "Liga"
                home  = pretty_name(m, "home")
                away  = pretty_name(m, "away")
                score = f"{m.get('score_home',0)}-{m.get('score_away',0)}"
                link  = build_match_url(m)

                title = f"⚽️ BTTS {lvl} – {liga}"
                line1 = f"*{home}* x *{away}*"
                line2 = f"{minute}' | {score}"
                stats = f"{resume}"
                linkl = f"\n[Ver partida]({link})" if link else ""

                msg = f"{title}\n{line1}\n{line2}\n{stats}{linkl}"

                await send(msg)

                # Marca o jogo como notificado (não repete)
                mark_sent(mk)

        except Exception as e:
            print("[ERROR]", e)

        await asyncio.sleep(POLL_SECONDS)

if __name__ == "__main__":
    try:
        asyncio.run(loop())
    except KeyboardInterrupt:
        print("Saindo...")
