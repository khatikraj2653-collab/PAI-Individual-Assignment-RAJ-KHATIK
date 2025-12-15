from src.transaction_loader import load_transactions
from pathlib import Path

def test_load_transactions():
    csv_path = Path(__file__).parent.parent / "Supermarket_dataset_PAI.csv"
    transactions = load_transactions(csv_path)

    assert isinstance(transactions, list)
    assert len(transactions) > 0
    assert isinstance(transactions[0], set)
