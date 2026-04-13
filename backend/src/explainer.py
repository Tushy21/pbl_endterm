import shap
import pandas as pd
import numpy as np

def get_explanation(pipeline, input_df: pd.DataFrame):
    """
    Computes SHAP feature contributions for the given input data using the trained pipeline.
    
    Args:
        pipeline: The trained model pipeline dictionary containing 'preprocessor' and 'model'.
        input_df: A pandas DataFrame containing the input features.
        
    Returns:
        A list of dictionaries containing {feature: str, contribution: float}
    """
    preprocessor = pipeline["preprocessor"]
    model = pipeline["model"]
    
    # Process the input data
    X_processed = preprocessor.transform(input_df)
    
    # Convert sparse matrix to dense if necessary
    if hasattr(X_processed, "toarray"):
        X_processed = X_processed.toarray()
    
    # Determine the model type to use the appropriate explainer
    model_type = type(model).__name__
    
    try:
        if "XGB" in model_type or "Forest" in model_type or "Tree" in model_type:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_processed)
            
            if isinstance(shap_values, list):
                # For some tree models (like Random Forest), shap_values is a list for each class
                contributions = shap_values[1][0]
            else:
                if len(shap_values.shape) == 3:
                    contributions = shap_values[0, :, 1]
                else:
                    contributions = shap_values[0]
                    
        elif "Logistic" in model_type or "Linear" in model_type:
            # For linear models without a background dataset, straightforward W * X 
            contributions = model.coef_[0] * X_processed[0]
            
        else:
            # Fallback
            if hasattr(model, 'feature_importances_'):
                contributions = model.feature_importances_
            elif hasattr(model, 'coef_'):
                contributions = model.coef_[0] * X_processed[0]
            else:
                contributions = np.zeros(X_processed.shape[1])
                
    except Exception as e:
        print(f"Explainability feature failed: {e}")
        contributions = np.zeros(X_processed.shape[1])
            
    # Map the contributions back to the original feature names
    feature_names = input_df.columns.tolist()
    
    feature_contributions = []
    # If the preprocessor generated more/less features (e.g., OHE), we'd need to aggregate,
    # but based on the current 5-feature numerical setup, it maps 1:1.
    for name, contrib in zip(feature_names, contributions):
        feature_contributions.append({
            "feature": name,
            "contribution": float(contrib)
        })
        
    # Sort by absolute contribution descending
    feature_contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
    
    return feature_contributions