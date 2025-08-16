from typing import List
from app.schemas.ai import AIReviewResponse, TopicSuggestion
from .utils.ai_client import run_ai_task
from .utils.ai_models import get_llm
from .utils.ai_prompts import review_prompt, topic_prompt

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
