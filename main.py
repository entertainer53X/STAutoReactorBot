import os
import asyncio
from fastapi import FastAPI, Request

from telegram import Update, ReactionTypeEmoji
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# ENVIRONMENT VARIABLES
# =========================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("BOT_TOKEN or WEBHOOK_URL is missing")

# =========================
# CONFIG
# =========================
# EXACTLY the emojis enabled in your channel
REACTIONS = [
    "👍", "❤️", "❤️‍🔥", "🔥", "👏",
    "😍", "😇", "🎉", "💘", "🙏", "🕊️"
]

DELAY_SECONDS = 10

# =========================
# FASTAPI APP
# =========================
app = FastAPI()

# Health check (for UptimeRobot)
@app.get("/")
async def health_check():
    return {"status": "ok"}

# =========================
# TELEGRAM APPLICATION
# =========================
telegram_app = Application.builder().token(BOT_TOKEN).build()

# =========================
# CHANNEL POST HANDLER
# =========================
async def react_with_all_11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.channel_post:
        return

    message = update.channel_post
    applied_reactions = []  # keeps previously added reactions

    for emoji in REACTIONS:
        applied_reactions.append(ReactionTypeEmoji(emoji=emoji))

        await context.bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=applied_reactions
        )

        await asyncio.sleep(DELAY_SECONDS)

telegram_app.add_handler(
    MessageHandler(filters.UpdateType.CHANNEL_POST, react_with_all_11)
)

# =========================
# STARTUP: SET WEBHOOK
# =========================
@app.on_event("startup")
async def on_startup():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)

# =========================
# WEBHOOK ENDPOINT
# =========================
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
