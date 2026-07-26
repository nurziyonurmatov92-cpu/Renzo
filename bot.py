"""
Har qanday savolga javob beradigan Telegram bot
"""

import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from anthropic import Anthropic

# Tokenlar Railway'ning Environment Variables bo'limidan o'qiladi
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

client = Anthropic(api_key=ANTHROPIC_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 👋\n\n"
        "Menga istalgan savolingizni yozing — masalan:\n"
        "• \"Ronaldo qachon tug'ilgan?\"\n"
        "• \"Yaxshi musiqiy film tavsiya qil\"\n\n"
        "Javob berishga harakat qilaman! 🤖"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Oddiy: menga har qanday savolingizni matn qilib yuboring, "
        "men javob beraman."
    )


async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    chat_id = update.effective_chat.id

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
