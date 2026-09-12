import os
import json
import pandas as pd

try:
    from openai import OpenAI
except ImportError:
    raise SystemExit("Run: python -m pip install -r requirements.txt")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("GEMINI_API_KEY is not set.")

MODEL = os.getenv("GEMINI_JUDGE_MODEL", "gemini-3.6-flash")
INPUT = "results/golden_replies.csv"
OUT = "results/llm_judgments.csv"

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

df = pd.read_csv(INPUT)
rows = []

for i, row in df.iterrows():

    prompt = f"""
You are evaluating a customer-support assistant.

CUSTOMER:
{row['customer_text']}

HISTORICAL EVIDENCE:
{row['retrieved_support_text']}

DRAFT REPLY:
{row['draft_reply']}

Evaluate the draft reply against the customer message and the historical
evidence.

Return JSON only with exactly these fields:

{{
  "helpful": integer from 1 to 5,
  "correct": integer from 1 to 5,
  "clear": integer from 1 to 5,
  "evidence_supported": 0 or 1,
  "reason": "brief reason"
}}

Scoring:
- helpful: Does the reply meaningfully help the customer?
- correct: Is the advice appropriate for the customer's issue?
- clear: Is the reply understandable and concise?
- evidence_supported: Set to 1 ONLY if the substantive advice in the
  draft reply is supported by the historical evidence shown.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a rigorous customer-support evaluation judge. Return valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()

        # Remove markdown JSON fences if the model adds them.
        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()

        result = json.loads(raw)

    except Exception as e:
        result = {
            "helpful": None,
            "correct": None,
            "clear": None,
            "evidence_supported": None,
            "reason": f"Judge error: {str(e)[:400]}"
        }

    rows.append(result)

    if (i + 1) % 10 == 0:
        print(f"Judged {i + 1}/{len(df)} examples")

out = pd.concat(
    [df.reset_index(drop=True), pd.DataFrame(rows)],
    axis=1
)

out.to_csv(OUT, index=False)

print(f"Saved: {OUT}")