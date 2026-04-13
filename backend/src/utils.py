# backend/src/utils.py


# ---------------------------------------------------------
# Apply Business Threshold
# ---------------------------------------------------------

def apply_threshold(probability: float, threshold: float = 0.5) -> int:
    """
    Convert probability into binary prediction.
    """
    return 1 if probability >= threshold else 0


# ---------------------------------------------------------
# Risk Category Mapping
# ---------------------------------------------------------

def map_risk(probability: float) -> str:
    """
    Map probability to risk category.
    """
    if probability < 0.3:
        return "Low"
    elif probability < 0.6:
        return "Medium"
    else:
        return "High"
