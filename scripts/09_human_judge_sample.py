import os
import pandas as pd

INPUT = "results/golden_replies.csv"
OUT = "results/human_judge_sample_50.csv"

df = pd.read_csv(INPUT)
n = min(50, len(df))
sample = df.sample(n=n, random_state=2026).copy()

sample["human_evidence_supported"] = ""
sample["human_helpful"] = ""
sample["human_correct"] = ""
sample["human_clear"] = ""
sample["human_notes"] = ""

os.makedirs("results", exist_ok=True)
sample.to_csv(OUT,index=False)

print(f"Created {n}-row human review sheet: {OUT}")
