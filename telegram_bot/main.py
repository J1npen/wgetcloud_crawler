import os 
import json
import logging
import sys
from pathlib import Path
from api_get_traffic import get_today_traffic

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def load_json(filename="config.json"):
    # main.py 所在目录
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / filename

    if not config_path.exists():
        logging.error(f"Cannot find config file: {config_path}")
        sys.exit(1)

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    logging.info(f"Json: Loaded {config_path}")
    return config

async def get_traffic_flow():
    url = "https://traffic.jinpen.icu"
    headers = {"X-API-TOKEN": WG_TOKEN}
    response = requests.get(url, headers=headers)
    return response.json().get("msg")

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi I can get you Wgetcloud traffic flow and tell you how many you use today!")

async def flow(update:Update, context: ContextTypes.DEFAULT_TYPE):
    traffic_flow_message = get_today_traffic.traffic(WG_COOKIE)
    await update.message.reply_text(traffic_flow_message)

async def echo(update:Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"You say: {text}")

if __name__ == "__main__":
    if len(sys.argv)>2 and os.path.exists(sys.argv[1]):
        config = load_json(sys.argv[1])
    else:
        config = load_json()
    TG_TOKEN = config.get("TG_TOKEN")
    WG_TOKEN = config.get("WG_TOKEN")
    WG_COOKIE = config.get("WG_COOKIE")

    app = ApplicationBuilder().token(TG_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("flow", flow))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()
