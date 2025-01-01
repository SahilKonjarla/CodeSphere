import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from app.utils.prompts import get_orchestrator_prompt
from app.services.debug_service import process_debug_request
from app.services.optimize_service import process_optimize_request
from app.services.document_service import (
    process_docstring_request,
    process_comments_request,
    process_overview_request,
    process_readme_request,
)

# Load environment variable
load_dotenv()  # Ensure the .env file is loaded

# Access the API key
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
if not OPEN_AI_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")


@tool
async def debug_tool(code: str, user_id: str) -> dict:
    """
    Debugs the given code
    :param code: the code to be debugged
    :param user_id: id of the current user
    :return: issues, suggestions, and explanation
    """

    return process_debug_request(code, user_id)


@tool
async def optimize_tool(code: str, user_id: str, goal: str = 'performance') -> dict:
    """
    Optimizes given code
    :param code: The code to be optimized
    :param user_id: id of the current user
    :param goal: What the user wants to be optimized
    :return: Optimizes the given code for the specified goal and returns suggestions and explanation
    """

    return process_optimize_request(code, user_id, goal)


@tool
async def document_tool(code: str, user_id: str, doc_type: str) -> dict:
    """
    Generates documents for given code
    :param code: The code given
    :param user_id: Id of the current user
    :param doc_type: The type of documentation
    :return: The documentation from the agent
    """

    if doc_type == "docstring":
        return process_docstring_request(code, user_id)
    elif doc_type == "comments":
        return process_comments_request(code, user_id)
    elif doc_type == "overview":
        return process_overview_request(code, user_id)
    elif doc_type == "readme":
        return process_readme_request(code, user_id)


def initialize_orchestrator():
    """
    Initializes the orchestrator service
    :return: Initialized orchestrator service with the registered tools
    """

    tools = [
        debug_tool,
        optimize_tool,
        document_tool,
    ]
    memory = MemorySaver()
    model = ChatOpenAI(model="gpt-4o-mini")
    agent_exec = create_react_agent(model, tools, checkpointer=memory)
    return agent_exec
