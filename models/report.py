from config.db_config import get_connection

def get_ledger_statement(ledger_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get Ledger Details
    cursor.execute("SELECT name, opening_balance, balance_type FROM ledgers WHERE id = %s", (ledger_id,))
    ledger = cursor.fetchone()
    
    # Get Transactions
    query = """
        SELECT v.date, v.voucher_no, v.voucher_type, ve.entry_type, ve.amount, v.remarks
        FROM voucher_entries ve
        JOIN vouchers v ON ve.voucher_id = v.id
        WHERE ve.ledger_id = %s
        ORDER BY v.date, v.id
    """
    cursor.execute(query, (ledger_id,))
    transactions = cursor.fetchall()
    
    conn.close()
    return ledger, transactions
