# backend/src/utils.py

import numpy as np


DEFAULT_THRESHOLD = 0.35  # Better than 0.5 for credit risk


def apply_threshold(probability: float, threshold: float = DEFAULT_THRESHOLD):
    return int(probability >= threshold)


def map_risk(probability: float):
    if probability < 0.2:
        return "Low Risk"
    elif probability < 0.5:
        return "Medium Risk"
    else:
        return "High Risk"
