"""Project paths and constants. Used by data loading, training, and API."""
import os
from pathlib import Path

# Project root (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Default directories (can override via env)
DATA_DIR = PROJECT_ROOT / "data"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

DATA_DIR = Path(os.getenv("DATA_DIR", str(DATA_DIR)))
ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR", str(ARTIFACTS_DIR)))

# Filenames for saved artifacts
PIPELINE_FILENAME = "pipeline.joblib"
RAW_DATA_FILENAME = "loan_data.csv"


def get_pipeline_path() -> Path:
    """Path to the full pipeline artifact (model + preprocessor)."""
    return ARTIFACTS_DIR / PIPELINE_FILENAME


def get_data_path() -> Path:
    """Path to raw loan data CSV."""
    return DATA_DIR / RAW_DATA_FILENAME
