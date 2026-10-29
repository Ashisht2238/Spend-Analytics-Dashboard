function SelectFilter({ label, name, choices, value, onUpdate }) {
  return (
    <label className="filter">
      <span>{label}</span>
      <select value={value} onChange={(event) => onUpdate(name, event.target.value)}>
        <option value="">All</option>
        {choices.map((choice) => (
          <option key={choice} value={choice}>
            {choice}
          </option>
        ))}
      </select>
    </label>
  );
}

function DateFilter({ label, name, value, min, max, onUpdate }) {
  return (
    <label className="filter">
      <span>{label}</span>
      <input
        type="date"
        value={value}
        min={min}
        max={max}
        onChange={(event) => onUpdate(name, event.target.value)}
      />
    </label>
  );
}

function FilterBar({ options, filters, onChange, onReset }) {
  // Make a copy of the filters with just one value changed.
  function update(name, value) {
    onChange({ ...filters, [name]: value });
  }

  return (
    <section className="filters">
      <SelectFilter label="Vendor" name="vendor" choices={options.vendors}
        value={filters.vendor} onUpdate={update} />
      <SelectFilter label="Category" name="category" choices={options.categories}
        value={filters.category} onUpdate={update} />
      <SelectFilter label="Department" name="department" choices={options.departments}
        value={filters.department} onUpdate={update} />
      <SelectFilter label="Status" name="status" choices={options.statuses}
        value={filters.status} onUpdate={update} />
       <DateFilter label="From" name="start_date" value={filters.start_date}
        min={options.min_date} max={filters.end_date || options.max_date} onUpdate={update} />
       <DateFilter label="To" name="end_date" value={filters.end_date}
        min={filters.start_date || options.min_date} max={options.max_date} onUpdate={update} />
       <button className="reset-button" onClick={onReset}>Reset</button>
    </section>
  );
}

export default FilterBar;