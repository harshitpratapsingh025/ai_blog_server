import os
from typing import List
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.schemas.ai import AIReviewResponse, TopicSuggestion

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=groq_api_key)

async def ai_review(title: str, content: str):
    try:
        parser = JsonOutputParser(pydantic_object=AIReviewResponse)

        # Prompt with format instructions
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an expert blog reviewer. "
             "Analyze the given blog and return a structured JSON response."),
            ("user", 
             "Review the following blog post and suggest improvements:\n\n"
             "Title: {title}\n\nContent: {content}\n\n"
             "{format_instructions}")
        ])

        # Add parser instructions to the prompt
        prompt = prompt.partial(format_instructions=parser.get_format_instructions())

        chain = prompt | llm | parser

        # Run asynchronously
        result = await chain.ainvoke({"title": title, "content": content})

        return result

    except Exception as e:
        print("---------ERROR-------------", e)
        return {"error": str(e)}

async def suggest_topics(past_titles: List[str]):
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are a helpful assistant. "
             "Suggest exactly 3 blog topic titles and one-line descriptions "
             "based on the user's past titles. "
             "The response must be a valid JSON array of 3 objects, each with keys: "
             "'title' (string) and 'description' (string)."),
            ("user", "Past titles:\n{titles}")
        ])
        
        parser = JsonOutputParser(pydantic_object=TopicSuggestion)
        
        prompt = prompt.partial(format_instructions=parser.get_format_instructions())

        chain = prompt | llm | parser
        
        result = await chain.ainvoke({"titles": "\n".join(past_titles)})
        return result
    
    except Exception as e:
        print('---------ERROR-------------', e)
        return {"error": str(e)}
