# Submission Checklist

Before submitting:

- [ ] `data/raw/twcs.csv` is present locally but NOT committed.
- [ ] `python scripts/run_pipeline.py` succeeds.
- [ ] 200 golden examples have been reviewed.
- [ ] `python scripts/05_validate_golden.py` passes.
- [ ] `python scripts/06_train.py` succeeds.
- [ ] `python scripts/07_retrieve_and_reply.py` succeeds.
- [ ] `python scripts/08_escalation.py` succeeds.
- [ ] `python scripts/evaluate.py` produces `results/metrics.json`.
- [ ] 50 human reply judgments have been completed.
- [ ] Optional LLM judge has been run if an API key is available.
- [ ] Human/LLM evidence agreement has been calculated if both sets exist.
- [ ] Report contains actual measured numbers, not placeholders.
- [ ] Report discusses at least 3 concrete failure modes.
- [ ] Report includes one misleading headline number.
- [ ] Report includes next-week improvements.
- [ ] Decision log contains the design decisions.
- [ ] README explains how to reproduce the result.
- [ ] No secrets/API keys are committed.
- [ ] Raw Kaggle data is not committed.
