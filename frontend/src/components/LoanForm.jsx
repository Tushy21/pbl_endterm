import { useState } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from "recharts";

function LoanForm() {
  const [formData, setFormData] = useState({
    loan_amnt: "",
    annual_inc: "",
    dti: "",
    revol_bal: "",
    total_acc: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const payload = {
        loan_amnt: Number(formData.loan_amnt),
        annual_inc: Number(formData.annual_inc),
        dti: Number(formData.dti),
        revol_bal: Number(formData.revol_bal),
        total_acc: Number(formData.total_acc),
      };

      const [predictRes, explainRes] = await Promise.all([
        axios.post("http://127.0.0.1:8000/predict", payload),
        axios.post("http://127.0.0.1:8000/explain", payload),
      ]);

      setResult({
        ...predictRes.data,
        explanation: explainRes.data.top_contributing_features,
      });
    } catch (err) {
      console.error(err);
      setError("Prediction service unavailable or failed. Check connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="main-market">
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Borrower Profile Market</h2>
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
                <div className="form-group">
                  <label className="form-label">Loan Amount</label>
                  <div className="bet-input-container">
                    <span className="bet-input-prefix">$</span>
                    <input
                      type="number"
                      className="bet-input"
                      name="loan_amnt"
                      placeholder="e.g. 15000"
                      value={formData.loan_amnt}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Annual Income</label>
                  <div className="bet-input-container">
                    <span className="bet-input-prefix">$</span>
                    <input
                      type="number"
                      className="bet-input"
                      name="annual_inc"
                      placeholder="e.g. 75000"
                      value={formData.annual_inc}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Debt-to-Income (DTI)</label>
                  <div className="bet-input-container">
                    <span className="bet-input-prefix">%</span>
                    <input
                      type="number"
                      className="bet-input"
                      name="dti"
                      placeholder="e.g. 15.5"
                      step="0.01"
                      value={formData.dti}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Revolving Balance</label>
                  <div className="bet-input-container">
                    <span className="bet-input-prefix">$</span>
                    <input
                      type="number"
                      className="bet-input"
                      name="revol_bal"
                      placeholder="e.g. 5000"
                      value={formData.revol_bal}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>
              </div>

              <div className="form-group" style={{ marginTop: "24px" }}>
                <label className="form-label">Total Accounts</label>
                <div className="bet-input-container">
                  <span className="bet-input-prefix">#</span>
                  <input
                    type="number"
                    className="bet-input"
                    name="total_acc"
                    placeholder="e.g. 12"
                    value={formData.total_acc}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              {error && <div className="error-message">{error}</div>}

              <div style={{ marginTop: "32px", borderTop: "1px solid var(--border-color)", paddingTop: "24px" }}>
                <button type="submit" className="btn-place-bet" disabled={loading}>
                  {loading ? (
                    <>
                      <span className="spinner" style={{ animation: "spin 1s linear infinite", display: "inline-block" }}>↻</span>
                      Analyzing Odds...
                    </>
                  ) : "Calculate Risk Odds"}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Explainability Chart moves here if result exists */}
        {result && result.explanation && (
          <div className="card" style={{ marginTop: "32px" }}>
            <div className="card-header">
              <h3 className="card-title">Risk Analysis Drivers</h3>
            </div>
            <div className="card-body">
              <div style={{ height: "300px", width: "100%" }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    layout="vertical"
                    data={result.explanation}
                    margin={{ top: 10, right: 30, left: 40, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
                    <XAxis type="number" stroke="#94a3b8" tick={{ fill: '#94a3b8' }} />
                    <YAxis dataKey="feature" type="category" width={100} tick={{ fill: '#94a3b8', fontSize: 12 }} stroke="#94a3b8" />
                    <Tooltip
                      formatter={(value) => value.toFixed(4)}
                      contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc' }}
                      itemStyle={{ color: '#fbbf24' }}
                    />
                    <Bar dataKey="contribution" radius={[0, 4, 4, 0]}>
                      {result.explanation.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.contribution > 0 ? 'var(--accent-red)' : 'var(--accent-green)'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div style={{ display: "flex", gap: "16px", marginTop: "16px", justifyContent: "center", fontSize: "12px", color: "var(--text-muted)" }}>
                <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                  <span style={{ width: "12px", height: "12px", backgroundColor: "var(--accent-red)", display: "inline-block", borderRadius: "2px" }}></span>
                  Increases Risk
                </span>
                <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                  <span style={{ width: "12px", height: "12px", backgroundColor: "var(--accent-green)", display: "inline-block", borderRadius: "2px" }}></span>
                  Decreases Risk
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="bet-slip">
        <div className="card">
          <div className="card-header" style={{ backgroundColor: "var(--accent-green)", color: "#000" }}>
            <h2 className="card-title" style={{ color: "#000", fontWeight: "800" }}>Prediction Slip</h2>
          </div>
          <div className="card-body">
            {!result ? (
              <div style={{ textAlign: "center", padding: "40px 0", color: "var(--text-muted)" }}>
                <p>Enter borrower details</p>
                <p>to see predicted odds.</p>
              </div>
            ) : (
              <div>
                <div className="slip-item">
                  <span className="slip-label">Status Preview</span>
                  <span className={`slip-value ${result.prediction === 1 ? 'danger' : 'success'}`}>
                    {result.prediction === 1 ? "DEFAULT LIKELY" : "CLEARED"}
                  </span>
                </div>
                <div className="slip-item">
                  <span className="slip-label">Risk Category</span>
                  <span className="slip-value" style={{ color: "var(--text-main)" }}>
                    {result.risk_level.toUpperCase()}
                  </span>
                </div>

                <div className="slip-total">
                  <span className="slip-total-label">Default Prob</span>
                  <span className="slip-total-value">
                    {(result.probability_default * 100).toFixed(1)}%
                  </span>
                </div>

                <div style={{ marginTop: "24px", padding: "12px", backgroundColor: "rgba(34, 197, 94, 0.1)", borderRadius: "6px", textAlign: "center", fontSize: "12px", color: "var(--accent-green)" }}>
                  Odds calculated successfully
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default LoanForm;

