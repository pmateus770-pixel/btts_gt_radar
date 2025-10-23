from fonte_de_dados import bet365_link

# ...
url = bet365_link(jogo)
msg = (
    f"{nivel} – {jogo['league']}\n"
    f"{jogo['home']} x {jogo['away']}\n"
    f"{jogo['minute']}' | {jogo['score_home']}-{jogo['score_away']}\n"
    f"Ver partida: {url}"
)
