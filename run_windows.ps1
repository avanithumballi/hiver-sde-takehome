$ErrorActionPreference = "Stop"

Write-Host "Installing dependencies..."
python -m pip install -r requirements.txt

Write-Host "Running data preparation..."
python scripts/run_pipeline.py
