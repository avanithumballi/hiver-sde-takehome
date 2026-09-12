import subprocess
import sys
import os

steps = [
    "scripts/01_create_pairs.py",
    "scripts/02_create_split.py",
    "scripts/03_create_golden.py",
]

for step in steps:
    print("\n>>>", step)
    subprocess.run([sys.executable, step], check=True)

print("""
Pipeline setup is complete.

IMPORTANT:
The 200-row golden set is currently blank and must be human-reviewed/labeled.

Then run:

python scripts/05_validate_golden.py
python scripts/06_train.py
python scripts/07_retrieve_and_reply.py
python scripts/08_escalation.py
python scripts/evaluate.py
python scripts/09_human_judge_sample.py

Optional:
python scripts/10_llm_judge.py
python scripts/11_compute_agreement.py
""")
