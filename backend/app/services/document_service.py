import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.utils.prompts import (
    get_docstring_prompt,
    get_comments_prompt,
    get_overview_prompt,
    get_readme_prompt,
)

# Load environment variable
load_dotenv()  # Ensure the .env file is loaded

# Access the API key
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
if not OPEN_AI_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")

# Initialize LLM
model = ChatOpenAI(OPEN_AI_KEY)


# Middleware function to call the correct document type
def call_documentation_type(code: str, doc_type: str):
    # Check for the specific docstring and call the correct function
    if doc_type == "docstring":
        return process_docstring_request(code)
    elif doc_type == "comments":
        return process_comments_request(code)
    elif doc_type == "overview":
        return process_overview_request(code)
    elif doc_type == "readme":
        return process_readme_request(code)


# Helper function to interact with LangChain
def call_agent(prompt):
    """
    :param prompt: The formatted prompt for the LLm
    :return: The parsed response
    """

    # Use LangChain and send prompt to the LLM
    response = model.invoke(prompt)
    return response


# Helper function to parse the agent_response
def parse_agent_response(response: str) -> dict:
    """
    :param response: The raw response from the LLM
    :return: dict: A structured response containing inefficiencies, suggestions, explanations
    """
    parsed_data = {
        "docstring": [],
        "readme": [],
        "overview": [],
        "comment": []
    }

    try:
        # Split the response by sections if structured
        print(response.content)
        lines = response.content.split("\n")
        docstring_section = False
        readme_section = False
        overview_section = False
        comments_section = False
        for line in lines:
            if "Docstring" in line:
                docstring_section = True
                readme_section = False
                overview_section = False
                comments_section = False
            elif "README" in line:
                readme_section = True
                docstring_section = False
                overview_section = False
                comments_section = False
            elif "Overview" in line:
                overview_section = True
                docstring_section = False
                readme_section = False
                overview_section = False
            elif "Comments" in line:
                comments_section = True
                docstring_section = False
                readme_section = False
                overview_section = False
            elif docstring_section:
                parsed_data["docstring"].append(line.strip())
            elif readme_section:
                parsed_data["readme"].append(line.strip())
            elif overview_section:
                parsed_data["overview"].append(line.strip())
            elif comments_section:
                parsed_data["comment"].append(line.strip())

    except Exception as e:
        parsed_data["docstring"] = f"Error parsing response: {str(e)}"

    return parsed_data


# Process docstring request
def process_docstring_request(code: str):
    """
    :param code: The code snippet from the user
    :return: The parsed LLM response
    """

    # A check to see if the user inputted the code
    if not code.strip():
        raise ValueError("Code cannot be empty")

    # Prompt for the agent
    prompt = get_docstring_prompt(code)

    try:
        agent_response = call_agent(prompt)
    except Exception as e:
        raise RuntimeError(f"Error communicating with docstring_agent: {str(e)}")

    # Parse the response and extract useful information
    parsed_response = parse_agent_response(agent_response)
    return parsed_response


# Process comments request
def process_comments_request(code: str):
    """
    :param code: The code snippet from the user
    :return: The parsed LLM response
    """

    # A check to see if the user inputted the code
    if not code.strip():
        raise ValueError("Code cannot be empty")

    # Prompt for the agent
    prompt = get_comments_prompt(code)

    try:
        agent_response = call_agent(prompt)
    except Exception as e:
        raise RuntimeError(f"Error communicating with docstring_agent: {str(e)}")

    # Parse the response and extract useful information
    parsed_response = parse_agent_response(agent_response)
    return parsed_response


# Process overview request
def process_overview_request(code: str):
    """
    :param code: The code snippet from the user
    :return: The parsed LLM response
    """

    # A check to see if the user inputted the code
    if not code.strip():
        raise ValueError("Code cannot be empty")

    # Prompt for the agent
    prompt = get_overview_prompt(code)

    try:
        agent_response = call_agent(prompt)
    except Exception as e:
        raise RuntimeError(f"Error communicating with docstring_agent: {str(e)}")

    # Parse the response and extract useful information
    parsed_response = parse_agent_response(agent_response)
    return parsed_response


# Process README request
def process_readme_request(code: str):
    """
    :param code: The code snippet from the user
    :return: The parsed LLM response
    """

    # A check to see if the user inputted the code
    if not code.strip():
        raise ValueError("Code cannot be empty")

    # Prompt for the agent
    prompt = get_docstring_prompt(code)

    try:
        agent_response = call_agent(prompt)
    except Exception as e:
        raise RuntimeError(f"Error communicating with docstring_agent: {str(e)}")

    # Parse the response and extract useful information
    parsed_response = parse_agent_response(agent_response)
    return parsed_response
