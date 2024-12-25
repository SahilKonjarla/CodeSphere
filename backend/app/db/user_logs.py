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
        serialized_response = json.dumps(ensure_json_serializable(response))
        serialized_request = json.dumps(ensure_json_serializable(request))
        connection = get_db_connection()
        cursor = connection.cursor()

        query = f"""
            INSERT INTO user_logs (user_id, agent, request, response, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """

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

        connection.commit()
        print("INSERT Successful --------------")
    except Exception as e:
        raise RuntimeError(f"Error while inserting user logs: str{e}")
    finally:
        if conn:
            cursor.close()
