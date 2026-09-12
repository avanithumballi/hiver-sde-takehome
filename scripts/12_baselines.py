import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parents[1]

GOLD_EXAMPLES_PATH = BASE_DIR / "data" / "golden" / "apple_golden_200.csv"
GOLD_LABELS_PATH = BASE_DIR / "data" / "golden" / "gold_labels.csv"
PRED_PATH = BASE_DIR / "results" / "final_predictions.csv"

# ---------------------------------------------------------
# Load files
# ---------------------------------------------------------

gold_examples = pd.read_csv(GOLD_EXAMPLES_PATH)
gold_labels = pd.read_csv(GOLD_LABELS_PATH)
predictions = pd.read_csv(PRED_PATH)

print("Golden examples columns:")
print(gold_examples.columns.tolist())

print("\nGold labels columns:")
print(gold_labels.columns.tolist())

print("\nPrediction columns:")
print(predictions.columns.tolist())

# ---------------------------------------------------------
# Attach the reviewed gold labels to the golden examples
# ---------------------------------------------------------

if len(gold_examples) != len(gold_labels):
    raise ValueError(
        f"Golden examples ({len(gold_examples)}) and gold labels "
        f"({len(gold_labels)}) have different row counts."
    )

gold = gold_examples.copy()
gold["gold_intent"] = gold_labels["gold_intent"].values

# ---------------------------------------------------------
# Match golden examples to model predictions
# ---------------------------------------------------------

gold["customer_tweet_id"] = gold["customer_tweet_id"].astype(str)
predictions["customer_tweet_id"] = predictions["customer_tweet_id"].astype(str)

df = gold.merge(
    predictions[
        [
            "customer_tweet_id",
            "customer_text",
            "predicted_intent"
        ]
    ],
    on="customer_tweet_id",
    how="inner",
    suffixes=("_gold", "_prediction")
)

print(f"\nGolden examples matched to predictions: {len(df)}")

if len(df) != len(gold):
    raise ValueError(
        f"Only {len(df)} of {len(gold)} golden examples matched "
        "the prediction file."
    )

# Use the golden-set text
df["text"] = df["customer_text_gold"].fillna("").astype(str)

df["gold_intent"] = df["gold_intent"].astype(str)
df["predicted_intent"] = df["predicted_intent"].astype(str)

# ---------------------------------------------------------
# BASELINE 1: Majority-class baseline
# ---------------------------------------------------------

majority_class = df["gold_intent"].mode()[0]

majority_predictions = [majority_class] * len(df)

majority_accuracy = accuracy_score(
    df["gold_intent"],
    majority_predictions
)

# ---------------------------------------------------------
# BASELINE 2: Simple keyword/rule classifier
# ---------------------------------------------------------

def keyword_classifier(text):

    text = text.lower()

    # Account / security
    if any(k in text for k in [
        "hack",
        "hacked",
        "phishing",
        "scam",
        "security",
        "password",
        "locked out",
        "stolen",
        "fraud"
    ]):
        return "account_security"

    # Software update
    if any(k in text for k in [
        "ios",
        "update",
        "updating",
        "upgrade",
        "restore",
        "downgrade"
    ]):
        return "software_update"

    # Connectivity
    if any(k in text for k in [
        "wifi",
        "wi-fi",
        "bluetooth",
        "cellular",
        "network",
        "signal",
        "internet",
        "connection",
        "connect",
        "calls"
    ]):
        return "connectivity"

    # Purchase / repair
    if any(k in text for k in [
        "repair",
        "replacement",
        "replace",
        "refund",
        "purchase",
        "buy",
        "trade in",
        "trade-in",
        "store",
        "damaged",
        "broken screen"
    ]):
        return "purchase_repair_support"

    # Device performance
    if any(k in text for k in [
        "slow",
        "freezing",
        "freeze",
        "crash",
        "crashing",
        "restart",
        "restarting",
        "overheating",
        "battery",
        "shut down",
        "shutdown"
    ]):
        return "device_performance"

    # App / feature
    if any(k in text for k in [
        "app",
        "camera",
        "photos",
        "facetime",
        "imessage",
        "siri",
        "icloud",
        "airdrop",
        "live photos",
        "notification"
    ]):
        return "app_or_feature_issue"

    # Information request
    if any(k in text for k in [
        "how do i",
        "how can i",
        "does iphone",
        "can i",
        "is there a way",
        "what is",
        "compatible",
        "compatibility"
    ]):
        return "information_request"

    return "unclear"


keyword_predictions = df["text"].apply(keyword_classifier)

keyword_accuracy = accuracy_score(
    df["gold_intent"],
    keyword_predictions
)

# ---------------------------------------------------------
# MAIN MODEL
# ---------------------------------------------------------

model_accuracy = accuracy_score(
    df["gold_intent"],
    df["predicted_intent"]
)

# ---------------------------------------------------------
# Print comparison
# ---------------------------------------------------------

print("\n===================================================")
print("              BASELINE COMPARISON")
print("===================================================\n")

print(f"Golden examples evaluated: {len(df)}")

print(
    f"Majority-class baseline: "
    f"{majority_accuracy:.4f} "
    f"({majority_accuracy * 100:.1f}%)"
)

print(
    f"Keyword/rule baseline:   "
    f"{keyword_accuracy:.4f} "
    f"({keyword_accuracy * 100:.1f}%)"
)

print(
    f"TF-IDF + Logistic model: "
    f"{model_accuracy:.4f} "
    f"({model_accuracy * 100:.1f}%)"
)

print("\n---------------------------------------------------")

print(
    f"Model improvement over majority: "
    f"{(model_accuracy - majority_accuracy) * 100:.1f} percentage points"
)

print(
    f"Model improvement over keyword:  "
    f"{(model_accuracy - keyword_accuracy) * 100:.1f} percentage points"
)

print("---------------------------------------------------")

print(f"\nMajority class was: {majority_class}")

# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

output = pd.DataFrame({
    "approach": [
        "Majority-class baseline",
        "Keyword/rule baseline",
        "TF-IDF + Logistic Regression"
    ],
    "intent_accuracy": [
        majority_accuracy,
        keyword_accuracy,
        model_accuracy
    ]
})

output_path = BASE_DIR / "results" / "baseline_comparison.csv"

output.to_csv(output_path, index=False)

print(f"\nSaved: {output_path}")