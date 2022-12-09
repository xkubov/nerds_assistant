"""
Implementation of the nerd_assistant command line interface.
"""

import os

import openai
import typer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from nerd_assistant.chat_gpt import ask_davinci, get_chat

app = typer.Typer()


async def chatgpt_answer(update: Update, _) -> None:
    """
    Answer question of user.
    """

    message = update.message["text"]
    assert isinstance(message, str)

    question = message.replace("/kurva", "").strip()
    if not question:
        await update.message.reply_text("?")
        return

    try:
        ai_answer = get_chat().ask(question)
        await update.message.reply_text(ai_answer)

    except Exception as e:
        print(e)
        await update.message.reply_text("You broke the AI 💀")


async def davinci_answer(update: Update, _) -> None:
    """
    Uses Davinci to answer.
    """
    message = update.message["text"]
    assert isinstance(message, str)

    question = message.replace("/smrad", "").strip()
    if not question:
        await update.message.reply_text("?")
        return

    try:
        await update.message.reply_text(ask_davinci(question))
    except Exception as e:
        print(e)
        await update.message.reply_text("You broke the AI 💀")


@app.command(help="Run bot")
def start() -> None:
    """
    Starts the bot.
    """

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    openai.api_key = openai_api_key

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # initialize chat.
    get_chat()

    bot = ApplicationBuilder().token(token).build()

    bot.add_handler(CommandHandler("kurva", chatgpt_answer))
    bot.add_handler(CommandHandler("smrad", davinci_answer))
    bot.run_polling()
