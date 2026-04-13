"""Preprocessing the data: missing values, encoding, scaling, etc."""
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

def _get_column_types(X):

        # Columns to DROP completely
    drop_cols = [
        "member_id",
        "id",
        "emp_title",
        "desc",
        "title",
        "url",
        "zip_code"
    ]

    # Drop them safely if they exist
    X = X.drop(columns=drop_cols, errors="ignore")
    """list of columns that are numeric"""
    numeric = X.select_dtypes(include=np.number).columns.tolist()
    """list of columns that are categorical"""
    categorical = X.select_dtypes(include=["category", "object"]).columns.tolist()
    return numeric, categorical

def build_preprocessor(X_train):
    """Building the preprocessor pipeline"""
    # get the column types
    numeric_cols, categorical_cols = _get_column_types(X_train)
    
    print(f"Numeric columns: {numeric_cols}")
    print(f"Categorical columns: {categorical_cols}")
    
    # Building the numerical pipeline
    numeric_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ])
    
    # Building the categorical pipeline
    # filling the missing value with "missing"
    # one hot encoding the categorical columns - Convert each category into separate yes/no columns
    categorical_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])    
    
    # Combining the pipelines using ColumnTransformer
    transformers = []
    # appending the tuple of transformers in the list transformers
    if numeric_cols:
        transformers.append(("num", numeric_pipeline, numeric_cols))
    if categorical_cols:
        transformers.append(("category", categorical_pipeline, categorical_cols))
    
    if not transformers:
        raise ValueError("Error: No numerical or categorical data detected.")
    
    # Finally, creating the ColumnTransformer
    # This is the "traffic controller" that routes the right pipelines to the right columns
    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

    if categorical_cols:
        X_train[categorical_cols] = X_train[categorical_cols].astype(str)
    
    
    # learns from the training data -> median, scaling arguments, categorical one hot encoding
    preprocessor.fit(X_train)
    return preprocessor

def preprocess_train_test(X_train, X_test, preprocessor):
    """Creating a function to actually use the preprocessor"""
    # preprocesses both training data and test data using same transformations
    if preprocessor is None:
        preprocessor = build_preprocessor(X_train)
    
    # applying the transformations
    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    return X_train_processed, X_test_processed, preprocessor


