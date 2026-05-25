const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";

export const ANGEL_INTENTS = [
  { slug: "love", displayName: "Love & Relationships" },
  { slug: "career", displayName: "Career & Money" },
  { slug: "twin-flame", displayName: "Twin Flame" },
  { slug: "manifestation", displayName: "Manifestation" },
  { slug: "health", displayName: "Health & Wellbeing" },
  { slug: "spiritual-growth", displayName: "Spiritual Growth" },
  { slug: "family", displayName: "Family & Home" },
  { slug: "protection", displayName: "Protection & Guidance" },
  { slug: "new-beginnings", displayName: "New Beginnings" },
];

async function requestJson(path, signal) {
  const response = await fetch(`${BACKEND_URL}${path}`, { signal });
  if (!response.ok) {
    const error = new Error(`Request failed with ${response.status}`);
    error.status = response.status;
    throw error;
  }
  return response.json();
}

export function fetchAngelHub(signal) {
  return requestJson("/api/seo/angel-numbers/hub", signal);
}

export function fetchAngelNumber(number, signal) {
  return requestJson(`/api/seo/angel-numbers/${number}`, signal);
}

export function fetchAngelIntent(number, intent, signal) {
  return requestJson(`/api/seo/angel-numbers/${number}/${intent}`, signal);
}

export function normaliseAngelSearchInput(raw) {
  const digits = `${raw || ""}`.replace(/\D/g, "");
  if (!digits) return null;
  const normalised = String(Number.parseInt(digits, 10));
  if (!normalised || Number.isNaN(Number(normalised))) return null;
  const value = Number(normalised);
  if (value < 1 || value > 10000) return null;
  return normalised;
}
