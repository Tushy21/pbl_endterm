import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

function SHAPChart({ data }) {
  return (
    <div style={{ width: "100%", height: 400 }}>
      <h3>Feature Contributions (SHAP)</h3>

      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="feature" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="contribution" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SHAPChart;


