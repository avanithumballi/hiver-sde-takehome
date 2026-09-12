import json
import os
import pandas as pd
from sklearn.metrics import cohen_kappa_score

LLM = "results/llm_judgments.csv"
HUMAN = "results/human_judge_sample_50.csv"
OUT = "results/judge_agreement.json"

llm = pd.read_csv(LLM)
human = pd.read_csv(HUMAN)

m = human[[
    "customer_tweet_id",
    "human_evidence_supported"
]].merge(
    llm[[
        "customer_tweet_id",
        "evidence_supported"
    ]],
    on="customer_tweet_id",
    how="inner"
)

m["human"] = m["human_evidence_supported"].astype(str).str.lower().map({
    "true":1, "false":0, "1":1, "0":0
})
m["llm"] = pd.to_numeric(m["evidence_supported"], errors="coerce")

m = m.dropna(subset=["human","llm"])

if len(m) < 2:
    raise SystemExit("Need at least two overlapping labeled examples.")

kappa = cohen_kappa_score(m["human"].astype(int),m["llm"].astype(int))

result = {
    "n_agreement_examples": int(len(m)),
    "cohen_kappa": float(kappa)
}

os.makedirs("results",exist_ok=True)
with open(OUT,"w",encoding="utf-8") as f:
    json.dump(result,f,indent=2)

print(json.dumps(result,indent=2))
