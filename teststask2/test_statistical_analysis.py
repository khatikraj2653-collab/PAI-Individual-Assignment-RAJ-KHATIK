from src.statistical_analysis import compute_statistics

def test_confidence_and_lift_calculation():
    transactions = [
        {"milk", "bread"},
        {"milk", "bread"},
        {"milk", "butter"},
        {"bread"}
    ]

    results = compute_statistics(transactions, "milk")
    result_dict = {item: (conf, lift) for item, conf, lift in results}

    # Confidence = 2 / 3
    assert round(result_dict["bread"][0], 2) == round(2 / 3, 2)

    # Lift = 8 / 9 ≈ 0.89
    assert round(result_dict["bread"][1], 2) == round(8 / 9, 2)
