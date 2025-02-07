import json
from app.db.connection import get_db_connection


# Ensure the response is JSON-serializable helper function
def ensure_json_serializable(data):
    if isinstance(data, dict):
        return {
            key: list(value) if isinstance(value, set) else ensure_json_serializable(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [ensure_json_serializable(item) for item in data]
    return data


def save_user_logs(user_id, agent, request, response, timestamp=None):
    """
    Inserts a new user log into the `user_logs` table.

    :param user_id: The ID of the user.
    :param agent: The name of the agent (e.g., debug, optimize, document).
    :param request: A dictionary containing the user's request.
    :param response: A dictionary containing the agent's response.
    :param timestamp: (Optional) The timestamp of the interaction.
    """
    cursor = None
    conn = None
    try:
        # Serialize the request and response
        serialized_response = json.dumps(ensure_json_serializable(response))
        serialized_request = json.dumps(ensure_json_serializable(request))

        # Initialize connection to database and create interaction instance
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query for the database
        query = f"""
            INSERT INTO user_logs (user_id, agent, request, response, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """

        # Query execution
        cursor.execute(
            query,
            (
                user_id,
                agent,
                serialized_request,
                serialized_response,
                timestamp,
            ),
        )

        # Commit the execution to the database
        connection.commit()
        print("INSERT Successful --------------")
    except Exception as e:
        raise RuntimeError(f"Error while inserting user logs: str{e}")
    finally:
        if conn:
            cursor.close()


def get_user_logs(user_id: str):
    """
    Retrieves the top 10 most recent interactions of user_id extracts
    :param user_id: The ID of the user
    :return: A list of user_logs
    """
    connection = None
    cursor = None
    try:
        # Initialize connection and interaction point
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to retrieve the data
        query = """
            SELECT *
            FROM user_logs
            Where user_id = %s
            ORDER BY timestamp DESC
            LIMIT 10
        """

        # Execute the query
        user_id = str(user_id)
        cursor.execute(query, (user_id,))
        logs = cursor.fetchall()

        print("RETRIEVAL SUCCESSFUL---------------")
        return logs  # Return the logs
    except Exception as e:
        raise RuntimeError(f"Error while retrieving user logs: {str(e)}")
    finally:
        if connection:
            cursor.close()
