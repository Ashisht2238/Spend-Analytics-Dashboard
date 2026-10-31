import { Bar, BarChart, CartesianGrid, Tooltip, XAxis, YAxis } from "recharts";

const compact = new Intl.NumberFormat("en-US", {
  notation: "compact",
  maximumFractionDigits: 1,
});
const whole = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });

function SpendChart({
  title,
  data,
  labelKey,
  horizontal = false,
  wide = false,
  valueKey = "total_spend",
  valueLabel = "Spend",
  emptyMessage = "No data for these filters.",
  note = null,
}) {
  const className = wide ? "chart-card chart-wide" : "chart-card";
  const height = horizontal ? Math.max(240, data.length * 32 + 40) : 615;

  return (
    <section className={className}>
      <h2>{title}</h2>
      {data.length === 0 ? (
        <p className="chart-empty">{emptyMessage}</p>
      ) : (
        <BarChart
          data={data}
          layout={horizontal ? "vertical" : "horizontal"}
          responsive
          width="100%"
          height={height}
          margin={{ top: 8, right: 16, bottom: 8, left: 8 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          {horizontal ? (
            <>
              <XAxis type="number" tickFormatter={(value) => compact.format(value)} />
              <YAxis type="category" dataKey={labelKey} width={130} interval={0} />
            </>
          ) : (
            <>
              <XAxis dataKey={labelKey} />
              <YAxis tickFormatter={(value) => compact.format(value)} width={25} />
            </>
          )}
          <Tooltip formatter={(value) => whole.format(value)} />
          <Bar dataKey={valueKey} name={valueLabel} fill="#2f5bea" barSize={50} />
        </BarChart>
      )}
      {note && <p className="chart-note">{note}</p>}
    </section>
  );
}

export default SpendChart;