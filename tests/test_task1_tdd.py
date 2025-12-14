import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
import pandas as pd

import db
import services
import analytics


@pytest.fixture(scope="function")
def tmp_db(tmp_path):
    path = tmp_path / "test.db"
    db.set_db(str(path))
    if os.path.exists(db.DB_NAME):
        os.remove(db.DB_NAME)
    db.init_db()
    yield str(path)
    if os.path.exists(db.DB_NAME):
        os.remove(db.DB_NAME)


def test_create_and_read_scenario(tmp_db):
    sid = db.insert_scenario(
        country="UK",
        date="2024-01-01",
        population=1_000_000,
        vaccination_rate=75.0,
        lockdown_level=2,
        mental_support_level=3,
        baseline_cases=200
    )
    s = db.get_scenario(sid)
    assert s is not None
    assert s["country"] == "UK"
    assert s["vaccination_rate"] == 75.0


def test_run_inference_creates_metrics(tmp_db):
    sid = db.insert_scenario("US", "2024-01-01", 1_000_000, 20.0, 0, 0, 3000)
    mid = services.run_inference_and_store(sid)
    assert isinstance(mid, int)

    df = analytics.get_joined_view({"scenario_id": sid})
    assert len(df) == 1
    assert pd.notna(df.iloc[0]["covid_cases_est"])
    assert df.iloc[0]["risk_level"] in ("LOW", "MEDIUM", "HIGH")


def test_update_scenario_then_rerun_inference_updates_metrics(tmp_db):
    sid = db.insert_scenario("India", "2024-02-01", 1_000_000, 10.0, 0, 0, 3000)
    services.run_inference_and_store(sid)

    df_before = analytics.get_joined_view({"scenario_id": sid})
    cases_before = float(df_before.iloc[0]["covid_cases_est"])

    # Update scenario inputs
    db.update_scenario(sid, vaccination_rate=80.0, lockdown_level=3, mental_support_level=3, baseline_cases=800)
    services.run_inference_and_store(sid)  

    df_after = analytics.get_joined_view({"scenario_id": sid})
    cases_after = float(df_after.iloc[0]["covid_cases_est"])

    assert df_after.iloc[0]["vaccination_rate"] == 80.0
    assert cases_after != cases_before


def test_delete_scenario_cascades_metrics(tmp_db):
    sid = db.insert_scenario("Germany", "2024-03-01", 800_000, 60.0, 1, 2, 1500)
    services.run_inference_and_store(sid)

    db.delete_scenario(sid)
    df = analytics.get_joined_view({"scenario_id": sid})
    assert df.empty
