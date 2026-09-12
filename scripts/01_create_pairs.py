import os
import pandas as pd

RAW = "data/raw/twcs.csv"
OUT = "data/processed/apple_support_pairs.csv"

if not os.path.exists(RAW):
    raise FileNotFoundError(f"Missing dataset: {RAW}")

df = pd.read_csv(RAW, dtype=str)
df["inbound"] = df["inbound"].fillna("").str.lower().str.strip()

customers = df[(df["inbound"] == "true") & df["tweet_id"].notna()].copy()
support = df[(df["inbound"] != "true") & (df["author_id"] == "AppleSupport")].copy()

customers = customers.rename(columns={
    "tweet_id": "customer_tweet_id",
    "created_at": "customer_time",
    "text": "customer_text",
})

support = support.rename(columns={
    "tweet_id": "support_tweet_id",
    "created_at": "support_time",
    "text": "support_text",
    "in_response_to_tweet_id": "customer_tweet_id",
})

pairs = customers[
    ["customer_tweet_id","customer_time","customer_text"]
].merge(
    support[
        ["support_tweet_id","support_time","support_text","customer_tweet_id"]
    ],
    on="customer_tweet_id",
    how="inner"
)

pairs = pairs.drop_duplicates("customer_tweet_id")
pairs["customer_time"] = pd.to_datetime(pairs["customer_time"], errors="coerce", utc=True)
pairs = pairs.dropna(subset=["customer_time"]).sort_values("customer_time")

os.makedirs("data/processed", exist_ok=True)
pairs.to_csv(OUT, index=False)

print(f"AppleSupport paired conversations: {len(pairs):,}")
print(f"Saved: {OUT}")
