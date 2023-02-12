import os
from functools import lru_cache

from revChatGPT.V2 import Chatbot


@lru_cache()
def get_chat() -> Chatbot:
    """
    Create new chat with AI.
    """
    email = os.getenv("OPENAI_EMAIL", "")
    password = os.getenv("OPENAI_PASSWORD", "")

    # Create a Chat object
    return Chatbot(email=email, password=password)
