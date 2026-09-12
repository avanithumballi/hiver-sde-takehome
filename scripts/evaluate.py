import json
import os
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
)

GOLDEN = "data/golden/apple_golden_200.csv"
INTENT = "results/intent_predictions.csv"
ESC = "results/final_predictions.csv"
REPLIES = "results/golden_replies.csv"

gold = pd.read_csv(GOLDEN)
intent = pd.read_csv(INTENT)
esc = pd.read_csv(ESC)
replies = pd.read_csv(REPLIES)

m = gold[[
    "customer_tweet_id","gold_intent","gold_escalate"
]].merge(intent, on="customer_tweet_id", validate="one_to_one").merge(
    esc[["customer_tweet_id","predicted_escalate"]],
    on="customer_tweet_id",
    validate="one_to_one"
).merge(
    replies[[
        "customer_tweet_id","draft_reply","retrieval_score"
    ]],
    on="customer_tweet_id",
    validate="one_to_one"
)

gold_escalate = m["gold_escalate"].astype(str).str.lower().eq("true")
pred_escalate = m["predicted_escalate"].astype(bool)

precision, recall, f1, _ = precision_recall_fscore_support(
    gold_escalate,
    pred_escalate,
    average="binary",
    zero_division=0
)

metrics = {
    "n_golden": int(len(m)),
    "intent_accuracy": float(
        accuracy_score(m["gold_intent"], m["predicted_intent"])
    ),
    "escalation_precision": float(precision),
    "escalation_recall": float(recall),
    "escalation_f1": float(f1),
    "average_reply_chars": float(
        m["draft_reply"].fillna("").str.len().mean()
    ),
    "average_retrieval_score": float(m["retrieval_score"].mean()),
}

os.makedirs("results", exist_ok=True)
with open("results/metrics.json","w",encoding="utf-8") as f:
    json.dump(metrics,f,indent=2)

print(json.dumps(metrics, indent=2))
print("\nIntent classification report:")
print(classification_report(
    m["gold_intent"],
    m["predicted_intent"],
    zero_division=0
))
