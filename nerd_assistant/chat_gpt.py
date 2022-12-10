import os
from functools import lru_cache

import openai
from pychatgpt import Chat, Options


def ask_davinci(prompt: str) -> str:
    """
    Asks davinci question.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]


@lru_cache()
def get_chat(unique_id: str) -> Chat:
    """
    Create new chat with AI.
    """
    options = Options()

    # Track conversation
    options.track = True

    # Optionally, you can pass a file path to save the conversation
    # They're created if they don't exist
    options.chat_log = f"chat_log_{unique_id}.txt"
    options.id_log = f"id_log_{unique_id}.txt"

    email = os.getenv("OPENAI_EMAIL", "")
    password = os.getenv("OPENAI_PASSWORD", "")

    # Create a Chat object
    return Chat(email=email, password=password, options=options)
