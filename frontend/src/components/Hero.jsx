function Hero() {
  return (
    <div style={styles.hero}>
      <h1>Credit Risk Prediction System</h1>
      <p>
        Machine Learning powered loan default prediction with SHAP
        explainability.
      </p>
    </div>
  );
}

const styles = {
  hero: {
    textAlign: "center",
    padding: "40px",
    background: "#e0e1dd",
  },
};

export default Hero;
