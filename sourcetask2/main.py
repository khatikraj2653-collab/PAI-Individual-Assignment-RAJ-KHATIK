import sys
from pathlib import Path

# Ensure project root is on Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))





from src.transaction_loader import load_transactions
from src.statistical_analysis import compute_statistics

def main():
    transactions = load_transactions("Supermarket_dataset_PAI.csv")
    target_item = "whole milk"

    results = compute_statistics(transactions, target_item)

    print("\n=== CONFIDENCE & LIFT ANALYSIS ===")
    print(f"Target Item: {target_item}\n")

    for item, conf, lift in sorted(results, key=lambda x: x[1], reverse=True)[:10]:
        print(f"{item:25} | confidence={conf:.3f} | lift={lift:.3f}")

if __name__ == "__main__":
    main()
