import pandas as pd
import db

def get_joined_view(filters=None) -> pd.DataFrame:
    filters = filters or {}
    where = []
    params = []

    if filters.get("scenario_id"):
        where.append("s.id = ?")
        params.append(int(filters["scenario_id"]))

    if filters.get("country"):
        where.append("s.country = ?")
        params.append(filters["country"])

    if filters.get("start_date"):
        where.append("s.date >= ?")
        params.append(filters["start_date"])

    if filters.get("end_date"):
        where.append("s.date <= ?")
        params.append(filters["end_date"])

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    c = db.conn()
    q = f"""
    SELECT
        s.id AS scenario_id,
        s.country, s.date, s.population,
        s.vaccination_rate, s.lockdown_level, s.mental_support_level, s.baseline_cases,
        m.covid_cases_est, m.hospital_admissions_est, m.mental_health_reports_est, m.risk_level
    FROM scenarios s
    LEFT JOIN inferred_metrics m ON m.scenario_id = s.id
    {where_sql}
    ORDER BY s.date ASC, s.id ASC;
    """
    df = pd.read_sql_query(q, c, params=params)
    c.close()
    return df

def summary_stats(df: pd.DataFrame, metric: str):
    if df.empty or metric not in df.columns:
        return {"count": 0, "mean": None, "min": None, "max": None}
    s = df[metric].dropna()
    if s.empty:
        return {"count": 0, "mean": None, "min": None, "max": None}
    return {
        "count": int(len(s)),
        "mean": float(s.mean()),
        "min": float(s.min()),
        "max": float(s.max()),
    }
