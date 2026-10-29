export const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

// Turn {vendor: "DHL", category: ""} into "?vendor=DHL" (empty values are skipped)
function toQueryString(filters) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.append(key, value);
  });
  const text = params.toString();
  return text ? `?${text}` : "";
}

export async function getJson(path, filters = {}) {
  const response = await fetch(`${API_URL}${path}${toQueryString(filters)}`);
  if (!response.ok) {
    throw new Error(`API returned ${response.status}`);
  }
  return response.json();
}