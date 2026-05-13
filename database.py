import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "customers.db"))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            need TEXT,
            budget TEXT,
            timeline TEXT,
            notes TEXT,
            intent_level TEXT,
            intent_reason TEXT,
            ai_analysis TEXT,
            email_draft TEXT,
            follow_up_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Migration for existing databases
    try:
        conn.execute("ALTER TABLE customers ADD COLUMN intent_reason TEXT")
    except Exception:
        pass
    conn.commit()
    conn.close()


def insert_customer(name, email, company, need, budget, timeline, notes,
                    intent_level="", ai_analysis="", email_draft="",
                    follow_up_date=""):
    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO customers (name, email, company, need, budget, timeline,
                               notes, intent_level, ai_analysis, email_draft,
                               follow_up_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, email, company, need, budget, timeline, notes,
          intent_level, ai_analysis, email_draft, follow_up_date))
    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return customer_id


def get_customer(customer_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM customers WHERE id = ?",
                       (customer_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_customers(intent_filter=None):
    conn = get_connection()
    if intent_filter and intent_filter in ("High", "Medium", "Low"):
        rows = conn.execute(
            "SELECT * FROM customers WHERE intent_level = ? ORDER BY created_at DESC",
            (intent_filter,)).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM customers ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_stats():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    high = conn.execute(
        "SELECT COUNT(*) FROM customers WHERE intent_level = 'High'").fetchone()[0]
    medium = conn.execute(
        "SELECT COUNT(*) FROM customers WHERE intent_level = 'Medium'").fetchone()[0]
    low = conn.execute(
        "SELECT COUNT(*) FROM customers WHERE intent_level = 'Low'").fetchone()[0]
    conn.close()
    return {"total": total, "high": high, "medium": medium, "low": low}


def update_customer(customer_id, **kwargs):
    if not kwargs:
        return
    fields = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [customer_id]
    conn = get_connection()
    conn.execute(f"UPDATE customers SET {fields} WHERE id = ?", values)
    conn.commit()
    conn.close()


def delete_customer(customer_id):
    conn = get_connection()
    conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
