<h1 align="center">🤖 Anonymous ChatBot</h1>

<p align="center">
  An anonymous Telegram chat bot built with <strong>aiogram 3</strong> and real-time partner matching
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/aiogram-3.x-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="aiogram">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

<p align="center">
  <a href="https://t.me/fsoky_community">
    <img src="https://img.shields.io/badge/Telegram-Community-26A5E4?style=for-the-badge&logo=telegram" alt="Telegram Community">
  </a>
</p>

---

## ✨ Features

- **Anonymous matching** — automatically pairs two users waiting for a chat partner
- **Media & text** — supports text, stickers, photos, videos, documents, voice messages, and audio
- **Replies & editing** — reply threading and synced message edits between partners
- **Localization** — Russian and English via Fluent (`fluentogram`)
- **FSM Scenes** — dialog state management using aiogram 3 built-in scenes
- **Docker** — ready-to-use `docker-compose` with MongoDB and mongo-express

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Telegram API | [aiogram](https://docs.aiogram.dev/) 3.x |
| Database | MongoDB + [motor](https://motor.readthedocs.io/) |
| Configuration | [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| i18n | [fluentogram](https://github.com/life4/fluentogram) |
| Package manager | [uv](https://docs.astral.sh/uv/) |

## 📁 Project Structure

```
anonimchatbot-aiogram3/
├── src/
│   ├── __main__.py              # Entry point
│   ├── bot/
│   │   ├── handlers/            # Routers and FSM scenes
│   │   ├── keyboards/           # Reply keyboards
│   │   ├── middlewares/         # UserMiddleware (DB + i18n)
│   │   ├── filters/             # Custom filters
│   │   └── utils/
│   ├── core/
│   │   ├── config.py            # Settings and TranslatorHub
│   │   └── locales/             # ru.ftl / en.ftl
│   └── db/
│       ├── models/              # Pydantic models
│       └── repositories/        # MongoDB access layer
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── .env.example
```

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Fsoky/anonimchatbot-aiogram3.git
cd anonimchatbot-aiogram3
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` — at minimum, set `BOT_TOKEN` and `DB_URL`:

```env
BOT_TOKEN=123456:ABC-DEF...
DB_URL=mongodb://localhost:27017
```

> [!TIP]
> Get your bot token from [@BotFather](https://t.me/BotFather) on Telegram.

### 3. Install dependencies

```bash
# Install uv: https://docs.astral.sh/uv/getting-started/installation/
uv sync
```

### 4. Start MongoDB

Locally or via Docker:

```bash
docker run -d --name mongo -p 27017:27017 mongo
```

### 5. Run the bot

```bash
uv run python src/__main__.py
```

## 🐳 Docker Compose

Full stack: bot + MongoDB + mongo-express (web DB admin UI).

```bash
cp .env.example .env
# Fill in BOT_TOKEN and change passwords in .env
docker compose up --build
```

This starts three services:

| Service | Container | Description |
|---------|-----------|-------------|
| `anonchat-telegram` | `anonbot-tg` | Telegram bot |
| `mongo` | `mongo-anonbot-tg` | Database |
| `mongo-express` | `mongo-express-anonbot-tg` | DB admin UI → `http://localhost:8081` |

> [!IMPORTANT]
> For Docker, set `DB_URL` with MongoDB credentials:
> ```env
> DB_URL=mongodb://root:CHANGE_ME@mongo:27017/
> ```
> Or call `config.set_project_level("prod")` in `src/__main__.py` — the URL will be built automatically from `MONGO_INITDB_*` variables.

Run in the background:

```bash
docker compose up -d
```

## ⚙️ Environment Variables

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Telegram bot token |
| `DB_URL` | MongoDB connection URI |
| `MONGO_INITDB_ROOT_USERNAME` | MongoDB root username (Docker) |
| `MONGO_INITDB_ROOT_PASSWORD` | MongoDB root password (Docker) |
| `ME_CONFIG_BASICAUTH_USERNAME` | mongo-express login |
| `ME_CONFIG_BASICAUTH_PASSWORD` | mongo-express password |

## 💬 Bot Commands

| Command | Action |
|---------|--------|
| `/start` | Main menu, shows number of users searching |
| `/search` | Start searching for an anonymous chat partner |
| `/cancel` | Cancel the search |
| `/leave` | Leave the current chat |
| `/next` | End the chat and immediately search for a new partner |

Keyboard buttons mirror the `search`, `cancel`, and `leave` commands.

## 🔄 How It Works

```mermaid
flowchart LR
    A["/start"] --> B{Status}
    B -->|IDLE| C["/search"]
    C --> D{Partner waiting?}
    D -->|Yes| E["CHATTING"]
    D -->|No| F["SEARCHING"]
    F --> G["Match found"]
    G --> E
    E --> H["/leave or /next"]
    H --> C
```

1. User taps **Search** — status changes to `SEARCHING`.
2. If another user is already searching — both move to `CHATTING` and can message each other.
3. The bot relays messages between partners without revealing identities.
4. `/leave` or `/next` ends the session and returns to the menu.

## 📄 License

Free to use and modify for your own projects.

---

<p align="center">
  Made with ☕ · <a href="https://t.me/fsoky_community">Telegram Community</a>
</p>
