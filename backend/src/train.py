"""
train.py

Train multiple ML models, evaluate them, and save the best performing model.
This module handles:
- Model training (Logistic Regression, Random Forest, XGBoost)
- Model evaluation (accuracy, precision, recall, F1, ROC-AUC)
- Model comparison
- Saving the best model
"""

import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

from src.data_loader import load_and_split
from src.preprocess import build_preprocessor
from src.config import get_pipeline_path, ARTIFACTS_DIR


def evaluate_model(y_true, y_pred, y_pred_proba, model_name):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_pred_proba)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    print(f"\n{'='*60}")
    print(f"📊 {model_name} - EVALUATION RESULTS")
    print(f"{'='*60}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print(f"\nConfusion Matrix:")
    print(f"  TN: {tn:5d}  |  FP: {fp:5d}")
    print(f"  FN: {fn:5d}  |  TP: {tp:5d}")
    print(f"{'='*60}")

    return {
        'model_name': model_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': (tn, fp, fn, tp)
    }


def train_single_model(model, model_name, X_train, y_train, X_test, y_test):
    print(f"\n🔄 Training {model_name}...")
    model.fit(X_train, y_train)
    print(f"✅ {model_name} trained successfully!")

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    metrics = evaluate_model(y_test, y_pred, y_pred_proba, model_name)
    return model, metrics


def train_all_models(X_train, y_train, X_test, y_test):
    print("\n" + "="*60)
    print("🚀 TRAINING MULTIPLE MODELS")
    print("="*60)

    models = {
        'Logistic Regression': LogisticRegression(
            max_iter=1000,
            random_state=42,
            class_weight='balanced'
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        ),
        'XGBoost': XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            scale_pos_weight=3,
            eval_metric='logloss'
        )
    }

    results = {}

    for model_name, model in models.items():
        trained_model, metrics = train_single_model(
            model, model_name, X_train, y_train, X_test, y_test
        )
        results[model_name] = {
            'model': trained_model,
            'metrics': metrics
        }

    return results


def select_best_model(results):
    print("\n" + "="*60)
    print("🏆 MODEL COMPARISON")
    print("="*60)

    comparison = []
    for model_name, result in results.items():
        metrics = result['metrics']
        comparison.append({
            'Model': model_name,
            'Accuracy': f"{metrics['accuracy']:.4f}",
            'Precision': f"{metrics['precision']:.4f}",
            'Recall': f"{metrics['recall']:.4f}",
            'F1': f"{metrics['f1_score']:.4f}",
            'ROC-AUC': f"{metrics['roc_auc']:.4f}"
        })

    df_comparison = pd.DataFrame(comparison)
    print(df_comparison.to_string(index=False))

    best_model_name = max(
        results.keys(),
        key=lambda x: results[x]['metrics']['roc_auc']
    )

    best_model = results[best_model_name]['model']
    best_metrics = results[best_model_name]['metrics']

    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   ROC-AUC: {best_metrics['roc_auc']:.4f}")
    print("="*60)

    return best_model, best_model_name, best_metrics


def save_pipeline(preprocessor, model, filepath=None):
    if filepath is None:
        filepath = get_pipeline_path()

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    pipeline = {
        'preprocessor': preprocessor,
        'model': model
    }

    joblib.dump(pipeline, filepath)
    print(f"\n💾 Pipeline saved to: {filepath}")


def train_pipeline():
    """
    Complete training pipeline (5 selected features only):
    1. Load and split data
    2. Select important features
    3. Build preprocessor
    4. Train models
    5. Select best model
    6. Save pipeline
    """

    print("\n" + "="*60)
    print("🚀 STARTING COMPLETE TRAINING PIPELINE (5 FEATURES)")
    print("="*60)

    # Step 1: Load and split data
    print("\n1️⃣  Loading data...")
    X_train, X_test, y_train, y_test = load_and_split()

    # Step 2: Select only important features
    selected_features = [
        "loan_amnt",
        "annual_inc",
        "dti",
        "revol_bal",
        "total_acc"
    ]

    X_train = X_train[selected_features]
    X_test = X_test[selected_features]

    print(f"✅ Using features: {selected_features}")
    print(f"Training shape after selection: {X_train.shape}")
    print(f"Test shape after selection: {X_test.shape}")

    # Step 3: Build and fit preprocessor
    print("\n2️⃣  Building preprocessor...")
    preprocessor = build_preprocessor(X_train)

    # Step 4: Transform data
    print("\n3️⃣  Preprocessing data...")
    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    print(f"Processed training shape: {X_train_processed.shape}")
    print(f"Processed test shape: {X_test_processed.shape}")

    # Step 5: Train models
    print("\n4️⃣  Training models...")
    results = train_all_models(
        X_train_processed, y_train,
        X_test_processed, y_test
    )

    # Step 6: Select best model
    print("\n5️⃣  Selecting best model...")
    best_model, best_name, best_metrics = select_best_model(results)

    # Step 7: Save pipeline
    print("\n6️⃣  Saving pipeline...")
    save_pipeline(preprocessor, best_model)

    print("\n" + "="*60)
    print("✅ TRAINING COMPLETED SUCCESSFULLY!")
    print(f"Best Model: {best_name}")
    print(f"ROC-AUC: {best_metrics['roc_auc']:.4f}")
    print("="*60)

    return preprocessor, best_model, best_metrics



if __name__ == "__main__":
    print("🚀 Starting training...")

    train_pipeline()

    print("✅ Training complete.")

