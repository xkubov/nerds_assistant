import os
from functools import lru_cache

from pychatgpt import Chat, Options


@lru_cache()
def get_chat() -> Chat:
    """
    Create new chat with AI.
    """
    options = Options()

    # Track conversation
    options.track = True

    # Optionally, you can pass a file path to save the conversation
    # They're created if they don't exist
    options.chat_log = "chat_log.txt"
    options.id_log = "id_log.txt"

    email = os.getenv("OPENAI_EMAIL", "")
    password = os.getenv("OPENAI_PASSWORD", "")

    # Create a Chat object
    return Chat(email=email, password=password, options=options)
