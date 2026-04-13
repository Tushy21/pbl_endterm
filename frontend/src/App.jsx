import LoanForm from "./components/LoanForm";
import "./App.css";

function App() {
  return (
    <div className="app-layout">
      {/* Top Navigation */}
      <nav className="top-nav">
        <div className="nav-brand">RiskPred Sportsbook</div>
        <div className="nav-links">
          <a href="#">Markets</a>
          <a href="#">Live Betting</a>
          <a href="#">Promotions</a>
          <a
            href="https://github.com/Tushy21/pbl_project"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "var(--accent-green)", fontWeight: "bold" }}
          >
            GitHub repo
          </a>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="main-content">
        <div className="betting-layout">
          {/* Main Market / Form Area */}
          <div className="main-market">
            <LoanForm />
          </div>

          {/* Right Column is where the Bet Slip (Results) will go, handled partially in LoanForm now, or we can structure it there. */}
          {/* We will let LoanForm handle the grid layout for its own internal slip, but for now we'll rely on it returning both sides or we can move state up. */}
          {/* If LoanForm handles both, we just render LoanForm. Let's assume LoanForm will be a self-contained component that uses the grid. */}
        </div>
      </main>
    </div>
  );
}

export default App;
