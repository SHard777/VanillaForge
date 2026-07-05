import sqlite3
import os
from contextlib import contextmanager
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("VanillaForgeMemory")

# Define the local database path in the project root
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'vanillaforge_memory.db')

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Table 1: Sentiment History
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentiment_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ticker TEXT NOT NULL,
                score INTEGER NOT NULL,
                theme TEXT
            )
        ''')
        
        # Table 2: Trade Journal
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ticker TEXT NOT NULL,
                strategy TEXT NOT NULL,
                bsm_price REAL NOT NULL,
                volatility REAL,
                agent_notes TEXT
            )
        ''')
        
        # Ensure volatility column exists for existing databases
        cursor.execute("PRAGMA table_info(trade_journal)")
        columns = [info['name'] for info in cursor.fetchall()]
        if 'volatility' not in columns:
            cursor.execute("ALTER TABLE trade_journal ADD COLUMN volatility REAL")

# --- MCP Tools ---

@mcp.tool()
def log_sentiment(ticker: str, score: int, theme: str) -> str:
    """Logs the sentiment score for a given ticker to the local database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sentiment_history (ticker, score, theme) VALUES (?, ?, ?)', (ticker.upper(), score, theme))
    return f"Successfully logged sentiment for {ticker.upper()}: Score {score}, Theme '{theme}'"

@mcp.tool()
def get_sentiment_trend(ticker: str) -> List[Dict[str, Any]]:
    """Retrieves the sentiment history for a given ticker (last 30 entries)."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT timestamp, score, theme FROM sentiment_history WHERE ticker = ? ORDER BY timestamp DESC LIMIT 30', (ticker.upper(),))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@mcp.tool()
def log_paper_trade(ticker: str, strategy: str, bsm_price: float, volatility: float, agent_notes: str) -> str:
    """Logs a hypothetical paper trade into the trade journal."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO trade_journal (ticker, strategy, bsm_price, volatility, agent_notes) VALUES (?, ?, ?, ?, ?)', 
                       (ticker.upper(), strategy, bsm_price, volatility, agent_notes))
    return f"Successfully logged paper trade for {ticker.upper()} using strategy '{strategy}' at theoretical price {bsm_price} (IV: {volatility})."

@mcp.tool()
def view_trade_journal() -> List[Dict[str, Any]]:
    """Retrieves all trades currently logged in the paper trade journal."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, timestamp, ticker, strategy, bsm_price, volatility, agent_notes FROM trade_journal ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

# Initialize the database schema when the module loads
init_db()

if __name__ == "__main__":
    mcp.run()
