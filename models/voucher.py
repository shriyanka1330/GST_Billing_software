from config.db_config import get_connection
import uuid

def create_sales_voucher(date, customer_ledger_id, products_list, subtotal, cgst, sgst, igst, grand_total):
    """
    products_list: list of dicts with {'product_id': id, 'quantity': q, 'price': p, 'gst_rate': r, 'total': t}
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Create Voucher Header
        voucher_no = f"SAL-{str(uuid.uuid4())[:8].upper()}"
        cursor.execute("""
            INSERT INTO vouchers (voucher_no, date, voucher_type, remarks)
            VALUES (%s, %s, %s, %s)
        """, (voucher_no, date, 'Sales', f"Sales to Ledger {customer_ledger_id}"))
        voucher_id = cursor.lastrowid
        
        # 2. Inventory Entries
        for prod in products_list:
            cursor.execute("""
                INSERT INTO inventory_entries (voucher_id, product_id, quantity, rate, amount)
                VALUES (%s, %s, %s, %s, %s)
            """, (voucher_id, prod['product_id'], prod['quantity'], prod['price'], prod['total']))
            
            # Decrease Stock
            cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (prod['quantity'], prod['product_id']))
        
        # 3. Double Entry Accounting (Voucher Entries)
        
        # a. DEBIT the Customer Ledger
        cursor.execute("""
            INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type)
            VALUES (%s, %s, %s, 'Dr')
        """, (voucher_id, customer_ledger_id, grand_total))
        
        # b. CREDIT Sales Account (We need a Sales ledger ID, but for now we find it dynamically or assume a group)
        # Let's find or create a Sales Ledger
        cursor.execute("SELECT id FROM ledgers WHERE name = 'Sales A/c'")
        sales_ledger = cursor.fetchone()
        if not sales_ledger:
            # Sales account group is 9
            cursor.execute("INSERT INTO ledgers (name, group_id, balance_type) VALUES ('Sales A/c', 9, 'Cr')")
            sales_ledger_id = cursor.lastrowid
        else:
            sales_ledger_id = sales_ledger[0]
            
        cursor.execute("""
            INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type)
            VALUES (%s, %s, %s, 'Cr')
        """, (voucher_id, sales_ledger_id, subtotal))
        
        # c. CREDIT Tax Ledgers
        if cgst > 0:
            cursor.execute("SELECT id FROM ledgers WHERE name = 'CGST'")
            cgst_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type) VALUES (%s, %s, %s, 'Cr')", (voucher_id, cgst_id, cgst))
            
        if sgst > 0:
            cursor.execute("SELECT id FROM ledgers WHERE name = 'SGST'")
            sgst_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type) VALUES (%s, %s, %s, 'Cr')", (voucher_id, sgst_id, sgst))

        if igst > 0:
            cursor.execute("SELECT id FROM ledgers WHERE name = 'IGST'")
            igst_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type) VALUES (%s, %s, %s, 'Cr')", (voucher_id, igst_id, igst))

        conn.commit()
        return voucher_no
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def create_purchase_voucher(date, supplier_ledger_id, products_list, subtotal, cgst, sgst, igst, grand_total):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Create Voucher Header
        voucher_no = f"PUR-{str(uuid.uuid4())[:8].upper()}"
        cursor.execute("""
            INSERT INTO vouchers (voucher_no, date, voucher_type, remarks)
            VALUES (%s, %s, %s, %s)
        """, (voucher_no, date, 'Purchase', f"Purchase from Ledger {supplier_ledger_id}"))
        voucher_id = cursor.lastrowid
        
        # 2. Inventory Entries
        for prod in products_list:
            cursor.execute("""
                INSERT INTO inventory_entries (voucher_id, product_id, quantity, rate, amount)
                VALUES (%s, %s, %s, %s, %s)
            """, (voucher_id, prod['product_id'], prod['quantity'], prod['price'], prod['total']))
            
            # Increase Stock
            cursor.execute("UPDATE products SET stock = stock + %s WHERE id = %s", (prod['quantity'], prod['product_id']))
        
        # 3. Double Entry Accounting (Voucher Entries)
        
        # a. CREDIT the Supplier Ledger
        cursor.execute("""
            INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type)
            VALUES (%s, %s, %s, 'Cr')
        """, (voucher_id, supplier_ledger_id, grand_total))
        
        # b. DEBIT Purchase Account
        cursor.execute("SELECT id FROM ledgers WHERE name = 'Purchase A/c'")
        purchase_ledger = cursor.fetchone()
        if not purchase_ledger:
            # Purchase account group is 10
            cursor.execute("INSERT INTO ledgers (name, group_id, balance_type) VALUES ('Purchase A/c', 10, 'Dr')")
            purchase_ledger_id = cursor.lastrowid
        else:
            purchase_ledger_id = purchase_ledger[0]
            
        cursor.execute("""
            INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type)
            VALUES (%s, %s, %s, 'Dr')
        """, (voucher_id, purchase_ledger_id, subtotal))
        
        # c. DEBIT Tax Ledgers
        if cgst > 0:
            cursor.execute("SELECT id FROM ledgers WHERE name = 'CGST'")
            cgst_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type) VALUES (%s, %s, %s, 'Dr')", (voucher_id, cgst_id, cgst))
            
        if sgst > 0:
            cursor.execute("SELECT id FROM ledgers WHERE name = 'SGST'")
            sgst_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type) VALUES (%s, %s, %s, 'Dr')", (voucher_id, sgst_id, sgst))

        if igst > 0:
            cursor.execute("SELECT id FROM ledgers WHERE name = 'IGST'")
            igst_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type) VALUES (%s, %s, %s, 'Dr')", (voucher_id, igst_id, igst))

        conn.commit()
        return voucher_no
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def create_payment_receipt_voucher(date, vch_type, dr_ledger_id, cr_ledger_id, amount, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        prefix = "PAY" if vch_type == "Payment" else "REC"
        voucher_no = f"{prefix}-{str(uuid.uuid4())[:8].upper()}"
        
        cursor.execute("""
            INSERT INTO vouchers (voucher_no, date, voucher_type, remarks)
            VALUES (%s, %s, %s, %s)
        """, (voucher_no, date, vch_type, remarks))
        voucher_id = cursor.lastrowid
        
        # DEBIT Entry
        cursor.execute("""
            INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type)
            VALUES (%s, %s, %s, 'Dr')
        """, (voucher_id, dr_ledger_id, amount))
        
        # CREDIT Entry
        cursor.execute("""
            INSERT INTO voucher_entries (voucher_id, ledger_id, amount, entry_type)
            VALUES (%s, %s, %s, 'Cr')
        """, (voucher_id, cr_ledger_id, amount))

        conn.commit()
        return voucher_no
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
