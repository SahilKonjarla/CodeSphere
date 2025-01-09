import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
# from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from app.utils.prompts import get_orchestrator_sys_prompt, get_orchestrator_prompt
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
def debug_tool(code: str, user_id: str) -> dict:
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
    :param user_id: id of the current user
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
    # memory = MemorySaver()
    model = ChatOpenAI(model="gpt-4o-mini")
    agent_exec = create_react_agent(model, tools)
    return agent_exec


def process_orchestrator_request(request) -> dict:
    """
    Handles user requests by invoking the appropriate tools via the orchestrator.
    :param request: request to be handled by the orchestrator
    :return: Aggregated response from the orchestrator
    """
    orchestrator = initialize_orchestrator()

    # Extract the details
    task = request.task
    code = request.code
    user_id = request.user_id
    additional_params = request.additional_params
    prompt = get_orchestrator_sys_prompt()
    prompt1 = get_orchestrator_prompt(task, code, user_id)
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=prompt1)
    ]
    result = orchestrator.invoke({"messages": messages}, {"recursion_limit": 100})
    """
    # Build a task-specific input for the orchestrator
    if task == "debug":
        return orchestrator.invoke({
            "messages": task,
            "code": code,
            "user_id": user_id,
        })
    elif task == "optimize":
        return orchestrator.invoke({
            "prompt": prompt,
            "code": code,
            "user_id": user_id,
            "goal": additional_params.get("goal", "performance"),
        })
    elif task == "document":
        return orchestrator.invoke({
            "prompt": prompt,
            "code": code,
            "user_id": user_id,
            "doc_type": additional_params.get("doc_type", "docstring"),
        })
    """
    return result
