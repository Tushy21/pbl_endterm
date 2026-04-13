# Credit Risk Prediction Web App (ML + SHAP)

Predict loan default risk using LendingClub-style data, with Explainable AI (SHAP).

## Step 1 done

- Project layout: `src/`, `data/`, `artifacts/`
- `requirements.txt` — install with: `pip install -r requirements.txt`
- `src/config.py` — paths for data and saved model (override via `DATA_DIR`, `ARTIFACTS_DIR` in `.env`)

## Next steps

1. Install deps: `pip install -r requirements.txt`
2. Add LendingClub CSV to `data/` as `loan_data.csv` (or update `config.RAW_DATA_FILENAME`)
3. Implement data loading (Step 2)
