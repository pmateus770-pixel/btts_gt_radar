import re, unicodedata, urllib.parse
from typing import Dict, List

def _first(*vals):
    for v in vals:
        if v:
            return v
    return ""

def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def match_key(jogo: Dict) -> str:
    for k in ("id", "fixture_id", "sofascore_id", "match_id", "bet365_id"):
        if jogo.get(k):
            return f"id:{jogo[k]}"
    return f"k:{_slug(jogo.get('league',''))}|{_slug(jogo.get('home',''))}|{_slug(jogo.get('away',''))}|{jogo.get('minute','')}"

def pretty_name(jogo: Dict, side: str) -> str:
    return _first(jogo.get(f"{side}_name"), jogo.get(side)) or "N/D"

def bet365_link(jogo: Dict) -> str:
    if jogo.get("bet365_id"):
        return f"https://www.bet365.com/?event={jogo['bet365_id']}"
    liga = _first(jogo.get("league_name"), jogo.get("league"))
    q = f"{liga} {pretty_name(jogo,'home')} x {pretty_name(jogo,'away')}"
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(q)

# ⇩⇩  Trocaremos esta função pela integração real da Bet365
async def get_live_matches() -> List[Dict]:
    """
    Retorna lista de jogos vivos no formato:
    {
      'league': 'GT',
      'minute': 45,
      'home': 'Time A', 'away': 'Time B',
      'score_home': 1, 'score_away': 0,
      'shots_on_target_home': 3, 'shots_on_target_away': 2,
      'shots_total_home': 8, 'shots_total_away': 6,
      'dangerous_attacks_sum': 85,
      'possession_home_pct': 52, 'possession_away_pct': 48,
      'bet365_id': '...'(opcional)
    }
    """
    return []  # por enquanto não quebra a app
