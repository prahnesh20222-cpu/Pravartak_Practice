"""CLI query tool for pipeline run results and answer logs.

Usage Examples:
    1. List all recent pipeline runs:
       python -m src.pipeline.query_results --runs

    2. View all answers across all runs:
       python -m src.pipeline.query_results

    3. Search/filter answers by a question substring pattern:
       python -m src.pipeline.query_results rag
"""

import sqlite3
import sys


def show_runs(con: sqlite3.Connection) -> None:
    """Print a fixed-width formatted table listing all executed pipeline runs."""
    query = """
    SELECT id, started_at, n_questions, n_retries_total, total_cost_usd, fail_rate, use_fake
    FROM runs
    ORDER BY id DESC
    """
    rows = con.execute(query).fetchall()

    # Fixed-width header definition
    header = f"{'id':>4}  {'started':>12}  {'questions':>9}  {'retries':>7}  {'cost_usd':>8}  {'fail':>5}  {'fake':>4}"
    print(header)
    print("-" * len(header))

    for row in rows:
        run_id, started_at, n_questions, n_retries, total_cost, fail_rate, use_fake = row
        print(
            f"{run_id:>4}  "
            f"{started_at:>12.1f}  "
            f"{n_questions:>9}  "
            f"{n_retries:>7}  "
            f"{total_cost:>8.4f}  "
            f"{fail_rate:>5.2f}  "
            f"{use_fake:>4}"
        )


def search_answers(con: sqlite3.Connection, pattern: str) -> None:
    """Search answers table for questions matching a substring pattern."""
    query = """
    SELECT id, run_id, retries, question, answer
    FROM answers
    WHERE question LIKE ?
    ORDER BY id
    """
    # Parameterised query prevents SQL injection
    bound_param = (f"%{pattern}%",)
    rows = con.execute(query, bound_param).fetchall()

    for row in rows:
        ans_id, run_id, retries, question, answer = row
        print(f"[#{ans_id} run={run_id} retries={retries}] {question} → {answer[:140]}")


def main() -> None:
    """Connect to results.db and dispatch CLI commands."""
    con = sqlite3.connect("results.db")

    try:
        # Determine CLI action based on arguments
        if len(sys.argv) > 1 and sys.argv[1] == "--runs":
            show_runs(con)
        else:
            pattern = sys.argv[1] if len(sys.argv) > 1 else ""
            search_answers(con, pattern)
    finally:
        con.close()


if __name__ == "__main__":
    main()