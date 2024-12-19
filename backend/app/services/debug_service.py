import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load Environment Variables
load_dotenv() # ensure the .env file is loaded