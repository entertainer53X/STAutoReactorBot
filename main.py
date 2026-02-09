import os
import asyncio
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application,
    ChannelPostHandler,
    ContextTypes
)

# ===== ENVIRONMENT VARIABLES =====
BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
WEBHOOK_PATH = "/webhook"

# ===== EXACT 11 REACTIONS (must match channel settings) =====
REACTIONS = [
    "👍", "❤️", "😂", "🔥", "👏",
    "😍", "😎", "🤩", "😱", "🙏", "💯"
]

DELAY_SECONDS = 10

# ===== FASTAPI APP =====
app = FastAPI()

telegram_app = Application.builder().token(BOT_TOKEN).build()

# ===== REACTION HANDLER =====
async def react_with_all_11(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post

    for emoji in REACTIONS:
        await context.bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[emoji]
        )
        await asyncio.sleep(DELAY_SECONDS)

telegram_app.add_handler(ChannelPostHandler(react_with_all_11))

# ===== STARTUP: SET WEBHOOK =====
@app.on_event("startup")
async def startup():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)

# ===== WEBHOOK ENDPOINT =====
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    upd
