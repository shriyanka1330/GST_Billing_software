from config.db_config import get_connection

def add_ledger(name, group_id, opening_balance, balance_type, gst_number="", address=""):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO ledgers (name, group_id, opening_balance, balance_type, gst_number, address)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, group_id, opening_balance, balance_type, gst_number, address))
    conn.commit()
    conn.close()

def get_all_ledgers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.id, l.name, g.name as group_name, l.opening_balance, l.balance_type 
        FROM ledgers l
        JOIN account_groups g ON l.group_id = g.id
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_account_groups():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM account_groups ORDER BY name")
    data = cursor.fetchall()
    conn.close()
    return data
