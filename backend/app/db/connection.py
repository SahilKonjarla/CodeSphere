import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch DB credentials from .env file
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def get_db_connection():
    """
    Establishes a connection to the PSQL database
    :return: A connection to the database
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"Unable to connect to the database: str{e}")
