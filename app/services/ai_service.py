import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from app.schemas.ai import AIReviewResponse, PostSummary, TopicSuggestion
from .utils.ai_client import run_ai_audio_task, run_ai_task
from .utils.ai_models import get_llm
from .utils.ai_prompts import review_prompt, topic_prompt, post_summary_prompt

load_dotenv()

# API keys
openai_api_key = os.getenv("OPENAI_API_KEY")


async def ai_review(title: str, content: str, provider="groq", model=None):
    llm = get_llm(provider=provider, model=model)
    return await run_ai_task(
        prompt_template=review_prompt,
        schema=AIReviewResponse,
        variables={"title": title, "content": content},
        llm=llm
    )


async def suggest_topics(past_titles: List[str], provider="groq", model=None):
    llm = get_llm(provider=provider, model=model)
    return await run_ai_task(
        prompt_template=topic_prompt,
        schema=TopicSuggestion,
        variables={"titles": "\n".join(past_titles)},
        llm=llm
    )

async def ai_post_summarize(content: str, provider="groq", model=None):
    llm = get_llm(provider=provider, model=model)
    return await run_ai_task(
        prompt_template=post_summary_prompt,
        schema=PostSummary,
        variables={"content": content},
        llm=llm
    )

async def ai_post_text_to_speech(content: str, speech_file_path: str):
    client = OpenAI(api_key=openai_api_key)
    older_path = "app/public/audios"
    file_name = speech_file_path
    full_path = os.path.join(older_path, file_name)

    os.makedirs(older_path, exist_ok=True)
    model = "gpt-4o-mini-tts"
    voice = "coral"
    with client.audio.speech.with_streaming_response.create(
        model=model,
        voice=voice,
        input=content,
        instructions="Speak in a cheerful and positive tone.",
    ) as response:
        response.stream_to_file(full_path)