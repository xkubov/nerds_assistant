"""
Implementation of the nerd_assistant command line interface.
"""

import os

import typer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from nerd_assistant.chat_gpt import get_chat

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
        response = ""
        chatbot = get_chat()
        async for line in chatbot.ask(question):
            response += line["choices"][0]["text"].replace("<|im_end|>", "")

        await update.message.reply_text(response)

    except Exception as e:
        print(e)
        await update.message.reply_text("You broke the AI 💀")


async def handler(update: Update, context) -> None:
    """Telegram handler. Checks for activation words."""
    activation_words = ["kurva", "smrad", "preco", "prečo", "proc", "proč", "why", "?"]
    message = update.message["text"].lower()
    for word in activation_words:
        if word in message:
            await chatgpt_answer(update, context)
            return


@app.command(help="Run bot")
def start() -> None:
    """
    Starts the bot.
    """

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")

    bot = ApplicationBuilder().token(token).build()

    bot.add_handler(CommandHandler("smrad", chatgpt_answer))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

    bot.run_polling()
