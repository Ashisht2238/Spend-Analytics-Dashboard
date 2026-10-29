const formatNumber = (value) =>
  value.toLocaleString(undefined, { maximumFractionDigits: 0 });

function KpiCards({ summary }) {
  const cards = [
    { label: "Total spend", value: formatNumber(summary.total_spend) },
    { label: "Orders", value: formatNumber(summary.orders) },
    { label: "Vendors", value: formatNumber(summary.vendors) },
    { label: "Flagged orders", value: formatNumber(summary.flagged_orders), highlight: true },
  ];

  return (
    <section className="kpi-grid">
      {cards.map((card) => (
        <div
          key={card.label}
          className={card.highlight ? "kpi-card kpi-flagged" : "kpi-card"}
        >
          <span className="kpi-label">{card.label}</span>
          <span className="kpi-value">{card.value}</span>
        </div>
      ))}
    </section>
  );
}

export default KpiCards;