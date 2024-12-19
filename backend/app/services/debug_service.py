import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load Environment Variables
load_dotenv()  # ensure the .env file is loaded

# Access the API key
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
if not OPEN_AI_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")

# Initialize the LLM
model = ChatOpenAI(model="gpt-4o-mini")


def process_debug_request(code: str, language: str = "python"):
    """
    Process the debugging request and return structured results.
    Args:
        code (str): The code snippet to debug.
        language (str): The programming language of the code (default: Python).

    Returns:
        dict: A structured response with debugging results.
    """

    # A check to see if the user inputted code
    if not code.strip():
        raise ValueError("Code Snippet cannot be empty")

    # Prompt for the agent
    prompt = f"""
    You are going to be a friendly debugging assistant. You're task is to assist the developer in debugging their code i.e. help them find syntax,
    logic, or runtime errors. Now please analyze the following {language} code:
    {code}
    Identify any syntax, logic, or runtime errors. Explain the errors and suggest fixes. If there are no fixes to be made, just say there are no fixes
    to be made.
    """

    # Call the agent and get the response
    try:
        agent_response = call_agent(prompt)
    except Exception as e:
        raise RuntimeError(f"Error communicating with debug_agent: {str(e)}")

    # Parse the response and extract useful information
    parsed_response = parse_agent_response(agent_response)
    return parsed_response


# Helper function to interact with LangChain
def call_agent(prompt: str) -> str:
    """
    Sends a prompt to LangChain and returns the raw response.
    Args:
        prompt (str): The formatted prompt for the LLM.

    Returns:
        str: The raw response from the LLM.
    """

    # Use LangChain and send prompt to the LLM
    response = model.invoke(prompt)
    return response


# Helper function to parse the agent response
def parse_agent_response(response: str) -> dict:
    """
    Parses the raw response from the LLM.
    :param response:
    :return: dict : A structure response containing issues, suggestions, and explanations.
    """
    parsed_data = {
        "issues": [],
        "suggestions": [],
        "explanation": ""
    }

    try:
        # Split the response by sections if structured
        lines = response.split("\n")
        issues_section = False
        suggestions_section = False

        for line in lines:
            if "Issues:" in line:
                issues_section = True
                suggestions_section = False
            elif "Suggestions:" in line:
                issues_section = False
                suggestions_section = True
            elif issues_section:
                parsed_data["issues"].append(line.strip())
            elif suggestions_section:
                parsed_data["suggestions"].append(line.strip())
            else:
                parsed_data["explanation"] += f"{line.strip()} "

    except Exception as e:
        parsed_data["explanation"] = f"Error parsing response: {str(e)}"

    return parsed_data
