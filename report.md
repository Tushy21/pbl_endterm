# Credit Risk Prediction Using Explainable Machine Learning

**A University Project Report**

---

## Abstract
Credit risk assessment is a critical function for financial institutions to minimize potential defaults and manage financial portfolios effectively. Traditional credit scoring systems, although functional, often lack the nuanced predictive capabilities of modern machine learning techniques and can act as "black-box" systems, failing to provide transparency in their decision-making. This project presents a full-stack web application for credit risk prediction, integrating robust machine learning models with human-readable explainability. leveraging Logistic Regression, Random Forest, and XGBoost classifiers, the system predicts the probability of a loan default based on a subset of carefully selected applicant features. The backend is powered by FastAPI, ensuring high-performance API endpoints, while a responsive React frontend utilizing Vite and Recharts provides an interactive user interface. Furthermore, the application integrates SHAP (SHapley Additive exPlanations) to ensure the predictions are explainable and transparent, giving insights into individual feature contributions for every application. 

---

## 1. Introduction
The financial services industry is increasingly adopting artificial intelligence and machine learning to improve the accuracy and efficiency of credit lending processes. The fundamental problem in lending is predicting whether a potential borrower is likely to default on their loan obligation. A highly accurate prediction model allows banks to adjust interest rates, deny high-risk applications, and manage capital reserves.

However, as models become more complex (e.g., ensemble trees like Random Forest and XGBoost), they also become opaque. Regulatory requirements heavily mandate transparency when denying credit to applicants, making the integration of Explainable Artificial Intelligence (XAI) indispensable. 

### 1.1 Objectives
The primary objectives of this project are:
1. To develop a robust machine learning pipeline capable of classifying credit risk applications into low, medium, and high-risk categories based on underlying probabilities.
2. To provide model interpretability via SHAP values, ensuring that domain experts and applicants can understand the driving factors behind a credit classification.
3. To deploy the trained model in an accessible, fast, and scalable full-stack web application structure (React + FastAPI).

---

## 2. Dataset and Feature Engineering
A critical aspect of developing an accurate classification model is the quality and relevance of the data provided to the algorithm.

### 2.1 Dataset Overview
The dataset contains large volumes of historical loan data (approx. 1.6 GB), encapsulating a variety of borrower characteristics and the final loan outcome (default or fully paid). Given the high dimensionality of financial datasets, filtering down to the most influential predictors prevents the curse of dimensionality and allows the model to generalize better.

### 2.2 Feature Selection
Through rigorous exploratory data analysis, the following five prominent continuous features were selected as the primary independent variables:
- **`loan_amnt`**: The total requested value of the loan. High loan amounts generally correlate with a higher baseline risk depending on the borrower's income.
- **`annual_inc`**: The self-reported annual income of the borrower. This acts as a stabilizer against the loan amount.
- **`dti` (Debt-to-Income Ratio)**: A crucial metric calculating the monthly debt payments divided by monthly gross income. Extremely high DTIs indicate borrowers stretched too thin financial-wise.
- **`revol_bal`**: The total credit revolving balance (e.g., credit card debt). 
- **`total_acc`**: The total number of credit lines currently in the borrower's file.

### 2.3 Preprocessing Pipeline
To guarantee consistent transformations during training and inference time, a `scikit-learn` pipeline was established:
- **Handling Missing Values**: Imputations are applied to prevent missing values from halting the pipeline, commonly utilizing median strategies for continuous variables to limit the impact of outliers.
- **Feature Scaling**: Algorithms such as Logistic Regression and XGBoost are sensitive to feature scales. Standardization techniques (Z-score normalization) are seamlessly integrated into the automated preprocessing pipeline.
- **Serialization**: The entire combined schema of preprocessors and estimators is exported via `joblib` (`pipeline.joblib`), assuring zero data leakage or offset distributions in the production environment.

---

## 3. Machine Learning Methodology
For robust credit risk evaluation, multiple state-of-the-art algorithms form the core model experimentation phase before the best-performing iteration is selected.

### 3.1 Model Architectures
1. **Logistic Regression:** Used as the baseline model. It applies the logistic sigmoid function to a linear combination of features to output a probability between 0 and 1. To account for the inherently imbalanced nature of default scenarios, class weights are kept perfectly balanced (`class_weight='balanced'`).
2. **Random Forest Classifier:** An ensemble learning method constructing a multitude of decision trees at training time. By bagging trees of different depth configurations (`max_depth=10`, `n_estimators=100`) it naturally suppresses overfitting tendencies and handles slightly non-linear relationships expertly.
3. **XGBoost (Extreme Gradient Boosting):** The strongest contender for this project, utilizing decision tree ensembles pushed through gradient descent frameworks. Specific hyperparameters (`learning_rate=0.1`, `max_depth=6`, `scale_pos_weight=3`) were chosen to specifically penalize false predictions toward the minority class (the defaulters).

### 3.2 Explainable AI Integration (SHAP)
Predictive power alone is insufficient for modern credit assessment tools. SHAP (SHapley Additive exPlanations), derived from cooperative game theory, computes the marginal contribution of a specific feature value to the final prediction, relative to a foundational baseline. 

Our explicit integration dynamically matches the correct explainer (`TreeExplainer` or `LinearExplainer`) with the loaded model and pushes out individualized feature weight lists dynamically. The API provides this directly as an end-user consumable JSON payload.

---

## 4. System Architecture
The application translates complex backend Python mechanics into an accessible user interface through a tightly decoupled modern web stack.

### 4.1 Backend Engine (FastAPI)
- **Framework:** FastAPI was elected over traditional counterparts like Flask or Django due to its asynchronous support out-of-the-box and extremely fast runtime driven by Starlette and Pydantic.
- **Endpoints:**
  - `GET /`: Health check route to verify Docker or local system uptime.
  - `POST /predict`: Handles incoming `LoanApplication` schema payloads, runs `transform` across the preprocessing engine, calls `model.predict_proba()`, and dynamically maps outputs to categorical risk brackets (High if $>0.15$, Medium if $>0.08$, else Low).
  - `POST /explain`: Executes the prediction mapping while additionally wrapping the payload inside the `get_explanation()` SHAP wrapper, sorting features by their absolute contributions in real-time.

### 4.2 Frontend Engine (React + Vite)
- **Framework:** The user-facing dashboard is constructed via React 19 natively compiled by Vite, providing instantaneous Hot Module Replacement (HMR).
- **Communication:** Axios is utilized to orchestrate the RESTful API commands connecting with `localhost:8000`. 
- **Data Visualization:** Raw numbers generated by SHAP are abstract for average users. `Recharts` is employed to translate `FeatureContribution` arrays directly into intuitive, visually appealing horizontal bar charts, mapping exactly which feature drove the user's risk rating towards rejection or approval.

---

## 5. Model Evaluation and Results
Credit defaults are substantially rarer than successful repayments. Therefore, evaluating precision (proportion of true defaults correctly identified among all predicted defaults) and recall (proportion of actual defaults detected) via rigorous statistical measurements takes precedence over nominal accuracy.

### 5.1 Evaluation Metrics
The framework evaluated Logistic Regression, Random Forest, and XGBoost using:
- **Precision, Recall, F1-Score**: Particularly optimized for the minority positive class.
- **ROC-AUC (Receiver Operating Characteristic - Area Under Curve)**: The ultimate arbiter for binary classifiers ranking prediction probabilities. The model displaying the highest structural AUC was preserved and explicitly serialized into `/artifacts/pipeline.joblib`. 

---

## 6. Challenges and Discussion
Implementing the credit risk prediction utility posed several challenges:
1. **Class Imbalance**: Defaulted loans consistently represent a fraction of total datasets. Without parameter recalibration (`scale_pos_weight`, `balanced` classes), models inherently collapsed to single-class prediction behavior (always predicting 'Low Risk').
2. **Computational Overhead with Explainability**: Native SHAP tree integrations are fast, but running exact calculation values required matrix denormalization. The structural code in `explainer.py` was refined to differentiate tree calculations smoothly avoiding memory leakage or overhead spikes.

---

## 7. Conclusion
This project successfully bridged the gap between highly structural statistical learning and intuitive UI/UX design. Through the careful pipeline assembly of preprocessing frameworks, advanced ensemble classifiers (XGBoost/Random Forest), and game-theory-driven explainability (SHAP), the proposed architecture demonstrates a capable and regulatory-compliant framework. Integrating this through a decoupled React-FastAPI interaction ensures it serves as an excellent foundational structure for scaled institutional deployment.

---

## 8. References
1. FastAPI Framework Documentation. *Tiangolo*. https://fastapi.tiangolo.com/
2. Lundberg, S. M., & Lee, S. I. (2017). *A Unified Approach to Interpreting Model Predictions*. Advances in Neural Information Processing Systems (NIPS).
3. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*.
4. React Documentation. *Meta Open Source*. https://react.dev/
5. Chen, T., & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System*. Proceedings of the 22nd ACM SIGKDD International Conference.
