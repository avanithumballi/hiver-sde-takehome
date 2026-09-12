import os
import re
import joblib
import pandas as pd

GOLDEN = "data/golden/apple_golden_200.csv"
MODEL = "results/tfidf_intent_model.joblib"
OUT = "results/final_predictions.csv"

gold = pd.read_csv(GOLDEN)
model = joblib.load(MODEL)

pred_intent = model.predict(gold["customer_text"].fillna(""))

def decide(text, intent):
    t = str(text).lower()
    reasons = []

    if intent in {"account_security", "purchase_repair_support", "unclear"}:
        reasons.append("higher-risk intent or insufficient information")

    if any(x in t for x in [
        "unauthorized","scam","phishing","stolen","hacked",
        "password","verification code","suspicious"
    ]):
        reasons.append("account/security signal")

    if any(x in t for x in [
        "refund","charged","purchase","money","payment","billing"
    ]):
        reasons.append("financial/purchase signal")

    if any(x in t for x in [
        "cracked","broken","damaged","replacement","repair","warranty"
    ]):
        reasons.append("hardware/service signal")

    if any(x in t for x in [
        "deleted","lost","missing","erase","erased"
    ]):
        reasons.append("possible data-loss signal")

    if re.search(r"\b(restart|reboot|shut off|shutdown)\b", t) and any(
        x in t for x in ["every","constantly","again","30 sec","30 seconds"]
    ):
        reasons.append("severe instability signal")

    return bool(reasons), (
        "; ".join(dict.fromkeys(reasons))
        if reasons else "routine troubleshooting signal"
    )

rows = []

for i, (text, intent) in enumerate(zip(
    gold["customer_text"].fillna(""), pred_intent
)):
    esc, reason = decide(text, intent)

    rows.append({
        "customer_tweet_id": gold.iloc[i]["customer_tweet_id"],
        "customer_text": text,
        "predicted_intent": intent,
        "predicted_escalate": esc,
        "escalation_reason": reason,
    })

pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"Saved: {OUT}")
