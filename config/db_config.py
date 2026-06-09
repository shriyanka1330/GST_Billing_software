import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shriyanka123",   # change
        database="gst_billing_software"
    )