import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variable
load_dotenv()  # Ensure the .env file is loaded

# Access the API key
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
if not OPEN_AI_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")

# Initialize LLM
model = ChatOpenAI(OPEN_AI_KEY)

def process_documentation_request(code: str, )
