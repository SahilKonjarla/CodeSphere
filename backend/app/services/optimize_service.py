import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load Environment Variable
load_dotenv()  # Ensure the .env file is loaded

# Access the API key
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
if not OPEN_AI_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")

# Initialize LLm
model = ChatOpenAI(model="gpt-4o-mini")


def process_optimize_request(code: str, goal: str = "Looking at the code given. Please improve either the structure, memory usage, or runtime"):
    """
    :param code: The code to be optimized
    :param goal: What the user wants to be optimized
    :return: The LLM response
    """

    # A check to see if the user inputted code
    if not code.strip():
        raise ValueError("Code snipped cannot be empty")

    # Prompt for the agent
    prompt = f"""
    You are an expert software optimizer specializing in analyzing code for inefficiencies and providing improvements. 

    Analyze the following code:
    
    {code}
    
    Your task is to:
    1. Identify inefficiencies in the code (e.g., redundant operations, slow algorithms, or excessive memory usage).
    2. Suggest specific optimizations to improve performance, reduce memory usage, or achieve other stated goals.
    3. Provide a detailed explanation for your suggestions, including why they improve the code and any trade-offs.
    
    Optimization Goal: {goal}
    If no inefficiencies are found, confirm that the code is already optimized and explain why no changes are necessary.
    
    In your output please structure it as such:
    Inefficiencies: Your response will go here
    Suggestions: Your response will go here
    Explanation: Your response will go here
    """

    try:
        agent_response = call_agent(prompt)
    except Exception as e:
        raise RuntimeError(f"Error communicating with optimize_agent: {str(e)}")

    # Parse the response and extract useful information
    parsed_response = parse_agent_response(agent_response)
    return parsed_response


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
        "inefficiencies": [],
        "suggestions": [],
        "explanations": ""
    }

    try:
        # Split the response by sections if structured
        lines = response.content.split("\n")
        inefficiencies_section = False
        suggestions_section = False

        for line in lines:
            if "Inefficiencies" in line:
                inefficiencies_section = True
                suggestions_section = False
            elif "Suggestions" in line:
                suggestions_section = True
                inefficiencies_section = False
            elif inefficiencies_section:
                parsed_data["inefficiencies"].append(line.strip())
            elif suggestions_section:
                parsed_data["suggestions"].append(line.strip())
            else:
                parsed_data["explanations"].append(line.strip())

    except Exception as e:
        parsed_data["explanations"] = f"Error parsing response: {str(e)}"

    return parsed_data
