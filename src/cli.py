import db
import services
import analytics
from utils import export_to_csv

def run_cli():
    db.init_db()
    while True:
        print("\n=== Public Health Inference Tool ===")
        print("1) Create scenario")
        print("2) Update scenario")
        print("3) Delete scenario")
        print("4) Run inference")
        print("5) View data")
        print("6) Export CSV")
        print("0) Exit")

        ch = input("Choice: ").strip()

        if ch == "1":
            country = input("Country: ")
            date = input("Date (YYYY-MM-DD): ")
            population = int(input("Population: "))
            vr = float(input("Vaccination rate (0-100): "))
            lock = int(input("Lockdown level (0-3): "))
            ms = int(input("Mental support level (0-3): "))
            base = int(input("Baseline cases: "))
            sid = db.insert_scenario(country, date, population, vr, lock, ms, base)
            print(f"Created scenario id={sid}")

        elif ch == "2":
            sid = int(input("Scenario ID to update: "))
            vr = float(input("New vaccination rate: "))
            lock = int(input("New lockdown level: "))
            ms = int(input("New mental support level: "))
            base = int(input("New baseline cases: "))
            db.update_scenario(sid, vaccination_rate=vr, lockdown_level=lock, mental_support_level=ms, baseline_cases=base)
            print("Updated. (Run inference again to refresh metrics.)")

        elif ch == "3":
            sid = int(input("Scenario ID to delete: "))
            db.delete_scenario(sid)
            print("Deleted.")

        elif ch == "4":
            sid = int(input("Scenario ID to infer: "))
            mid = services.run_inference_and_store(sid)
            print(f"Inference updated metrics id={mid}")

        elif ch == "5":
            df = analytics.get_joined_view()
            print(df.to_string(index=False))

        elif ch == "6":
            path = input("Export path (e.g. data/exports/out.csv): ")
            df = analytics.get_joined_view()
            export_to_csv(df, path)
            print("Exported.")

        elif ch == "0":
            break

        else:
            print("Invalid.")
