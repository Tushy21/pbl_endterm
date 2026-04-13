# Credit Risk Prediction Web App

This is a full-stack web application for predicting credit risk based on loan application data, complete with model explainability.

## Project Structure

The project is divided into two main directories:
- `backend/`: A FastAPI backend that serves the credit risk prediction model and provides SHAP-based explainability.
- `frontend/`: A React frontend built with Vite, allowing users to input their data and view predictions alongside visual explanations.

## Features

- **Credit Risk Prediction**: Predicts whether a loan applicant has a High, Medium, or Low risk of default.
- **Model Explainability**: Integrates SHAP (SHapley Additive exPlanations) to explain individual predictions, showing which features contributed most to the model's decision.
- **Interactive UI**: A modern React interface featuring visual charts (via Recharts) to display the SHAP explanations clearly.

## Prerequisites

- Node.js (v18+ recommended)
- Python (3.9+ recommended)

## Setup and Installation

### Backend Setup

1. Navigate to the `backend` directory:
   ```sh
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```sh
   uvicorn src.app:app --reload
   ```
   The backend will start at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```sh
   cd frontend
   ```
2. Install the dependencies:
   ```sh
   npm install
   ```
3. Start the Vite development server:
   ```sh
   npm run dev
   ```
   The frontend will start at `http://localhost:5173`.

## API Endpoints

- `GET /` - Health check endpoint.
- `POST /predict` - Accepts loan application data and returns the calculated probability of default, a boolean prediction, and a risk level classification (High/Medium/Low).
- `POST /explain` - Accepts loan application data and returns the standard prediction probability along with SHAP feature contributions for explainability.
