import { useEffect, useState } from "react";
import { getJson } from "./api";
import AnomalyTable from "./components/AnomalyTable";
import FilterBar from "./components/FilterBar";
import KpiCards from "./components/KpiCards";
import SpendChart from "./components/SpendChart";
import SpendLineChart from "./components/SpendLineChart";

const EMPTY_FILTERS = {
  vendor: "",
  category: "",
  department: "",
  status: "",
  start_date: "",
  end_date: "",
};

function App() {
  const [options, setOptions] = useState(null);
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState(null);
  const [attempt, setAttempt] = useState(0); // goes up by 1 each time we retry

  // Load the dropdown choices (again whenever we retry).
  useEffect(() => {
    getJson("/api/filters")
      .then(setOptions)
      .catch((err) => setError(err.message));
  }, [attempt]);

  // Reload everything when a filter changes (or when we retry).
  useEffect(() => {
    let ignore = false;
    Promise.all([
      getJson("/api/summary", filters),
      getJson("/api/spend/vendor", filters),
      getJson("/api/spend/category", filters),
      getJson("/api/spend/monthly", filters),
      getJson("/api/anomalies", filters),
      getJson("/api/forecast", filters),
    ])
      .then(([summary, byVendor, byCategory, byMonth, anomalies, forecast]) => {
        if (!ignore) {
          setDashboard({
            summary,
            byVendor,
            byCategory,
            byMonth,
            anomalies,
            forecast,
            forFilters: filters, // remember which filters this data belongs to
          });
          setError(null);
        }
      })
      .catch((err) => {
        if (!ignore) setError(err.message);
      });
    return () => {
      ignore = true;
    };
  }, [filters, attempt]);

  function retry() {
    setError(null);
    setAttempt((n) => n + 1);
  }

  // Nothing to show yet: either still loading, or the very first load failed.
  if (!options || !dashboard) {
    if (error) {
      return (
        <div className="message">
          <p>Could not load data: {error}</p>
          <button className="reset-button" onClick={retry}>Try again</button>
        </div>
      );
    }
    return <p className="message">Loading...</p>;
  }

  // The data on screen is stale while it belongs to older filters.
  const loading = !error && dashboard.forFilters !== filters;
  const { forecast } = dashboard;
  const forecastTitle = forecast.next_month
    ? `Forecast for ${forecast.next_month}`
    : "Forecast";

  return (
    <div className="page">
      <header className="page-header">
        <h1>Spend Analytics Dashboard</h1>
        <p>Purchase order spend, unusual orders and forecast</p>
      </header>
      {error && (
        <div className="error-banner" role="alert">
          <span>Could not refresh data: {error}</span>
          <button className="reset-button" onClick={retry}>Try again</button>
        </div>
      )}
      <FilterBar
        options={options}
        filters={filters}
        onChange={setFilters}
        onReset={() => setFilters(EMPTY_FILTERS)}
      />
     <div className={loading ? "content is-loading" : "content"} aria-busy={loading}>
        <KpiCards summary={dashboard.summary} />
        <h2 className="section-title">1. Spend Analysis</h2>
        <section className="chart-grid">
          <SpendChart title="Spend by Vendor" data={dashboard.byVendor} labelKey="vendor" horizontal />
          <SpendChart title="Spend by Category" data={dashboard.byCategory} labelKey="category"   /> 
          <SpendLineChart title="Spend by Month" data={dashboard.byMonth} labelKey="month" valueKey="total_spend"/>
        </section>
        <h2 className="section-title">2. Unusual Orders</h2>
        <AnomalyTable orders={dashboard.anomalies} />
        <h2 className="section-title">3. Forecast: Next Month's Spend</h2>
        <SpendChart
              data={forecast.forecast}
              labelKey="category"
              valueKey="forecast_spend"
              valueLabel="Forecast"
              emptyMessage={forecast.message || "No data for these filters."}
            />
      </div>
    </div>
  );
}

export default App;