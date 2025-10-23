
# BTTS GT Radar — Telegram Alerts (24/7, Railway-ready)

Radar automático que monitora **fontes públicas** de estatísticas de eSoccer (Liga GT), aplica o **Método Mateus Protocol v1** e envia **alertas no Telegram**.  
**Não interage** com casas de aposta.

## Regras (Mateus Protocol v1)
- Liga: **GT**
- Mercado: **Ambas Marcam (BTTS)** — sinal/tendência
- Odd alvo: **≥ 1.66** (estimada pela pressão)
- Janela de entrada:
  - 0–0 até **25'**
  - 1–0 / 0–1 entre **20'–60'**
- Indicadores mínimos:
  - **SOT somados ≥ 4**
  - **Finalizações somadas ≥ 10**
  - **Ataques perigosos somados ≥ 80**
  - Posse equilibrada **35–65%** (se disponível)

## Arquitetura
- `app.py` — loop principal (async), agenda a coleta e envia alertas.
- `logic.py` — aplica as regras e classifica FORTE/OK/FRACO.
- `datasource.py` — **fonte pública** de estatísticas (troque aqui pela sua).
- `notifier.py` — envio de mensagens pro Telegram.
- `state.py` — evita alertas duplicados.
- `config.py` — lê variáveis de ambiente.
- `requirements.txt` — dependências.
- `Railway.toml` — comando para rodar no Railway.

## Executando localmente
1. Python 3.10+
2. `pip install -r requirements.txt`
3. Copie `.env.example` para `.env` e preencha:
   - `BOT_TOKEN` — token do seu bot (BotFather)
   - `CHAT_ID` — ID do **seu canal privado** (veja abaixo)
   - `LEAGUE_FILTER=GT`
   - `MODE=demo` (para testar) ou `MODE=live` (quando ligar a fonte real)
4. `python app.py`

## Como obter o CHAT_ID do canal privado
1. Adicione o **seu bot** ao canal (Admin > Add Admin > seu bot).
2. Encaminhe **qualquer mensagem do canal** para o bot `@getidsbot` ou `@userinfobot`.
3. Ele retornará algo como: `Chat ID: -1001234567890`.
4. Use esse valor na variável `CHAT_ID` (com o sinal de menos).

## Deploy no Railway
1. Suba estes arquivos para um repositório privado no GitHub.
2. No Railway: **New Project > Deploy from GitHub Repo** (conecte sua conta GitHub).
3. Em **Variables**, adicione:
   - `BOT_TOKEN`
   - `CHAT_ID`
   - `LEAGUE_FILTER=GT`
   - `MODE=demo` (mude pra `live` quando ligar a fonte real)
4. Deploy. Os logs mostrarão o loop rodando e eventuais alertas.

## Ligando uma fonte real (sem casa de aposta)
Edite `datasource.py` para buscar estatísticas **públicas** (HTML/JSON) de eSoccer/Liga GT.
A função `get_live_matches()` deve retornar uma lista como:

```jsonc
[{
  "id": "gt-12345",
  "league": "GT",
  "minute": 28,
  "home": "Time A",
  "away": "Time B",
  "score_home": 1,
  "score_away": 0,
  "shots_on_target_home": 3,
  "shots_on_target_away": 2,
  "shots_total_home": 7,
  "shots_total_away": 6,
  "dangerous_attacks_sum": 86,
  "possession_home_pct": 52,   // opcional
  "possession_away_pct": 48    // opcional
}]
```

> **Dica**: mantenha a frequência padrão do coletor (a cada 30s) e respeite os termos do site público.

## Observação de segurança
- Nunca exponha seu `BOT_TOKEN` publicamente.
- Este projeto não interage com casas de aposta.
