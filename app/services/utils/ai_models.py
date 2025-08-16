import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import openai

load_dotenv()

# API keys
groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")


def get_llm(provider: str = "groq", model: str = None):
    """
    Returns a chat model dynamically based on provider + model.
    Supported providers: groq, openai, anthropic
    """
    if provider == "groq":
        return ChatGroq(model=model or "openai/gpt-oss-20b", groq_api_key=groq_api_key)
    
    elif provider == "openai":
        return openai.ChatCompletion.create(
            model=model or "gpt-4o-mini",
            api_key=openai_api_key
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")
