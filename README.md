# Agentiska AI – Workshop

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Agent Framework](https://img.shields.io/badge/Agent_Framework-1.0.0rc1-purple?logo=microsoft&logoColor=white)
![Azure OpenAI](https://img.shields.io/badge/Azure_OpenAI-GPT--5_nano-0078D4?logo=microsoftazure&logoColor=white)
![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-Search-DE5833?logo=duckduckgo&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

En praktisk introduksjon til agentiske AI-systemer bygget med [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/?pivots=programming-language-python).

---

## Kom i gang

### 1. Klon repoet

```bash
git clone https://github.com/kantega/agents-workshop.git
cd agents-workshop
```

### 2. Opprett virtuelt miljø og installer pakker

```bash
python3.13 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

> Velg riktig interpreter i VS Code: `Cmd/Ctrl + Shift + P` → **Python: Select Interpreter** → velg `.venv`

### 3. Konfigurer API-nøkkel

Opprett en `.env`-fil i rotmappen med følgende innhold:

```
AZURE_OPENAI_API_KEY="din_api_nøkkel_her"
AZURE_OPENAI_ENDPOINT="Ditt endepunkt"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-5-nano"
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME="gpt-5-nano"
```

### 4. Test miljøet

```bash
.venv/bin/python test_environment.py
```

---

## Øvelser

### Øvelse 1 – Web-søk med verktøy
**Fil:** `exercises/1_web_browsing_exercise.py`

Lær hvordan en agent kan bruke eksterne verktøy som web-søk (DuckDuckGo). Du definerer en `web_search`-funksjon som agenten kaller automatisk når den trenger informasjon.

```bash
.venv/bin/python exercises/1_web_browsing_exercise.py
```

### Øvelse 2 – Agent-til-agent diskusjon
**Fil:** `exercises/2_discussion_exercise.py`

To agenter (Coder og Critic) diskuterer og forbedrer løsninger i fellesskap, koordinert av en orchestrator.

```bash
.venv/bin/python exercises/2_discussion_exercise.py
```

### Øvelse 3 – Menneske i løkka
**Fil:** `exercises/3_discussion_with_user_exercise.py`

Som øvelse 2, men her kan du selv gi feedback til agentene underveis i diskusjonen. Når agenten spør `Feedback for Critic (or 'skip' to approve):` skriver du inn din feedback eller `skip` for å godkjenne.

```bash
.venv/bin/python exercises/3_discussion_with_user_exercise.py
```

---

## Om agentiske systemer

Agentiske systemer består av flere autonome AI-agenter som samarbeider for å løse komplekse oppgaver. I stedet for én enkelt modell som gjør alt, deles arbeidet mellom spesialiserte agenter med ulike roller.

### Fordeler

| Fordel | Beskrivelse |
|--------|-------------|
| **Spesialisering** | Hver agent fokuserer på sitt domene |
| **Kvalitetskontroll** | Agenter kan gi hverandre peer review |
| **Skalerbarhet** | Enkelt å legge til nye agenter |
| **Robusthet** | Hvis én agent feiler, kan andre kompensere |

### Sammenlikning med tradisjonelle LLM-er

| | Tradisjonell LLM | Agentisk system |
|--|-----------------|-----------------|
| **Arkitektur** | Én modell | Flere samarbeidende agenter |
| **Problemløsning** | Lineær | Iterativ og kollaborativ |
| **Kvalitetskontroll** | Begrenset | Peer review mellom agenter |
| **Kompleksitet** | Begrenset av kontekst | Kan håndtere større problemer |

### Nøkkelkonsepter i Agent Framework

**Agenter** – Autonome enheter med instruksjoner og eventuelt verktøy.

**Team (GroupChat)** – Agenter organisert i et team med en orchestrator som styrer hvem som snakker når.

**Modellklienter** – Kobler agentene til språkmodeller:
- `AzureOpenAIChatClient` – for chat-baserte agenter
- `AzureOpenAIResponsesClient` – for strukturerte svar

**Verktøy** – Python-funksjoner agenter kan kalle:
```python
@tool(approval_mode="never_require")
async def web_search(query: str) -> str:
    """Søk etter informasjon på nettet"""
    results = DDGS().text(query, max_results=5)
    return str(results)
```

**Kjøring med streaming:**
```python
stream = team.run(task, stream=True)
await process_event_stream(stream)
```
