import os
import logging
import db
import rule_engine

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/app.log", level=logging.INFO)

def run_inference_and_store(scenario_id: int) -> int:
    scenario = db.get_scenario(scenario_id)
    if not scenario:
        raise ValueError(f"Scenario {scenario_id} not found.")

    metrics = rule_engine.infer_metrics(scenario)

    mid = db.upsert_metrics(
        scenario_id=scenario_id,
        covid_cases_est=metrics["covid_cases_est"],
        hospital_admissions_est=metrics["hospital_admissions_est"],
        mental_health_reports_est=metrics["mental_health_reports_est"],
        risk_level=metrics["risk_level"],
    )

    logging.info(f"Ran inference for scenario_id={scenario_id} metrics_id={mid}")
    return mid
