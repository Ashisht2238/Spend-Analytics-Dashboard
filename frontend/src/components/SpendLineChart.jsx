import { CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";

const compact = new Intl.NumberFormat("en-US", {
  notation: "compact",
  maximumFractionDigits: 1,
});
const whole = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });

function SpendLineChart({
  title,
  data,
  labelKey = "month",
  valueKey = "total_spend",
  valueLabel = "Spend",
  emptyMessage = "No data for these filters.",
}) {
  return (
    <section className="chart-card chart-wide">
      <h2>{title}</h2>
      {data.length === 0 ? (
        <p className="chart-empty">{emptyMessage}</p>
      ) : (
        <LineChart
          data={data}
          responsive
          width="100%"
          height={300}
          margin={{ top: 8, right: 16, bottom: 8, left: 8 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={labelKey} />
          <YAxis tickFormatter={(value) => compact.format(value)} width={50} />
          <Tooltip formatter={(value) => whole.format(value)} />
          <Line
            type="linear"
            dataKey={valueKey}
            name={valueLabel}
            stroke="green"
            strokeWidth={2}
            dot
          />
        </LineChart>
      )}
    </section>
  );
}

export default SpendLineChart;