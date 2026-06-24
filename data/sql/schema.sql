DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    region TEXT,
    employment_status TEXT,
    income REAL,
    customer_since DATE,
    credit_score INTEGER
);

CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    account_type TEXT,
    open_date DATE,
    interest_rate REAL,
    credit_limit REAL,
    current_balance REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    transaction_date DATE,
    amount REAL,
    transaction_type TEXT,
    merchant_category TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE payments (
    account_id INTEGER,
    due_date DATE,
    payment_date DATE,
    amount_due REAL,
    amount_paid REAL,
    days_late INTEGER,
    default_flag INTEGER,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
	