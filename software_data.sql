create database gst_billing_software;
use gst_billing_software;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);
select * from users;
INSERT INTO users (username, password)
VALUES ('admin', '1234');

CREATE TABLE account_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    parent_id INT NULL,
    FOREIGN KEY (parent_id) REFERENCES account_groups(id)
);

CREATE TABLE ledgers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    group_id INT NOT NULL,
    opening_balance DECIMAL(15,2) DEFAULT 0.00,
    balance_type ENUM('Dr', 'Cr') DEFAULT 'Dr',
    gst_number VARCHAR(15) NULL,
    address TEXT NULL,
    FOREIGN KEY (group_id) REFERENCES account_groups(id)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    hsn_code VARCHAR(20) NULL,
    price DECIMAL(15,2) DEFAULT 0.00,
    gst_rate INT DEFAULT 0,
    stock INT DEFAULT 0
);

CREATE TABLE vouchers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    voucher_no VARCHAR(50) UNIQUE NOT NULL,
    date DATE NOT NULL,
    voucher_type ENUM('Sales', 'Purchase', 'Payment', 'Receipt', 'Journal', 'Contra') NOT NULL,
    narration TEXT NULL
);

CREATE TABLE voucher_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    voucher_id INT NOT NULL,
    ledger_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    entry_type ENUM('Dr', 'Cr') NOT NULL,
    FOREIGN KEY (voucher_id) REFERENCES vouchers(id),
    FOREIGN KEY (ledger_id) REFERENCES ledgers(id)
);

CREATE TABLE inventory_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    voucher_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    rate DECIMAL(15,2) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    FOREIGN KEY (voucher_id) REFERENCES vouchers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);




