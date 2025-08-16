from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key="docker", base_url="http://localhost:12434/engines/v1")

prompt = f"""
        Suggest exactly 2 blog topic titles and one-line descriptions based on these past titles: Run LLMs Locally With Docker Model Runner.
        Return ONLY raw JSON — no extra text, no explanation, no code block formatting.
        The JSON must be an array of exactly 2 objects, each with keys: "title" (string) and "description" (string).
"""
response = client.chat.completions.create(
    model="ai/smollm3",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.8,
    max_tokens=4000,
)
content = response.choices[0].message.content
print(content)
