import os
import pandas as pd

INFILE = "data/processed/apple_support_pairs.csv"
TRAIN = "data/processed/apple_train.csv"
TEST = "data/processed/apple_test.csv"

df = pd.read_csv(INFILE)
df["customer_time"] = pd.to_datetime(df["customer_time"], errors="coerce", utc=True)
df = df.dropna(subset=["customer_time"]).sort_values("customer_time").reset_index(drop=True)

cut = int(len(df) * 0.8)
train = df.iloc[:cut].copy()
test = df.iloc[cut:].copy()

os.makedirs("data/processed", exist_ok=True)
train.to_csv(TRAIN, index=False)
test.to_csv(TEST, index=False)

print(f"Train rows: {len(train):,}")
print(f"Test rows:  {len(test):,}")
print(f"Train period: {train.customer_time.min()} -> {train.customer_time.max()}")
print(f"Test period:  {test.customer_time.min()} -> {test.customer_time.max()}")
