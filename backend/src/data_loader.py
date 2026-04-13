"""
data_loader.py

Load LendingClub-style data, map target to 0/1, and split into train/test.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from src.config import get_data_path

# Column name for loan outcome in the CSV (adjust if your dataset uses a different name)
LOAN_STATUS_COL = "loan_status"

# Values that mean "default" (1); all others that we map become "non-default" (0) or are dropped
DEFAULT_STATUSES = ("Charged Off", "Default", "Charged off", "default")


def load_data():
    """
    Load raw CSV into a DataFrame.
    
    Returns:
    --------
    pd.DataFrame : Raw loan data
    """
    # Get path from config
    path = get_data_path()
    
    # Read the CSV file into a dataframe
    print(f"📂 Loading data from: {path}")
    df = pd.read_csv(path)
    print(f"✅ Data loaded successfully! Shape: {df.shape}")
    
    return df


def map_target(df):
    """
    Map loan_status to binary target (0 = non-default, 1 = default).
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with loan_status column
    
    Returns:
    --------
    pd.DataFrame : DataFrame with 'target' column added
    """
    if LOAN_STATUS_COL not in df.columns:
        raise ValueError(f"Column '{LOAN_STATUS_COL}' not found in dataset.")
    
    # Map to binary: 1 if default, 0 otherwise
    df['target'] = df[LOAN_STATUS_COL].apply(
        lambda x: 1 if x in DEFAULT_STATUSES else 0
    )
    
    print(f"\n📊 Target distribution:")
    print(df['target'].value_counts())
    print(f"   Default rate: {df['target'].mean():.2%}")
    
    return df


def load_and_split(test_size=0.2, random_state=42):
    """
    Load data, map target, and split into train/test.
    
    Parameters:
    -----------
    test_size : float
        Proportion of dataset for testing (default: 0.2 = 20%)
    random_state : int
        Random seed for reproducibility (default: 42)
    
    Returns:
    --------
    tuple : (X_train, X_test, y_train, y_test)
        - X_train: Training features
        - X_test: Test features
        - y_train: Training labels
        - y_test: Test labels
    
    Example:
    --------
    >>> X_train, X_test, y_train, y_test = load_and_split()
    >>> print(X_train.shape)  # (26064, 50)
    """
    # Step 1: Load raw data
    df = load_data()
    
    # Step 2: Map target variable
    df = map_target(df)
    
    # Step 3: Separate features and target
    # Drop loan_status (original) and target (our label)
    X = df.drop([LOAN_STATUS_COL, 'target'], axis=1)
    y = df['target']
    
    print(f"\n📋 Features shape: {X.shape}")
    print(f"📋 Target shape: {y.shape}")
    
    # Step 4: Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state,
        stratify=y  # Keep same proportion of defaults in train/test
    )
    
    print(f"\n✂️  Data split complete:")
    print(f"   Training set: {X_train.shape}")
    print(f"   Test set: {X_test.shape}")
    print(f"   Train default rate: {y_train.mean():.2%}")
    print(f"   Test default rate: {y_test.mean():.2%}")
    
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    """
    Test the data loader functions.
    Run this file directly to test: python -m src.data_loader
    """

    
    # Test loading and splitting
    X_train, X_test, y_train, y_test = load_and_split()
    
 