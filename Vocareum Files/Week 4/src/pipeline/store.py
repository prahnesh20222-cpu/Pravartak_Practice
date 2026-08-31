import sqlite3
import time
from pathlib import Path
from typing import Iterable

#from .pipeline import Answer
from .models import Answer

from .settings import RunSummary
import json

# ---------- SCHEMA ----------
SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at REAL NOT NULL,
    elapsed_seconds REAL NOT NULL,
    n_questions INTEGER NOT NULL,
    n_succeeded INTEGER NOT NULL,
    n_retries_total INTEGER NOT NULL,
    total_cost_usd REAL NOT NULL,
    fail_rate REAL NOT NULL,
    use_fake INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    question TEXT NOT NULL,
    content TEXT NOT NULL,
    cost_usd REAL NOT NULL,
    retries INTEGER DEFAULT 0,
    model TEXT NOT NULL,
    confidence REAL NOT NULL,
    sources TEXT,
    schema_version TEXT NOT NULL,
    ts REAL NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs (id)
);
"""

# ---------- DATABASE INTERACTION ----------

def connect(path: str | Path = "results.db") -> sqlite3.Connection:
    """Open a SQLite connection, run the schema script, and return the connection."""
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    con.commit()
    return con


def write_run(con: sqlite3.Connection, summary: RunSummary) -> int:
    """Insert a RunSummary record into the runs table and return the new run's ID."""
    query = """
    INSERT INTO runs (
        started_at,
        elapsed_seconds,
        n_questions,
        n_succeeded,
        n_retries_total,
        total_cost_usd,
        fail_rate,
        use_fake
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        summary.started_at,
        summary.elapsed_seconds,
        summary.n_questions,
        summary.n_succeeded,
        summary.n_retries_total,
        summary.total_cost_usd,
        summary.fail_rate,
        1 if summary.use_fake else 0,
    )
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    return cur.lastrowid  # Returns the autoincremented PK for the new run


def write_answers(
    con: sqlite3.Connection, run_id: int, answers: Iterable[Answer]
) -> int:
    """Batch-insert answer records linked to run_id into the answers table."""
    now = time.time()
    rows = [
        (
            run_id,
            a.question,
            a.content,
            a.cost_usd,
            a.retries,
            now,
        )
        for a in answers
    ]
    
    query = """
    INSERT INTO answers (
        run_id,
        question,
        answer,
        cost_usd,
        retries,
        ts
    ) VALUES (?, ?, ?, ?, ?, ?)
    """
    con.executemany(query, rows)
    con.commit()
    return len(rows)

def save_answer(
    con: sqlite3.Connection,
    *,
    question: str,
    content: str,
    retries: int,
    cost_usd: float,
    model: str,
    confidence: float,
    sources: list[str],
    schema_version: str,
) -> int:
    """Save one W4 answer and return its database ID."""

    query = """
    INSERT INTO answers (
        question,
        content,
        retries,
        cost_usd,
        model,
        confidence,
        sources,
        schema_version,
        ts
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = (
        question,
        content,
        retries,
        cost_usd,
        model,
        confidence,
        json.dumps(sources),
        schema_version,
        time.time(),
    )

    cur = con.execute(query, params)
    con.commit()
    return cur.lastrowid