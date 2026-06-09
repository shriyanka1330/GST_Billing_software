import mysql.connector
from config.db_config import get_connection

def setup_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Groups Table (Account Groups)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS account_groups (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            parent_id INT NULL,
            FOREIGN KEY (parent_id) REFERENCES account_groups(id)
        )
        """)

        # 2. Ledgers Table (Individual Accounts)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ledgers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            group_id INT NOT NULL,
            opening_balance DECIMAL(15,2) DEFAULT 0.00,
            balance_type ENUM('Dr', 'Cr') DEFAULT 'Dr',
            gst_number VARCHAR(15) NULL,
            address TEXT NULL,
            FOREIGN KEY (group_id) REFERENCES account_groups(id)
        )
        """)

        # 3. Products Table (Inventory Master)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            product_code VARCHAR(20) NULL,
            price DECIMAL(15,2) DEFAULT 0.00,
            gst_rate INT DEFAULT 0,
            stock INT DEFAULT 0
        )
        """)

        # 4. Vouchers Table (Header)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vouchers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            voucher_no VARCHAR(50) UNIQUE NOT NULL,
            date DATE NOT NULL,
            voucher_type ENUM('Sales', 'Purchase', 'Payment', 'Receipt', 'Journal', 'Contra') NOT NULL,
            remarks TEXT NULL
        )
        """)

        # 5. Voucher Entries (Double Entry lines: Dr/Cr)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS voucher_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            voucher_id INT NOT NULL,
            ledger_id INT NOT NULL,
            amount DECIMAL(15,2) NOT NULL,
            entry_type ENUM('Dr', 'Cr') NOT NULL,
            FOREIGN KEY (voucher_id) REFERENCES vouchers(id),
            FOREIGN KEY (ledger_id) REFERENCES ledgers(id)
        )
        """)

        # 6. Inventory Entries (Linked to Vouchers)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            voucher_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            rate DECIMAL(15,2) NOT NULL,
            amount DECIMAL(15,2) NOT NULL,
            FOREIGN KEY (voucher_id) REFERENCES vouchers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """)

        # Insert Default Groups (Basic Tally Groups)
        default_groups = [
            ("Capital Account", None),
            ("Current Liabilities", None),
            ("Sundry Creditors", 2),
            ("Duties & Taxes", 2),
            ("Current Assets", None),
            ("Sundry Debtors", 5),
            ("Cash-in-Hand", 5),
            ("Bank Accounts", 5),
            ("Sales Accounts", None),
            ("Purchase Accounts", None),
            ("Direct Incomes", None),
            ("Direct Expenses", None),
            ("Indirect Incomes", None),
            ("Indirect Expenses", None)
        ]

        # Note: We skip inserting if groups already exist
        cursor.execute("SELECT COUNT(*) FROM account_groups")
        if cursor.fetchone()[0] == 0:
            for name, parent_id in default_groups:
                cursor.execute("INSERT INTO account_groups (name, parent_id) VALUES (%s, %s)", (name, parent_id))
        
        # Insert Default Ledgers (Cash, CGST, SGST, IGST)
        cursor.execute("SELECT COUNT(*) FROM ledgers")
        if cursor.fetchone()[0] == 0:
            # Assuming IDs for groups based on above inserts
            # Cash-in-Hand is group ID 7, Duties & Taxes is group ID 4
            cursor.execute("INSERT INTO ledgers (name, group_id, balance_type) VALUES ('Cash', 7, 'Dr')")
            cursor.execute("INSERT INTO ledgers (name, group_id, balance_type) VALUES ('CGST', 4, 'Cr')")
            cursor.execute("INSERT INTO ledgers (name, group_id, balance_type) VALUES ('SGST', 4, 'Cr')")
            cursor.execute("INSERT INTO ledgers (name, group_id, balance_type) VALUES ('IGST', 4, 'Cr')")

        conn.commit()
        print("Database schema successfully set up for Tally ERP!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
