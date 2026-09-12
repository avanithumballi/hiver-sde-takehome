import pandas as pd
from src.taxonomy import INTENTS

FILE = "data/golden/apple_golden_200.csv"
df = pd.read_csv(FILE)

required = [
    "customer_tweet_id","customer_time","customer_text",
    "support_tweet_id","support_time","support_text",
    "gold_intent","gold_escalate","gold_escalation_reason","annotation_notes"
]

missing = [x for x in required if x not in df.columns]
if missing:
    raise ValueError(f"Missing columns: {missing}")

if len(df) != 200:
    raise ValueError(f"Expected 200 rows, found {len(df)}")

if df["gold_intent"].fillna("").str.strip().eq("").any():
    raise ValueError("gold_intent contains blank values.")

bad = sorted(set(df["gold_intent"]) - set(INTENTS))
if bad:
    raise ValueError(f"Invalid intent labels: {bad}")

escalate = df["gold_escalate"].fillna("").astype(str).str.lower().str.strip()
if not escalate.isin(["true","false"]).all():
    raise ValueError("gold_escalate must contain only true or false.")

print("Golden set is valid.")
