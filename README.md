# Hiver SDE Intern Take-Home

## Apple Support Customer Support Copilot

This repository implements an end-to-end baseline for:

1. Reconstructing AppleSupport customer/support conversations.
2. Classifying incoming customer messages into a compact intent taxonomy.
3. Retrieving historically resolved support examples.
4. Drafting a conservative, evidence-grounded response.
5. Separately deciding whether to auto-handle or escalate.
6. Evaluating intent and escalation on a 200-example golden set.
7. Supporting optional LLM-as-judge reply evaluation and human agreement measurement.

## 1. Dataset

Use the Kaggle Customer Support on Twitter dataset.

Expected local path:

`data/raw/twcs.csv`

The raw CSV is deliberately not included in this repository.

Important dataset fields used:
- `tweet_id`
- `author_id`
- `inbound`
- `created_at`
- `text`
- `response_tweet_id`
- `in_response_to_tweet_id`

Customer messages are linked to the AppleSupport response through `in_response_to_tweet_id`.

## 2. Why AppleSupport?

AppleSupport provides a large number of usable support interactions and covers many recurring support themes, including updates, apps/features, connectivity, account/security, purchases/repairs, and device problems.

## 3. Intent taxonomy

The taxonomy is deliberately small and operational.

- `software_update`: Problems installing, updating, restoring, or reverting an operating-system update, including problems directly caused by an iOS or macOS update.
- `device_performance`: General device instability, performance, crashing, freezing, unexpected restarting, overheating, shutdowns, or other device-level problems.
- `app_or_feature_issue`: A specific Apple app, feature, or functionality is malfunctioning or behaving unexpectedly.
- `connectivity`: Wi-Fi, Bluetooth, cellular, phone-call, or other network and connection problems.
- `account_security`: Account access, authentication, suspicious communications, phishing, security concerns, or being locked out of a device or account.
- `purchase_repair_support`: Purchases, trade-ins, repairs, replacements, damaged hardware, store support, or questions about obtaining service for a product.
- `information_request`: Primarily requesting information, compatibility details, feature explanations, how-to guidance, or other non-problem-specific product information.
- `unclear`: There is not enough information to confidently determine the customer's intent.

Escalation is a separate decision from intent.

## 4. Reproducible run

From the repository root:

```powershell
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
```

This creates:
- `data/processed/apple_support_pairs.csv`
- `data/processed/apple_train.csv`
- `data/processed/apple_test.csv`
- `data/golden/apple_golden_200.csv`
- `results/intent_predictions.csv`
- `results/golden_replies.csv`
- `results/final_predictions.csv`
- `results/metrics.json`

The first run creates a blank 200-example golden set. Human review is required before those labels can honestly be called hand-labelled.

## 5. Golden set

The golden set is sampled from the held-out test period with:

`random_state=2026`

The sample contains exactly 200 examples.

To label it:
1. Open `data/golden/apple_golden_200.csv`.
2. Fill:
   - `gold_intent`
   - `gold_escalate`
   - `gold_escalation_reason`
   - `annotation_notes`
3. Run:

```powershell
python scripts/validate_golden.py
```

A separate `gold_labels.csv` can also be used with `apply_gold_labels.py`.

## 6. Model baseline

The baseline uses:
- word TF-IDF features;
- character TF-IDF features;
- Logistic Regression with balanced classes.

Weak labels are used only to train the baseline. They are not presented as human ground truth.

## 7. Retrieval and reply

The system retrieves the most similar historical customer message from the training split and uses the corresponding historical support response as evidence.

The generated reply is deliberately conservative. It does not invent product-specific procedures that are absent from the retrieved historical evidence.

## 8. Escalation

The escalation policy considers:
- account/security risk;
- purchase/financial issues;
- repair/replacement/hardware damage;
- possible data loss;
- severe repeated instability;
- unclear cases where safe handling is not possible.

This is intentionally separate from intent classification.

## 9. Evaluation

Run:

```powershell
python scripts/evaluate.py
```

Metrics include:
- intent accuracy;
- intent classification report;
- escalation precision;
- escalation recall;
- escalation F1;
- average retrieval similarity;
- average draft length.

Do not put invented values in the report. Copy actual values from `results/metrics.json`.

## 10. Reply evaluation

Create a 50-example human-review sheet:

```powershell
python scripts/human_judge_sample.py
```

Optional LLM judge:

```powershell
$env:OPENAI_API_KEY="YOUR_KEY"
python scripts/llm_judge.py
python scripts/compute_agreement.py
```

The LLM judge evaluates:
- helpfulness;
- correctness;
- clarity;
- evidence support.

Human agreement is measured on the evidence-supported field.

## 11. Submission notes

Do not commit:
- `data/raw/twcs.csv`;
- generated model files;
- generated result files containing customer text unless appropriate for the submission.

Review the dataset's Kaggle license/terms before redistribution.

AI-assisted proposed annotations must be reviewed before being described as independently hand-labelled.
