# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python automation project for monitoring Wgetcloud traffic usage. The project consists of two independent modules that share common traffic-fetching logic:

1. **api_get_traffic**: Flask HTTP API service for querying traffic via REST endpoint
2. **telegram_bot**: Telegram bot for querying traffic via chat commands

Both modules use web scraping (via cloudscraper) to fetch traffic data from Wgetcloud's user panel.

## Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install flask cloudscraper fake-useragent python-telegram-bot
```

### Running Services

**Flask API:**
```bash
# Run from project root
python -m api_get_traffic.api_get_traffic
# Runs on http://0.0.0.0:5000
```

**Telegram Bot:**
```bash
# Run from project root (default config)
python -m telegram_bot.main

# Or with custom config path
python -m telegram_bot.main /path/to/config.json
```

### Testing API
```bash
# Test the Flask API with curl
curl -H "X-API-TOKEN: your_token_here" http://127.0.0.1:5000/
```

## Architecture

### Module Structure

```
api_get_traffic/
├── api_get_traffic.py       # Flask app with token auth
├── get_today_traffic.py     # Core scraping logic
└── config.json              # WG_COOKIE, API_TOKEN

telegram_bot/
├── main.py                  # Bot handlers and polling
└── config.json              # TG_TOKEN, WG_COOKIE
```

### Data Flow

**For Telegram Bot:**
```
User → Telegram /flow command → telegram_bot/main.py →
api_get_traffic/get_today_traffic.py → Wgetcloud API → Response
```

**For API Service:**
```
HTTP Client → Flask (token auth) → get_today_traffic.py →
Wgetcloud API → JSON Response
```

### Key Implementation Details

**Configuration Loading:**
- Both modules use `load_json()` to read `config.json` from their respective directories
- Path resolution uses `Path(__file__).resolve().parent` for module-relative paths
- Config files must be in the same directory as the main module file

**Traffic Scraping Logic (`get_today_traffic.py`):**
- Uses `cloudscraper` to bypass Cloudflare protection
- Posts to `https://3jkkvi9afjjln2yjwnbc.wgetcloud.org/user/log_month` with date range
- Date range: yesterday to today (format: "YYYY-MM-DD 至 YYYY-MM-DD")
- Response format: `{"date":["...","..."],"t":[float,float],"t_u":[...],"t_d":[...]}`
- Extracts `data_dict.get('t')[1]` for today's traffic (index 1, not 0)
- Auto-converts units: <1 GB → multiply by 1000 for MB display

**Authentication:**
- Flask API: Custom token auth via `X-API-TOKEN` header, compared against `API_TOKEN` from config
- Wgetcloud: Cookie-based authentication via `WG_COOKIE` in request headers

**Telegram Bot Handlers:**
- `/start`: Welcome message (customized based on whether user has set cookie)
- `/setcookie <cookie>`: Set or update user's Wgetcloud Cookie
- `/flow`: Query traffic using user's stored cookie and return result
- `/removecookie`: Delete user's stored cookie
- Plain text: Echo with "You say: {text}" prefix

**User Cookie Storage:**
- Each Telegram user's cookie is stored in `telegram_bot/user_cookies.json`
- Format: `{"user_id": "cookie_value", ...}`
- File is auto-generated on first user registration
- Already added to `.gitignore` for security

## Configuration Files

Each module requires its own `config.json` in its directory:

**api_get_traffic/config.json:**
```json
{
  "WG_COOKIE": "your_wgetcloud_cookie",
  "API_TOKEN": "your_api_token"
}
```

**telegram_bot/config.json:**
```json
{
  "TG_TOKEN": "your_telegram_bot_token"
}
```

**Note:** The Telegram bot no longer requires `WG_COOKIE` in config.json. Each user sets their own cookie via the `/setcookie` command, which is stored in `user_cookies.json`.

These config files are git-ignored via each module's `.gitignore`.

## Important Notes

- The Wgetcloud URL is hardcoded in `get_today_traffic.py:22`
- If Wgetcloud changes their panel structure or URL, update the scraping logic accordingly
- The traffic data extraction assumes the response JSON structure remains consistent
- Both modules import `get_today_traffic` from `api_get_traffic` package, meaning telegram_bot depends on api_get_traffic module
- When running modules as scripts, always use `python -m` notation from project root to ensure proper imports
- **Multi-user support**: Telegram bot now stores each user's cookie separately in `user_cookies.json`
- Each Telegram user must set their own Wgetcloud cookie via `/setcookie` command before querying traffic
- User cookies are identified by Telegram user ID and stored persistently across bot restarts
