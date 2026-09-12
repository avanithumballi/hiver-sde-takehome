import os
import pandas as pd

TEST = "data/processed/apple_test.csv"
OUT = "data/golden/apple_golden_200.csv"

df = pd.read_csv(TEST)

if len(df) < 200:
    raise ValueError("Need at least 200 held-out test examples.")

gold = df.sample(n=200, random_state=2026).sort_index().copy()

gold["gold_intent"] = ""
gold["gold_escalate"] = ""
gold["gold_escalation_reason"] = ""
gold["annotation_notes"] = ""

cols = [
    "customer_tweet_id","customer_time","customer_text",
    "support_tweet_id","support_time","support_text",
    "gold_intent","gold_escalate","gold_escalation_reason","annotation_notes"
]

os.makedirs("data/golden", exist_ok=True)
gold[cols].to_csv(OUT, index=False)

print(f"Created deterministic golden set: {len(gold)} rows")
print(f"Saved: {OUT}")
