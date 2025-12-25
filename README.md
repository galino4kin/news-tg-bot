# Telegram News NLP Bot

Small Telegram bot that fetches top news for a topic and applies NLP: summarization and sentiment. Built for fast prototyping.

Made in collaboration with [@AlisaUrikh](https://github.com/AlisaUrikh).

**Content**

1. [Features](#features)  
2. [Flow](#flow)  
3. [Project layout](#project-layout)  
4. [Requirements](#requirements)  
5. [Setup](#setup)  
6. [How it works](#how-it-works)  
7. [Config](#config)  
8. [Testing](#testing)  
9. [Extending](#extending)  
10. [How to use](#how-to-use) 

## Features

* News search via [GNews API](https://gnews.io)
* Up to 5 top headlines with links
* Summarization via `gpt-4o-mini` by OpenAI
* Sentiment analysis of news `gpt-4o-mini` by OpenAI
* Simple Telegram bot interface

## Flow

```mermaid
---
config:
  theme: default
---
flowchart TD
    A((User)) --> B[TG API]
    B --> C[query -> API]
    C --> D[Google News Search]
    D --> E[JSON result]
    E --> F[NLP: summarize, sentiment]
    F --> G[output]
    G --> B
    B --> A
```

## Project layout

```
news-tg-bot/
├── .env
├── .gitignore
├── requirements.txt
├── config.py
├── text_loader.py
├── services/
│   ├── search.py
│   ├── nlp.py
│   └── telegram_bot.py
├── main.py
└── tests/
    ├── result.json
    └── test_flow.py
```

## Requirements

* Python 3.10+
* GNews API token
* OpenAI API token
* Telegram Bot token

## Setup

1. Clone and enter:

```bash
git clone <this-repo-url>
cd news-tg-bot
```

2. Create and activate venv:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

3. Install deps:

```bash
pip install -r requirements.txt
```

4. Fill `.env`:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_custom_search_engine_id
```

5. Run:

```bash
cd news_bot
python main.py
```

Open Telegram and send any topic to your bot.

## How it works

* `services/search_gnews.py` calls Google Custom Search to fetch news-like results for the topic.
* `services/nlp.py` calls OpenAI API for 
* `services/telegram_bot.py` wires Telegram handlers.

## Config

`config.py`:

```python
SEARCH_TOP_K = 5
SUMMARY_MAX_TOKENS = 256
```

Tune to your needs. Larger values cost more tokens and time.

## Testing

```bash
pytest -q
```

Simple smoke test calls the flow and checks output shape.

## Extending

* Add NER: new function in `services/nlp.py`.
* Add fact-check: create `services/factcheck.py`.
* Caching: add a small cache layer (e.g., `diskcache` or Redis) around search and model calls.

## How to use

1. Open the bot in Telegram and press **Start** (or send `/start`).
   - The bot will show a menu with 3 buttons:
     - **Топ новостей**
     - **Суммаризация и сентимент анализ**
     - **Помощь**

2. Choose what you want to do:

   **Option A: Top headlines**
   - Tap **Топ новостей** (or send `/top_news`)
   - Send a topic in the next message (at least 2 characters), for example:
     - `инфляция в Европе`
     - `курс рубля`
     - `искусственный интеллект`
   - The bot will return up to **5** headlines with source links (previews are disabled).

   **Option B: Summary + sentiment**
   - Tap **Суммаризация и сентимент анализ** (or send `/extra`)
   - Send a topic in the next message (at least 2 characters)
   - The bot will:
     - fetch up to **5** news items,
     - build a text from up to **3** articles,
     - generate a short summary,
     - return a sentiment label.

3. Help / commands
   - Tap **Помощь** (or send `/help`) to see available commands and tips.

Notes:
- If you send a topic without choosing an option first, the bot will ask you to select an action from the menu.
- If the topic is too short, the bot will ask you to retry.
- If no news is found for the query, the bot will return `Новости не найдены.` or `Недостаточно данных`.


<img width="735" height="490" alt="image" src="https://github.com/user-attachments/assets/d3fda35b-b1d9-47e8-81fb-626ba4ca03de" />
