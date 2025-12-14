import sqlite3
from typing import Optional, Dict, Any

DB_NAME = "public_health_inference.db"

def set_db(path: str):
    global DB_NAME
    DB_NAME = path

def conn():
    c = sqlite3.connect(DB_NAME)
    c.execute("PRAGMA foreign_keys = ON;")
    return c

def init_db():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scenarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT NOT NULL,
        date TEXT NOT NULL,
        population INTEGER NOT NULL,
        vaccination_rate REAL NOT NULL,
        lockdown_level INTEGER NOT NULL,
        mental_support_level INTEGER NOT NULL,
        baseline_cases INTEGER NOT NULL
    );
    """)

    # One metrics row scenario_id references one scenario
    cur.execute("""
    CREATE TABLE IF NOT EXISTS inferred_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scenario_id INTEGER NOT NULL UNIQUE,
        covid_cases_est REAL NOT NULL,
        hospital_admissions_est REAL NOT NULL,
        mental_health_reports_est REAL NOT NULL,
        risk_level TEXT NOT NULL,
        FOREIGN KEY (scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
    );
    """)

    c.commit()
    c.close()

def insert_scenario(country: str, date: str, population: int, vaccination_rate: float,
                    lockdown_level: int, mental_support_level: int, baseline_cases: int) -> int:
    c = conn()
    cur = c.cursor()
    cur.execute("""
        INSERT INTO scenarios(country, date, population, vaccination_rate, lockdown_level, mental_support_level, baseline_cases)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (country, date, population, vaccination_rate, lockdown_level, mental_support_level, baseline_cases))
    c.commit()
    sid = int(cur.lastrowid)
    c.close()
    return sid

def list_scenarios() -> list[dict]:
    c = conn()
    cur = c.cursor()
    cur.execute("""
        SELECT id, country, date, population, vaccination_rate, lockdown_level, mental_support_level, baseline_cases
        FROM scenarios ORDER BY id ASC
    """)
    rows = cur.fetchall()
    c.close()
    return [
        {
            "scenario_id": r[0], "country": r[1], "date": r[2], "population": r[3],
            "vaccination_rate": r[4], "lockdown_level": r[5],
            "mental_support_level": r[6], "baseline_cases": r[7]
        }
        for r in rows
    ]

def get_scenario(scenario_id: int) -> Optional[Dict[str, Any]]:
    c = conn()
    cur = c.cursor()
    cur.execute("""
        SELECT id, country, date, population, vaccination_rate, lockdown_level, mental_support_level, baseline_cases
        FROM scenarios WHERE id=?
    """, (scenario_id,))
    r = cur.fetchone()
    c.close()
    if not r:
        return None
    return {
        "scenario_id": r[0],
        "country": r[1],
        "date": r[2],
        "population": r[3],
        "vaccination_rate": r[4],
        "lockdown_level": r[5],
        "mental_support_level": r[6],
        "baseline_cases": r[7],
    }

def update_scenario(scenario_id: int, **fields):
    allowed = {"country","date","population","vaccination_rate","lockdown_level","mental_support_level","baseline_cases"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return
    set_clause = ", ".join([f"{k}=?" for k in updates.keys()])
    params = list(updates.values()) + [scenario_id]
    c = conn()
    cur = c.cursor()
    cur.execute(f"UPDATE scenarios SET {set_clause} WHERE id=?", params)
    c.commit()
    c.close()

def delete_scenario(scenario_id: int):
    c = conn()
    cur = c.cursor()
    cur.execute("DELETE FROM scenarios WHERE id=?", (scenario_id,))
    c.commit()
    c.close()

def upsert_metrics(scenario_id: int, covid_cases_est: float, hospital_admissions_est: float,
                   mental_health_reports_est: float, risk_level: str) -> int:
    c = conn()
    cur = c.cursor()
    cur.execute("""
        INSERT INTO inferred_metrics(scenario_id, covid_cases_est, hospital_admissions_est, mental_health_reports_est, risk_level)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(scenario_id) DO UPDATE SET
            covid_cases_est=excluded.covid_cases_est,
            hospital_admissions_est=excluded.hospital_admissions_est,
            mental_health_reports_est=excluded.mental_health_reports_est,
            risk_level=excluded.risk_level
    """, (scenario_id, covid_cases_est, hospital_admissions_est, mental_health_reports_est, risk_level))
    c.commit()
    cur.execute("SELECT id FROM inferred_metrics WHERE scenario_id=?", (scenario_id,))
    mid = int(cur.fetchone()[0])
    c.close()
    return mid
