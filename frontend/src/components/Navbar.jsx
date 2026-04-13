function Navbar() {
  return (
    <div style={styles.nav}>
      <div style={styles.logo}>Credit Risk ML System</div>
    </div>
  );
}

const styles = {
  nav: {
    background: "#0d1b2a",
    color: "white",
    padding: "15px",
    fontSize: "20px",
    fontWeight: "bold",
  },
  logo: {
    textAlign: "center",
  },
};

export default Navbar;
