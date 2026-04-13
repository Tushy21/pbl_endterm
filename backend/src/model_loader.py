import joblib
from pathlib import Path

# Path to saved pipeline
MODEL_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "pipeline.joblib"

_model = None  # cache model so we don't reload every request


def get_model():
    global _model

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Please train the model first."
            )

        _model = joblib.load(MODEL_PATH)

    return _model
