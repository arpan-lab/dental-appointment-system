from langchain_groq import ChatGroq

from app.config.settings import settings


def get_llm():

    llm = ChatGroq(
        model=settings.model_name,
        temperature=settings.temperature,
        api_key=settings.groq_api_key,
    )

    return llm