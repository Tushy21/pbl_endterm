import React from "react";

function ResultCard({ result }) {
  return (
    <div style={{ marginTop: "40px", padding: "20px", border: "1px solid #ccc" }}>
      <h2>Prediction Result</h2>

      <p>
        Probability of Default:{" "}
        {(result.probability_default * 100).toFixed(2)}%
      </p>

      <p>Prediction: {result.prediction}</p>

      <p>Risk Level: {result.risk_level}</p>
    </div>
  );
}

export default ResultCard;

