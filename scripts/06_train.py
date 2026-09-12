import os
import re
import joblib
import pandas as pd
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

TRAIN = "data/processed/apple_train.csv"
GOLDEN = "data/golden/apple_golden_200.csv"
MODEL = "results/tfidf_intent_model.joblib"
PRED = "results/intent_predictions.csv"

def weak_label(text):
    t = str(text).lower()

    # More specific categories get precedence over generic device symptoms.
    if re.search(r"\bios\s*[\d.]|\bmacos\b|\bhigh sierra\b|\bupdate\b|\bupdat(e|ing|ed)\b|\brestore\b", t):
        return "software_update"

    if any(x in t for x in [
        "wifi","wi-fi","bluetooth","cellular","signal","network",
        "can't call","cannot call","calls","connection"
    ]):
        return "connectivity"

    if any(x in t for x in [
        "password","apple id","icloud login","locked",
        "verification code","scam","phishing","fake email","unauthorized"
    ]):
        return "account_security"

    if any(x in t for x in [
        "repair","replacement","replace","warranty","refund",
        "purchase","damaged","cracked","genius bar","store"
    ]):
        return "purchase_repair_support"

    if any(x in t for x in [
        "crash","crashing","freeze","frozen","reboot","restarts",
        "restart","shut off","shutdown","overheat","slow","lag","battery"
    ]):
        return "device_performance"

    if any(x in t for x in [
        "how do i","how to","compatible","compatibility","which",
        "can i","what is","when is"
    ]):
        return "information_request"

    if any(x in t for x in [
        "itunes","photos","messages","facetime","siri","music",
        "podcast","app store","notes","mail","camera","maps",
        "apple pay","watch"
    ]):
        return "app_or_feature_issue"

    return "unclear"

train = pd.read_csv(TRAIN)
train["weak_intent"] = train["customer_text"].fillna("").map(weak_label)

print("Weak-label distribution:")
print(train["weak_intent"].value_counts())

features = FeatureUnion([
    ("word", TfidfVectorizer(
        ngram_range=(1,2),
        min_df=2,
        max_features=120000,
        sublinear_tf=True
    )),
    ("char", TfidfVectorizer(
        analyzer="char",
        ngram_range=(3,5),
        min_df=2,
        max_features=80000,
        sublinear_tf=True
    )),
])

model = Pipeline([
    ("features", features),
    ("classifier", LogisticRegression(
        max_iter=1200,
        class_weight="balanced",
        n_jobs=-1
    ))
])

model.fit(train["customer_text"], train["weak_intent"])

os.makedirs("results", exist_ok=True)
joblib.dump(model, MODEL)

gold = pd.read_csv(GOLDEN)
pred = model.predict(gold["customer_text"].fillna(""))

pd.DataFrame({
    "customer_tweet_id": gold["customer_tweet_id"],
    "predicted_intent": pred
}).to_csv(PRED, index=False)

print(f"Model: {MODEL}")
print(f"Predictions: {PRED}")
