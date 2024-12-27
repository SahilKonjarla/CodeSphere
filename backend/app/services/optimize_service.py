import datetime
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.utils.prompts import get_optimize_prompt
from app.db.user_logs import save_user_logs

# Load Environment Variable
load_dotenv()  # Ensure the .env file is loaded

# Access the API key
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
if not OPEN_AI_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")

# Initialize LLM
model = ChatOpenAI(model="gpt-4o-mini")


def process_optimize_request(user_id: str, code: str, goal: str = "Looking at the code given. Please improve either the structure, memory usage, or runtime"):
    """
    :param user_id: The id of the user
    :param code: The code to be optimized
    :param goal: What the user wants to be optimized
    :return: The LLM response
    """

    # A check to see if the user inputted code
    if not code.strip():
        raise ValueError("Code snippet cannot be empty")

    # Prompt for the agent
    prompt = get_optimize_prompt(code, goal)

    try:
        agent_response = call_agent(prompt)
    except Exception as e:
        raise RuntimeError(f"Error communicating with optimize_agent: {str(e)}")

    # Parse the response and extract useful information
    parsed_response = parse_agent_response(agent_response)
    save_user_logs(
        user_id=user_id,
        agent="optimize",
        request={
            "code": code,
            "goal": goal,
            "user_id": user_id
        },
        response=parsed_response,
        timestamp=datetime.datetime.now().isoformat(),
    )
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
        "explanation": []
    }

    try:
        # Split the response by sections if structured
        print(response.content)
        lines = response.content.split("\n")
        inefficiencies_section = False
        suggestions_section = False
        explanation_section = False
        for line in lines:
            if "Inefficiencies" in line:
                inefficiencies_section = True
                suggestions_section = False
                explanation_section = False
            elif "Suggestions" in line:
                suggestions_section = True
                inefficiencies_section = False
                explanation_section = False
            elif "Explanation" in line:
                explanation_section = True
                suggestions_section = False
                inefficiencies_section = False
            elif inefficiencies_section:
                parsed_data["inefficiencies"].append(line.strip())
            elif suggestions_section:
                parsed_data["suggestions"].append(line.strip())
            elif explanation_section:
                parsed_data["explanation"].append(line.strip())
    except Exception as e:
        parsed_data["explanation"] = f"Error parsing response: {str(e)}"

    return parsed_data
