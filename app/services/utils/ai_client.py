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
