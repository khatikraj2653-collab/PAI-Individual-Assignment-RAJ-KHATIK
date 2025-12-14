import streamlit as st
import pandas as pd

import db
import services
import analytics
from utils import export_to_csv

db.init_db()
st.set_page_config(page_title="Public Health Inference Dashboard", layout="wide")
st.title("🧠 Rule-Based Public Health Inference Dashboard")

# Load scenarios for dropdown
scenarios = db.list_scenarios()
scenario_ids = [s["scenario_id"] for s in scenarios]

with st.sidebar:
    st.header("Create Scenario")
    new_country = st.text_input("Country", value="UK")
    new_date = st.text_input("Date (YYYY-MM-DD)", value="2024-01-01")
    new_population = st.number_input("Population", min_value=1000, value=1_000_000, step=1000)
    new_vr = st.slider("Vaccination rate (0-100)", 0.0, 100.0, 70.0, 0.5)
    new_lock = st.selectbox("Lockdown level (0-3)", [0, 1, 2, 3], index=1)
    new_ms = st.selectbox("Mental support level (0-3)", [0, 1, 2, 3], index=2)
    new_base = st.number_input("Baseline cases", min_value=0, value=1000, step=50)

    if st.button("Save Scenario"):
        sid = db.insert_scenario(new_country, new_date, int(new_population), float(new_vr), int(new_lock), int(new_ms), int(new_base))
        st.success(f"Saved scenario id={sid}. Refresh to see it in dropdown.")

    st.divider()
    st.header("Edit / Delete Scenario")

    if scenario_ids:
        selected_id = st.selectbox("Select Scenario ID", scenario_ids)
        current = db.get_scenario(int(selected_id))

        edit_country = st.text_input("Edit Country", value=current["country"])
        edit_date = st.text_input("Edit Date (YYYY-MM-DD)", value=current["date"])
        edit_population = st.number_input("Edit Population", min_value=1000, value=int(current["population"]), step=1000)
        edit_vr = st.slider("Edit Vaccination rate", 0.0, 100.0, float(current["vaccination_rate"]), 0.5)
        edit_lock = st.selectbox("Edit Lockdown level", [0, 1, 2, 3], index=int(current["lockdown_level"]))
        edit_ms = st.selectbox("Edit Mental support level", [0, 1, 2, 3], index=int(current["mental_support_level"]))
        edit_base = st.number_input("Edit Baseline cases", min_value=0, value=int(current["baseline_cases"]), step=50)

        colA, colB = st.columns(2)

        with colA:
            if st.button("Update Scenario"):
                db.update_scenario(
                    int(selected_id),
                    country=edit_country,
                    date=edit_date,
                    population=int(edit_population),
                    vaccination_rate=float(edit_vr),
                    lockdown_level=int(edit_lock),
                    mental_support_level=int(edit_ms),
                    baseline_cases=int(edit_base),
                )
                st.success("Scenario updated. Now run inference to refresh metrics.")

        with colB:
            if st.button("Delete Scenario"):
                db.delete_scenario(int(selected_id))
                st.warning("Scenario deleted. Refresh the page to update dropdown/table.")

        st.divider()
        st.header("Run Inference")
        if st.button("Run Inference for Selected Scenario"):
            try:
                services.run_inference_and_store(int(selected_id))
                st.success("Inference updated metrics (saved to DB).")
            except Exception as e:
                st.error(str(e))
    else:
        st.info("No scenarios yet. Create one first.")

# Main data view
st.subheader("Stored Scenarios + Inferred Metrics")
df = analytics.get_joined_view()
st.dataframe(df, use_container_width=True)

st.subheader("Summary Statistics")
metric = st.selectbox("Metric", ["covid_cases_est", "hospital_admissions_est", "mental_health_reports_est"])
stats = analytics.summary_stats(df, metric)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Count", stats["count"])
c2.metric("Mean", "-" if stats["mean"] is None else round(stats["mean"], 2))
c3.metric("Min", "-" if stats["min"] is None else round(stats["min"], 2))
c4.metric("Max", "-" if stats["max"] is None else round(stats["max"], 2))

st.subheader("Trend Chart")
plot_df = df.dropna(subset=[metric]).copy()
plot_df["date"] = pd.to_datetime(plot_df["date"], errors="coerce")
plot_df = plot_df.dropna(subset=["date"]).sort_values("date")
if plot_df.empty:
    st.info("No inferred data to plot yet. Run inference on at least one scenario.")
else:
    st.line_chart(plot_df, x="date", y=metric, use_container_width=True)

st.subheader("Export")
export_path = st.text_input("Export path", value="data/exports/inference_export.csv")
if st.button("Export CSV"):
    export_to_csv(df, export_path)
    st.success(f"Exported to {export_path}")
