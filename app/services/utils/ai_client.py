import io
from fastapi.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

async def run_ai_task(
        prompt_template: ChatPromptTemplate, 
        schema, 
        variables: dict,
        llm
    ):
    try:
        parser = JsonOutputParser(pydantic_object=schema)
        prompt = prompt_template.partial(format_instructions=parser.get_format_instructions())

        chain = prompt | llm | parser
        return await chain.ainvoke(variables)
    
    except Exception as e:
        print("---------ERROR-------------", e)
        return {"error": str(e)}
    
async def run_ai_audio_task(
        text: str, 
        voice: str, 
        format: str,
        llm
    ):
    try:
        resp = llm.invoke({
            "input": text,
            "voice": voice if voice else "Cheyenne-PlayAI",
            "format": format if format else "mp3"
        })
        print("AI Audio Response:", resp)
        audio_bytes = resp.content if hasattr(resp, "content") else resp
        return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")

    except Exception as e:
        print("---------ERROR-------------", e)
        return {"error": str(e)}
