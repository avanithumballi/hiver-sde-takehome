import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TRAIN = "data/processed/apple_train.csv"
GOLDEN = "data/golden/apple_golden_200.csv"
MODEL = "results/tfidf_intent_model.joblib"
OUT = "results/golden_replies.csv"

train = pd.read_csv(TRAIN)
gold = pd.read_csv(GOLDEN)
model = joblib.load(MODEL)

retriever = TfidfVectorizer(
    ngram_range=(1,2),
    min_df=2,
    max_features=120000,
    sublinear_tf=True
)

X = retriever.fit_transform(train["customer_text"].fillna(""))
pred = model.predict(gold["customer_text"].fillna(""))

def draft_reply(intent, evidence):
    evidence = str(evidence).strip()

    if intent == "unclear":
        return (
            "I’m sorry you’re running into this. Could you share a little more "
            "detail about what is happening and which device or software version "
            "you’re using?"
        )

    if not evidence:
        return (
            "I’m sorry you’re having trouble. Could you share a few more details "
            "about the issue so we can point you to the right next step?"
        )

    # Keep the historical response as the evidence basis rather than inventing
    # a new unsupported troubleshooting procedure.
    evidence = evidence.replace("\n", " ").strip()
    if len(evidence) > 500:
        evidence = evidence[:500].rsplit(" ",1)[0] + "..."

    return (
        "I’m sorry you’re running into this. Based on a similar Apple Support "
        "case, a relevant next step was: " + evidence +
        " If that does not resolve the issue, Apple Support can help with the "
        "next troubleshooting or service step."
    )

rows = []

for i, (text, intent) in enumerate(zip(gold["customer_text"].fillna(""), pred)):
    q = retriever.transform([text])
    scores = cosine_similarity(q, X).ravel()

    # Top historical case from TRAIN only.
    idx = int(np.argmax(scores))
    evidence = train.iloc[idx]["support_text"]

    rows.append({
        "customer_tweet_id": gold.iloc[i]["customer_tweet_id"],
        "customer_text": text,
        "predicted_intent": intent,
        "retrieved_support_text": evidence,
        "retrieval_score": float(scores[idx]),
        "draft_reply": draft_reply(intent, evidence),
    })

out = pd.DataFrame(rows)
os.makedirs("results", exist_ok=True)
out.to_csv(OUT, index=False)

print(f"Saved: {OUT}")
