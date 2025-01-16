import os
from dotenv import load_dotenv
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
import json
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
def optimize_tool(code: str, user_id: str, goal: str = 'performance') -> dict:
    """
    Optimizes given code
    :param code: The code to be optimized
    :param user_id: id of the current user
    :param goal: What the user wants to be optimized
    :return: Optimizes the given code for the specified goal and returns suggestions and explanation
    """

    return process_optimize_request(code, user_id, goal)


@tool
def document_tool(code: str, user_id: str, doc_type: str) -> dict:
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


def parse_response(response):
    """

    :param response: The raw response from the LLm
    :return: A dictionary with the structured response from the specified agent
    """
    extracted_contents = []
    try:
        # Iterate through all messages in the response
        for message in response.get("messages", []):
            # Handle different types of message objects
            if hasattr(message, "type") and message.type == "tool":
                # Access attributes directly for non-dictionary objects
                content = getattr(message, "content", None)

                # Parse content if it's a JSON string
                if content:
                    try:
                        parsed_content = json.loads(content)
                        extracted_contents.append(parsed_content)
                    except json.JSONDecodeError:
                        # If content is not valid JSON, append the raw string
                        extracted_contents.append(content)
    except Exception as e:
        print(f"Exception while parsing response: {e}")

    return extracted_contents


def process_orchestrator_request(request) -> list:
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
    response = parse_response(result)

    return response
