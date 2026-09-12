import pandas as pd

GOLDEN = "data/golden/apple_golden_200.csv"
LABELS = "data/golden/gold_labels.csv"

gold = pd.read_csv(GOLDEN)
labels = pd.read_csv(LABELS)

expected = [
    "gold_intent",
    "gold_escalate",
    "gold_escalation_reason",
    "annotation_notes",
]

if list(labels.columns) != expected:
    raise ValueError(f"gold_labels.csv columns must be exactly: {expected}")

if len(gold) != 200 or len(labels) != 200:
    raise ValueError("Both files must have exactly 200 rows.")

for c in expected:
    gold[c] = labels[c].values

gold.to_csv(GOLDEN, index=False)
print("Applied gold labels to the 200-row golden set.")
