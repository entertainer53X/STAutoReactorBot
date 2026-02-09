import asyncio
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, ChannelPostHandler, ContextTypes

BOT_TOKEN = "8409377553:AAGU1l_yF7VjsRKNVm1604TD9v1FPVZDIQM"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://YOUR-RENDER-APP.onrender.com/webhook"

# EXACT 11 reactions (must match channel settings)
REACTIONS = [
    "👍", "❤️", "😂", "🔥", "👏",
    "😍", "😎", "🤩", "😱", "🙏", "💯"
]

DELAY_SECONDS = 10

app = FastAPI()
telegram_app = Application.builder().token(BOT_TOKEN).build()

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

@app.on_event("startup")
async def startup():
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(WEBHOOK_URL)

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}
    