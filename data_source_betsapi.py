import aiohttp
from typing import List, Dict
from config import BETSAPI_TOKEN, BETSAPI_SPORT_ID

API_INPLAY = "https://betsapi.com/api/v1/bet365/inplay"  # ajuste se seu plano usar outro host/caminho

def _norm(x): return (x or "").strip()

def _team_name(ev, side):
    # tenta vários campos comuns na Bet365/BetsAPI
    return _norm(
        ev.get(f"{side}_name")
        or ev.get(f"{side}")
        or ev.get(f"{side.capitalize()}")  # Home/Away
        or ""
    )

def _minute_from_timer(ev):
    # muitos feeds entregam "time": "53:27", ou "timer": {"tm": 53}
    t = ev.get("time") or ev.get("timer") or {}
    if isinstance(t, dict):
        return int(t.get("tm") or 0)
    if isinstance(t, str) and ":" in t:
        try:
            return int(t.split(":")[0])
        except:
            return 0
    return int(t or 0)

async def fetch_matches() -> List[Dict]:
    if not BETSAPI_TOKEN:
        return []

    params = {"token": BETSAPI_TOKEN, "sport_id": BETSAPI_SPORT_ID}
    async with aiohttp.ClientSession() as s:
        async with s.get(API_INPLAY, params=params, timeout=25) as r:
            if r.status != 200:
                txt = await r.text()
                print(f"[BetsAPI][{r.status}] {txt}")
                return []
            data = await r.json()

    rows = []
    for ev in (data.get("results") or []):
        # filtre apenas FIFA/GT/esoccer; ajuste o critério conforme ver na sua conta
        league = _norm(ev.get("league", ""))
        if not any(k in league.upper() for k in ["FIFA", "E-SOCCER", "ESOC", "GT"]):
            continue

        home = _team_name(ev, "home")
        away = _team_name(ev, "away")
        if not home or not away:
            continue

        # placar
        try:
            sh, sa = ev.get("ss", "0-0").split("-")
            sh, sa = int(sh), int(sa)
        except:
            sh, sa = int(ev.get("home_score") or 0), int(ev.get("away_score") or 0)

        # chutes a gol / total se existirem
        stats = ev.get("stats") or {}
        sot_h = int(stats.get("sog_home") or stats.get("shots_on_target_home") or 0)
        sot_a = int(stats.get("sog_away") or stats.get("shots_on_target_away") or 0)
        st_h  = int(stats.get("shots_home") or 0)
        st_a  = int(stats.get("shots_away") or 0)

        rows.append({
            "id": ev.get("id") or ev.get("event_id"),
            "league": league,
            "home": home,
            "away": away,
            "minute": _minute_from_timer(ev),
            "score_home": sh,
            "score_away": sa,
            "shots_on_target_home": sot_h,
            "shots_on_target_away": sot_a,
            "shots_total_home": st_h,
            "shots_total_away": st_a,
            # link direto (se a API fornecer). se vier "bet365_id", você consegue montar deep-link do seu afiliado:
            "link": ev.get("url") or ev.get("link") or "",
        })
    return rows
