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

# User cookies storage file
USER_COOKIES_FILE = Path(__file__).resolve().parent / "user_cookies.json"

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

def load_user_cookies():
    """Load user cookies from JSON file"""
    if not USER_COOKIES_FILE.exists():
        return {}

    try:
        with USER_COOKIES_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading user cookies: {e}")
        return {}

def save_user_cookies(user_cookies):
    """Save user cookies to JSON file"""
    try:
        with USER_COOKIES_FILE.open("w", encoding="utf-8") as f:
            json.dump(user_cookies, f, ensure_ascii=False, indent=2)
        logging.info(f"User cookies saved to {USER_COOKIES_FILE}")
    except Exception as e:
        logging.error(f"Error saving user cookies: {e}")

def get_user_cookie(user_id):
    """Get cookie for a specific user"""
    user_cookies = load_user_cookies()
    return user_cookies.get(str(user_id))

def set_user_cookie(user_id, cookie):
    """Set cookie for a specific user"""
    user_cookies = load_user_cookies()
    user_cookies[str(user_id)] = cookie
    save_user_cookies(user_cookies)

def remove_user_cookie(user_id):
    """Remove cookie for a specific user"""
    user_cookies = load_user_cookies()
    if str(user_id) in user_cookies:
        del user_cookies[str(user_id)]
        save_user_cookies(user_cookies)
        return True
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cookie = get_user_cookie(user_id)

    if cookie:
        await update.message.reply_text(
            "欢迎回来！\n\n"
            "可用命令：\n"
            "/flow - 查询今日流量使用情况\n"
            "/setcookie <cookie> - 更新你的 Wgetcloud Cookie\n"
            "/removecookie - 删除你的 Wgetcloud Cookie"
        )
    else:
        await update.message.reply_text(
            "你好！欢迎使用 Wgetcloud 流量查询机器人。\n\n"
            "首次使用需要设置你的 Wgetcloud Cookie：\n"
            "/setcookie <your_wgetcloud_cookie>\n\n"
            "设置后即可使用：\n"
            "/flow - 查询今日流量使用情况"
        )

async def setcookie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if cookie is provided
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "请提供你的 Wgetcloud Cookie：\n"
            "/setcookie <your_wgetcloud_cookie>\n\n"
            "获取 Cookie 的方法：\n"
            "1. 登录 Wgetcloud 网站\n"
            "2. 打开浏览器开发者工具 (F12)\n"
            "3. 在 Network 标签页找到请求头中的 Cookie"
        )
        return

    # Get cookie from command arguments
    cookie = " ".join(context.args)

    # Save cookie for this user
    set_user_cookie(user_id, cookie)

    logging.info(f"User {user_id} set their cookie")
    await update.message.reply_text(
        "✅ Cookie 已保存！\n\n"
        "现在你可以使用 /flow 命令查询流量了。"
    )

async def removecookie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if remove_user_cookie(user_id):
        logging.info(f"User {user_id} removed their cookie")
        await update.message.reply_text("✅ 你的 Cookie 已被删除。")
    else:
        await update.message.reply_text("❌ 你还没有设置 Cookie。")

async def flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cookie = get_user_cookie(user_id)

    if not cookie:
        await update.message.reply_text(
            "❌ 你还没有设置 Wgetcloud Cookie。\n\n"
            "请先使用以下命令设置：\n"
            "/setcookie <your_wgetcloud_cookie>"
        )
        return

    try:
        traffic_dic = get_today_traffic.traffic(cookie)
        traffic = traffic_dic.get("traffic", 0)
        unit = traffic_dic.get("unit", "G")
        traffic_flow_message = f"今日已使用 {traffic}{unit}"
        await update.message.reply_text(traffic_flow_message)
        logging.info(f"User {user_id} queried traffic successfully")
    except Exception as e:
        logging.error(f"Error getting traffic for user {user_id}: {e}")
        await update.message.reply_text(
            "❌ 查询失败，请检查你的 Cookie 是否有效。\n\n"
            "如需更新 Cookie，请使用：\n"
            "/setcookie <your_wgetcloud_cookie>"
        )

async def remain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    cookie = get_user_cookie(user_id)

    if not cookie:
        await update.message.reply_text(
            "❌ 你还没有设置 Wgetcloud Cookie。\n\n"
            "请先使用以下命令设置：\n"
            "/setcookie <your_wgetcloud_cookie>"
        )
        return

    try:
        result = get_today_traffic.parse_traffic_and_reset_date(cookie)
        remain_flow = round(result.get("total_traffic") - result.get("used_traffic"), 2)
        unit = result.get("traffic_unit")
        available_days = result.get("available_days")
        message = f"剩余流量：{remain_flow}{unit}（{available_days}天）"
        await update.message.reply_text(message)
        logging.info(f"User {user_id} queried remain flow successfully")
    except Exception as e:
        logging.error(f"Error getting remain flow for user {user_id}: {e}")
        await update.message.reply_text(
            "❌ 查询失败，请检查你的 Cookie 是否有效。\n\n"
            "如需更新 Cookie，请使用：\n"
            "/setcookie <your_wgetcloud_cookie>"
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"You say: {text}")

if __name__ == "__main__":
    if len(sys.argv) > 2 and os.path.exists(sys.argv[1]):
        config = load_json(sys.argv[1])
    else:
        config = load_json()
    TG_TOKEN = config.get("TG_TOKEN")

    app = ApplicationBuilder().token(TG_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("flow", flow))
    app.add_handler(CommandHandler("remain", remain))
    app.add_handler(CommandHandler("setcookie", setcookie))
    app.add_handler(CommandHandler("removecookie", removecookie))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logging.info("Bot started. User cookie storage enabled.")
    app.run_polling()
