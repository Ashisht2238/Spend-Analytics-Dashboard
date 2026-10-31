const money = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const whole = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });

function AnomalyTable({ orders }) {
  return (
    <section className="table-card">
      {orders.length === 0 ? (
        <p className="chart-empty">No unusual orders for these filters.</p>
      ) : (
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>PO number</th>
                <th>Date</th>
                <th>Vendor</th>
                <th>Category</th>
                <th>Item</th>
                <th className="num">Quantity</th>
                <th className="num">Unit price</th>
                <th className="num">Total</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.po_number}>
                  <td>{order.po_number}</td>
                  <td>{order.po_date}</td>
                  <td>{order.vendor}</td>
                  <td>{order.category}</td>
                  <td>{order.item}</td>
                  <td className="num">{whole.format(order.quantity)}</td>
                  <td className="num">{money.format(order.unit_price)}</td>
                  <td className="num">{money.format(order.total_amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default AnomalyTable;