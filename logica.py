from typing import Dict, Tuple

def classify_btssignal(m: Dict) -> Tuple[str, str]:
    """
    Retorna (nivel, resumo) onde nivel ∈ {"FORTE","OK","FRACO","DESCARTA"}
    """
    minute = int(m.get("minute") or 0)
    h, a = int(m.get("score_home") or 0), int(m.get("score_away") or 0)
    sot_h, sot_a = int(m.get("shots_on_target_home") or 0), int(m.get("shots_on_target_away") or 0)
    st_h, st_a = int(m.get("shots_total_home") or 0), int(m.get("shots_total_away") or 0)
    attacks = int(m.get("dangerous_attacks_sum") or 0)
    pos_h = m.get("possession_home_pct")
    pos_a = m.get("possession_away_pct")

    # Janela básica
    if h == 0 and a == 0:
        if minute > 25 or minute < 0:
            return "DESCARTA", "0-0 fora da janela"
    elif abs(h - a) == 1:
        if minute < 20 or minute > 60:
            return "DESCARTA", "1-0 fora da janela"
    else:
        return "DESCARTA", "Placar não favorável"

    sot_sum = sot_h + sot_a
    st_sum = st_h + st_a

    if sot_sum >= 4 and st_sum >= 10 and attacks >= 80:
        if pos_h is not None and pos_a is not None and not (35 <= int(pos_h) <= 65):
            return "OK", f"SOT:{sot_sum} Final:{st_sum} Atk:{attacks} (posse desequilibrada)"
        return "FORTE", f"SOT:{sot_sum} Final:{st_sum} Atk:{attacks}"
    if sot_sum >= 3 and st_sum >= 8 and attacks >= 60:
        return "OK", f"SOT:{sot_sum} Final:{st_sum} Atk:{attacks}"
    return "FRACO", f"SOT:{sot_sum} Final:{st_sum} Atk:{attacks}"
