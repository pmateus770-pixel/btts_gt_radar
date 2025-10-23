
import asyncio, random, time
from typing import List, Dict
from config import MODE, LEAGUE_FILTER

# ===== DEMO GENERATOR =====
# Gera partidas falsas para você ver o alerta funcionando.
def _demo_matches() -> List[Dict]:
    now = int(time.time())
    rnd = random.Random(now // 15)  # muda a cada ~15s (determinístico por janela)
    matches = []
    for i in range(5):
        minute = rnd.randint(5, 70)
        score_home = rnd.choice([0,1])
        score_away = 0 if score_home==1 else rnd.choice([0,1])
        st_h = rnd.randint(3,10)
        st_a = rnd.randint(3,10)
        sot_h = rnd.randint(0, st_h//2 + 1)
        sot_a = rnd.randint(0, st_a//2 + 1)
        attacks = rnd.randint(40, 95)
        matches.append({
            "id": f"gt-demo-{i}",
            "league": LEAGUE_FILTER,
            "minute": minute,
            "home": f"GT Team {i*2+1}",
            "away": f"GT Team {i*2+2}",
            "score_home": score_home,
            "score_away": score_away,
            "shots_on_target_home": sot_h,
            "shots_on_target_away": sot_a,
            "shots_total_home": st_h,
            "shots_total_away": st_a,
            "dangerous_attacks_sum": attacks,
            "possession_home_pct": rnd.randint(38,62),
            "possession_away_pct": None,
        })
    return matches

async def get_live_matches() -> List[Dict]:
    if MODE == "demo":
        return _demo_matches()
    # ===== LIVE MODE (edite aqui) =====
    # 1) Buscar página/endpoint público com estatísticas da Liga GT
    # 2) Fazer parse e retornar a lista no formato esperado
    #    Veja o schema no README.
    # deixe um "pass" aqui até configurar sua fonte
    return []
