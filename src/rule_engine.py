from typing import Dict, Any

def infer_metrics(scenario: Dict[str, Any]) -> Dict[str, Any]:
    vr = float(scenario["vaccination_rate"])
    lockdown = int(scenario["lockdown_level"])
    support = int(scenario["mental_support_level"])
    baseline = int(scenario["baseline_cases"])
    pop = int(scenario["population"])

    # scale around 1,000,000 people's population
    pop_factor = max(0.5, min(2.0, pop / 1_000_000))

    # vaccination reduces spread of diseases
    v_factor = max(0.2, 1.0 - (vr / 120.0))

    # lockdown reduces spread of diseases at somewhat level
    l_factor = {0: 1.20, 1: 1.00, 2: 0.80, 3: 0.65}[max(0, min(3, lockdown))]

    covid_cases_est = baseline * v_factor * l_factor * pop_factor

    # admissions related to cases and vaccination
    admission_rate = max(0.01, 0.06 - (vr / 2500.0))
    hospital_admissions_est = covid_cases_est * admission_rate

    # mental health: lockdown increases, support reduces
    mh_base = 200 * pop_factor
    mh_lockdown_boost = lockdown * 0.35
    mh_support_reduction = support * 0.20
    mental_health_reports_est = mh_base * (1.0 + mh_lockdown_boost - mh_support_reduction)

    if covid_cases_est > 5000:
        risk = "HIGH"
    elif covid_cases_est > 2000:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "covid_cases_est": round(float(covid_cases_est), 2),
        "hospital_admissions_est": round(float(hospital_admissions_est), 2),
        "mental_health_reports_est": round(float(mental_health_reports_est), 2),
        "risk_level": risk
    }
