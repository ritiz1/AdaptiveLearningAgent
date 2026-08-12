from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv("app/.env")


def get_llm() -> ChatGroq:
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )

llm = get_llm()

