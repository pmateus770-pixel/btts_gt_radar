# fonte_de_dados.py
"""
Fonte: Bet365 via BetsAPI (in-play).
Retorna uma lista de partidas padronizadas para o restante do app.
Obs.: o feed da Bet365 normalmente não traz estatísticas como SOT/ataques.
Se você precisa das regras por estatística (SOT/Finalizações/DA), mantenho
um fallback simples e/ou fazemos um enrich depois com SofaScore apenas
para métricas — mas a lista de jogos vem da Bet365.
"""

from typing import List, Dict, Any
import aiohttp
import asyncio
from config import BETSAPI_KEY

BETSAPI_BASE = "https://api.b365api.com/v1"   # domínio da BetsAPI

async def _fetch_json(session: aiohttp.ClientSession, url: str, params: Dict[str, Any]) -> Dict:
    async with session.get(url, params=params, timeout=25) as r:
        if r.status != 200:
            txt = await r.text()
            raise RuntimeError(f"[BetsAPI {r.status}] {txt}")
        return await r.json()

def _normalize_event(ev: Dict) -> Dict:
    """
    Normaliza o evento no formato que o app espera.
    Campos típicos da BetsAPI (bet365/inplay): 'home', 'away', 'league', 'timer', 'scores', 'id'
    Atenção: nomes exatos podem variar conforme plano/rota.
    """
    home = ev.get("home", "") or ev.get("home_name", "")
    away = ev.get("away", "") or ev.get("away_name", "")
    league = ev.get("league", "") or ev.get("league_name", "")
    minute = 0
    try:
        # alguns retornam 'timer' ou 'time'
        minute = int(ev.get("timer") or ev.get("time") or 0)
    except Exception:
        minute = 0

    # placar
    h = a = 0
    scores = ev.get("scores") or {}
    try:
        h = int(scores.get("home", 0))
        a = int(scores.get("away", 0))
    except Exception:
        pass

    # id bet365 (para montar link depois)
    b365_id = ev.get("id") or ev.get("bet365_id") or ev.get("event_id")

    return {
        "league": league,
        "home": home,
        "away": away,
        "minute": minute,
        "score_home": h,
        "score_away": a,
        "bet365_id": b365_id,
        # Sem estatísticas no feed Bet365 público:
        "shots_on_target_home": 0,
        "shots_on_target_away": 0,
        "shots_total_home": 0,
        "shots_total_away": 0,
        "dangerous_attacks_sum": 0,
        "possession_home_pct": None,
        "possession_away_pct": None,
    }

async def get_live_matches() -> List[Dict]:
    """
    Busca jogos AO VIVO (soccer) da Bet365 via BetsAPI.
    sport_id=1  => futebol
    """
    if not BETSAPI_KEY:
        raise RuntimeError("BETSAPI_KEY não configurada.")

    params = {
        "token": BETSAPI_KEY,
        "sport_id": 1,   # soccer
    }
    url = f"{BETSAPI_BASE}/bet365/inplay"
    async with aiohttp.ClientSession() as sess:
        data = await _fetch_json(sess, url, params)

    results = data.get("results") or data.get("events") or []
    norm = [_normalize_event(ev) for ev in results]
    return norm

# helper para link da partida (Bet365)
def bet365_link(ev: Dict) -> str:
    """
    Bet365 muda bastante o formato de URL por região/idioma.
    Usamos o id quando possível (algumas integrações usam EV{id}).
    Como fallback, devolvemos uma busca focada.
    """
    b365_id = ev.get("bet365_id")
    if b365_id:
        # Algumas instalações funcionam assim (pode variar):
        return f"https://www.bet365.com/#/IP/EV{b365_id}"
    # fallback: busca
    from urllib.parse import quote_plus
    q = f"{ev.get('league','')} {ev.get('home','')} x {ev.get('away','')} site:bet365.com"
    return "https://www.google.com/search?q=" + quote_plus(q)
