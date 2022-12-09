"""
Implementation of the nerd_assistant command line interface.
"""

import os

import typer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from nerd_assistant.chat_gpt import get_chat

app = typer.Typer()


async def answer(update: Update, _) -> None:
    """
    Answer question of user.
    """

    message = update.message["text"]
    assert isinstance(message, str)

    try:
        ai_answer = get_chat().ask(message.replace("/kurva", ""))
        await update.message.reply_text(ai_answer)

    except Exception as e:
        print(e)
        await update.message.reply_text("You broke the AI 💀")


@app.command(help="Run bot")
def start() -> None:
    """
    Starts the bot.
    """

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    bot = ApplicationBuilder().token(token).build()

    bot.add_handler(CommandHandler("kurva", answer))
    bot.run_polling()
