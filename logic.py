from typing import Dict, Tuple
import re, unicodedata, urllib.parse

# -------------------------------------------
# CLASSIFICAÇÃO DO SINAL BTTS
# -------------------------------------------
def classify_btssignal(m: Dict) -> Tuple[str, str]:
    league = (m.get("league") or "").upper()
    minute = int(m.get("minute") or 0)
    h, a = int(m.get("score_home") or 0), int(m.get("score_away") or 0)
    sot_h, sot_a = int(m.get("shots_on_target_home") or 0), int(m.get("shots_on_target_away") or 0)
    st_h, st_a = int(m.get("shots_total_home") or 0), int(m.get("shots_total_away") or 0)
    attacks = int(m.get("dangerous_attacks_sum") or 0)
    pos_h = m.get("possession_home_pct")
    pos_a = m.get("possession_away_pct")

    # filtros básicos de janela e placar (0-0 até 25', 1-0 entre 20-60')
    if h == 0 and a == 0:
        if minute > 25 or minute < 0:
            return "DESCARTA", "0-0 fora da janela"
    elif abs(h - a) == 1:
        if minute < 20 or minute > 60:
            return "DESCARTA", "1-0 fora da janela"
    else:
        return "DESCARTA", "Placar não favorável"

    # indicadores de pressão
    sot_sum = sot_h + sot_a
    st_sum = st_h + st_a

    if sot_sum >= 4 and st_sum >= 10 and attacks >= 80:
        if pos_h is not None and pos_a is not None:
            if not (35 <= int(pos_h) <= 65):
                return "OK", f"SOT:{sot_sum} Final:{st_sum} Atk:{attacks} (posse desequilibrada)"
        return "FORTE", f"SOT:{sot_sum} Final:{st_sum} Atk:{attacks}"
    elif sot_sum >= 3 and st_sum >= 8 and attacks >= 60:
        return "OK", f"SOT:{sot_sum} Final:{st_sum} Atk:{attacks}"
    else:
        return "FRACO", f"SOT:{sot_sum} Final:{st_sum} Atk:{attacks}"


# -------------------------------------------
# KEY ÚNICA DO JOGO
# -------------------------------------------
def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def match_key(jogo: dict) -> str:
    for k in ("id", "fixture_id", "sofascore_id", "match_id"):
        if jogo.get(k):
            return f"id:{jogo[k]}"

    liga = jogo.get("league", "")
    home = jogo.get("home", "")
    away = jogo.get("away", "")
    minuto = jogo.get("minute", "")

    return f"k:{_slug(liga)}|{_slug(home)}|{_slug(away)}|{minuto}"


# -------------------------------------------
# LINK DO JOGO
# -------------------------------------------
def _first(*vals):
    for v in vals:
        if v:
            return v
    return ""

def build_match_url(jogo: dict) -> str:
    if jogo.get("sofascore_id"):
        return f"https://www.sofascore.com/event/{jogo['sofascore_id']}"
    if jogo.get("flashscore_id"):
        return f"https://www.flashscore.com/match/{jogo['flashscore_id']}"
    if jogo.get("fixture_id"):
        return f"https://seuservico.exemplo/match/{jogo['fixture_id']}"

    liga = _first(jogo.get("league_name"), jogo.get("league"))
    home = _first(jogo.get("home_name"), jogo.get("home"))
    away = _first(jogo.get("away_name"), jogo.get("away"))
    q = f"{liga} {home} x {away}"
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(q)


# -------------------------------------------
# NOME BONITO DOS TIMES
# -------------------------------------------
def pretty_name(jogo: dict, side: str) -> str:
    return _first(
        jogo.get(f"{side}_name"),
        jogo.get(f"{side}Name"),
        jogo.get(side),
    ) or "N/D"
