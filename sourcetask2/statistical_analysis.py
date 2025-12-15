from collections import Counter
from itertools import combinations

def compute_statistics(transactions, target_item):
    total = len(transactions)
    item_counts = Counter()
    pair_counts = Counter()

    for t in transactions:
        for item in t:
            item_counts[item] += 1
        for a, b in combinations(sorted(t), 2):
            pair_counts[(a, b)] += 1

    results = []

    for (a, b), pair_count in pair_counts.items():
        if target_item not in (a, b):
            continue

        other = b if a == target_item else a

        support_target = item_counts[target_item] / total
        support_other = item_counts[other] / total
        support_pair = pair_count / total

        confidence = support_pair / support_target
        lift = confidence / support_other

        results.append((other, confidence, lift))

    return results

