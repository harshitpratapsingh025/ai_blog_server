from langchain_core.prompts import ChatPromptTemplate

review_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert blog reviewer. "
     "Analyze the given blog and return a structured JSON response."),
    ("user", 
     "Review the following blog post and suggest improvements:\n\n"
     "Title: {title}\n\nContent: {content}\n\n{format_instructions}")
])

topic_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a helpful assistant. "
     "Suggest exactly 3 blog topic titles and one-line descriptions "
     "based on the user's past titles. "
     "The response must be a valid JSON array of 3 objects, each with keys: "
     "'title' (string) and 'description' (string)."),
    ("user", "Past titles:\n{titles}\n\n{format_instructions}")
])

post_summary_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a helpful assistant. "
     "Summarize the blog post and provide the estimated reading time. "
     "The response must be a valid JSON object with keys: "
     "'summary' (string) and 'reading_time' (int)."),
    ("user", "Blog post content:\n{content}\n\n{format_instructions}")
])
