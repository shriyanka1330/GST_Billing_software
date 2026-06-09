from config.db_config import get_connection

def add_product(name, product_code, price, gst_rate, stock):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO products (name, product_code, price, gst_rate, stock)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, product_code, price, gst_rate, stock))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, product_code, price, gst_rate, stock FROM products")
    data = cursor.fetchall()
    conn.close()
    return data
