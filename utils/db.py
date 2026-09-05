"""
Lightweight SQLite layer for A-Day registrations and scores.

NOTE on hosting: Streamlit Community Cloud's filesystem is ephemeral —
the aday.db file survives while the app is awake but can reset on a
redeploy or a long sleep. That's fine for running a single-day fest.
If you need the data to survive across redeploys, see the "Optional:
persistent storage with Google Sheets" section in README.md.
"""

import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).resolve().parent.parent / "aday.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT UNIQUE NOT NULL,
                members TEXT NOT NULL,
                contact TEXT,
                department TEXT,
                registered_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                case_name TEXT NOT NULL,
                points REAL NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
                UNIQUE(team_id, case_name)
            )
        """)


# ---------------------------------------------------------------- teams ----
def add_team(team_name: str, members: str, contact: str = "", department: str = "") -> tuple[bool, str]:
    team_name = team_name.strip()
    if not team_name:
        return False, "Team name is required."
    if not members.strip():
        return False, "At least one member name is required."
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO teams (team_name, members, contact, department, registered_at) VALUES (?, ?, ?, ?, ?)",
                (team_name, members.strip(), contact.strip(), department.strip(), datetime.now().isoformat(timespec="seconds")),
            )
        return True, f"'{team_name}' is registered!"
    except sqlite3.IntegrityError:
        return False, f"A team called '{team_name}' is already registered."


def get_teams() -> pd.DataFrame:
    with get_conn() as conn:
        return pd.read_sql_query("SELECT * FROM teams ORDER BY registered_at DESC", conn)


def team_count() -> int:
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM teams").fetchone()[0]


def delete_team(team_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM teams WHERE id = ?", (team_id,))


# --------------------------------------------------------------- scores ----
def upsert_score(team_id: int, case_name: str, points: float):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO scores (team_id, case_name, points, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(team_id, case_name)
            DO UPDATE SET points = excluded.points, updated_at = excluded.updated_at
        """, (team_id, case_name, points, datetime.now().isoformat(timespec="seconds")))


def get_scores_raw() -> pd.DataFrame:
    with get_conn() as conn:
        return pd.read_sql_query("""
            SELECT t.team_name, s.case_name, s.points, s.updated_at
            FROM scores s JOIN teams t ON t.id = s.team_id
            ORDER BY s.updated_at DESC
        """, conn)


def get_leaderboard() -> pd.DataFrame:
    """Total points per team, ranked highest first."""
    with get_conn() as conn:
        teams = pd.read_sql_query("SELECT id, team_name FROM teams", conn)
        scores = pd.read_sql_query("SELECT team_id, case_name, points FROM scores", conn)
    if teams.empty:
        return pd.DataFrame(columns=["Rank", "Team", "Total Points"])
    totals = scores.groupby("team_id")["points"].sum().rename("Total Points") if not scores.empty else pd.Series(dtype=float)
    board = teams.set_index("id").join(totals).fillna({"Total Points": 0.0})
    board = board.sort_values("Total Points", ascending=False).reset_index(drop=True)
    board.insert(0, "Rank", board.index + 1)
    board = board.rename(columns={"team_name": "Team"})
    return board[["Rank", "Team", "Total Points"]]


def get_breakdown() -> pd.DataFrame:
    """Pivot table: teams x cases, with total points per case."""
    with get_conn() as conn:
        teams = pd.read_sql_query("SELECT id, team_name FROM teams", conn)
        scores = pd.read_sql_query("SELECT team_id, case_name, points FROM scores", conn)
    if teams.empty:
        return pd.DataFrame()
    merged = teams.merge(scores, left_on="id", right_on="team_id", how="left")
    pivot = merged.pivot_table(index="team_name", columns="case_name", values="points", fill_value=0, aggfunc="sum")
    pivot["Total"] = pivot.sum(axis=1)
    pivot = pivot.sort_values("Total", ascending=False)
    return pivot
