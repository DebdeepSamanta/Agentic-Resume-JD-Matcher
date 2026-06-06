import os
import json
import re
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

_llm: ChatGroq | None = None


def get_llm() -> ChatGroq:
    """Return a cached ChatGroq instance."""
    global _llm
    if _llm is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY is not set in environment / .env file.")
        _llm = ChatGroq(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            api_key=api_key,
            temperature=0.2,
        )
    return _llm


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Send a prompt to Groq and return the raw text response."""
    llm = get_llm()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    response = llm.invoke(messages)
    return response.content


def call_llm_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Call the LLM and parse a JSON object from the response.
    """
    raw = call_llm(system_prompt, user_prompt)

    # Remove ```json ... ``` fences
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        # Try to extract the first {...} block
        match = re.search(r"\{.*\}", clean, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(
            f"LLM did not return valid JSON.\nRaw output:\n{raw}"
        )
