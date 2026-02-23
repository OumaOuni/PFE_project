from backend.database import get_connection

def get_user_by_username(username):
    
    # Query PostgreSQL
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user