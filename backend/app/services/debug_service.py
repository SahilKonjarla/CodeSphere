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


def process_debug_request(code: str):
    """
    Process the debugging request and return structured results.
    Args:
        code (str): The code snippet to debug.

    Returns:
        dict: A structured response with debugging results.
    """

    # A check to see if the user inputted code
    if not code.strip():
        raise ValueError("Code Snippet cannot be empty")

    # Prompt for the agent
    prompt = f"""
    You are an expert debugging assistant. Your job is to analyze code for errors and provide detailed explanations and solutions.

    Here is the code snippet that needs to be debugged:
    {code}
    
    Your task is to:
    1. Identify any syntax, logical, or runtime errors in the code. Be specific about the issues and indicate the line numbers if possible.
    2. Suggest corrections or improvements for each issue.
    3. Provide a detailed explanation for each issue, including why it occurs and how your suggested solution resolves it.
    
    If the code has no errors, confirm that it is valid and explain why the code works correctly.
    
    Return the output in the following structure:
    - Errors: A list of identified issues in the code.
    - Suggestions: A list of corrections or improvements.
    - Explanation: A detailed explanation of the errors and solutions.
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
    :param response: Parses the raw response from the LLM.
    :return: dict : A structure response containing issues, suggestions, and explanations.
    """
    parsed_data = {
        "errors": [],
        "suggestions": [],
        "explanation": []
    }

    try:
        # Split the response by sections if structured
        print(response.content)
        lines = response.content.split("\n")
        errors_section = False
        suggestions_section = False
        explanation_section = False
        for line in lines:
            if "Errors" in line:
                errors_section = True
                suggestions_section = False
                explanation_section = False
            elif "Suggestions" in line:
                errors_section = False
                suggestions_section = True
                explanation_section = False
            elif "Explanation" in line:
                explanation_section = True
                suggestions_section = False
                errors_section = False
            elif errors_section:
                parsed_data["errors"].append(line.strip())
            elif suggestions_section:
                parsed_data["suggestions"].append(line.strip())
            elif explanation_section:
                parsed_data["explanation"].append(line.strip())

    except Exception as e:
        parsed_data["explanation"] = f"Error parsing response: {str(e)}"

    return parsed_data
