import json
from app.db.connection import get_db_connection


def save_user_log(user_id, agent, request, response, timestamp=None):
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
                json.dumps(request),
                json.dumps(response),
                timestamp,
            ),
        )

        connection.commit()
    except Exception as e:
        raise RuntimeError(f"Error while inserting user logs: str{e}")
    finally:
        if conn:
            cursor.close()
