const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

async function requestJson(path, options = {}) {
  const response = await fetch(`${BACKEND_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let detail = `Request failed with ${response.status}`;
    try {
      const payload = await response.json();
      detail = payload?.detail || detail;
    } catch {
      // Keep the generic detail when the backend does not return JSON.
    }
    const error = new Error(detail);
    error.status = response.status;
    throw error;
  }

  return response.json();
}

export function fetchCategories(signal) {
  return requestJson("/api/auspicious/categories", { signal });
}

export function calculateMonth(payload, signal) {
  return requestJson("/api/auspicious/calculate-month", {
    method: "POST",
    body: JSON.stringify(payload),
    signal,
  });
}

export function fetchTopDays(params, signal) {
  const search = new URLSearchParams();
  Object.entries(params || {}).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") return;
    search.set(key, String(value));
  });
  return requestJson(`/api/auspicious/top-days?${search.toString()}`, { signal });
}
