from config.db_config import get_connection

def check_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    conn.close()

    return result