import sqlite3
from pathlib import Path

DB_PATH = Path("data/trades.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            open_date TEXT NOT NULL,
            close_date TEXT,
            pair TEXT NOT NULL,
            direction TEXT NOT NULL,
            narrative TEXT NOT NULL,
            setup_type TEXT NOT NULL,
            result_r REAL NOT NULL,
            notes TEXT,
            reflection TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_all_trades():
    conn = get_connection()
    trades = conn.execute("SELECT * FROM trades ORDER BY open_date DESC, id DESC").fetchall()
    conn.close()
    return trades


def add_trade(open_date, close_date, pair, direction, narrative, setup_type, result_r, notes, reflection):
    conn = get_connection()
    conn.execute("""
        INSERT INTO trades (
            open_date, close_date, pair, direction, narrative,
            setup_type, result_r, notes, reflection
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (open_date, close_date, pair, direction, narrative, setup_type, result_r, notes, reflection))
    conn.commit()
    conn.close()


def delete_trade(trade_id):
    conn = get_connection()
    conn.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
    conn.commit()
    conn.close()