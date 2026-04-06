import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function flattenLocationGroups(groups) {
  return (groups || []).flatMap((group) =>
    (group.locations || []).map((location) => ({
      ...location,
      country_code: group.country_code,
      country_name: group.country_name,
      search_text: [
        location.city_name,
        location.country,
        location.country_name,
        location.label,
        location.timezone,
        location.tz_abbr,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase(),
    })),
  );
}

function SharedBirthCityPicker({
  inputId = "birth-location",
  label = "Birth Location",
  placeholder = "Search city, country, or timezone",
  value = "",
  onChange,
  required = false,
  disabled = false,
  wrapperStyle,
  labelStyle,
  inputStyle,
  selectStyle,
  helpText,
}) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [locationGroups, setLocationGroups] = useState([]);

  useEffect(() => {
    let active = true;
    async function loadLocations() {
      setLoading(true);
      setError("");
      try {
        const res = await axios.get(`${API}/panchang/locations/grouped`);
        if (!active) return;
        setLocationGroups(res.data?.groups || []);
      } catch (err) {
        if (!active) return;
        setError(err?.response?.data?.detail || "Unable to load city catalogue.");
      } finally {
        if (active) setLoading(false);
      }
    }
    loadLocations();
    return () => {
      active = false;
    };
  }, []);

  const flatOptions = useMemo(() => flattenLocationGroups(locationGroups), [locationGroups]);

  const filteredOptions = useMemo(() => {
    if (!search.trim()) return flatOptions;
    const needle = search.trim().toLowerCase();
    return flatOptions.filter((item) => item.search_text.includes(needle));
  }, [flatOptions, search]);

  const selectedOption = flatOptions.find((item) => item.slug === value) || null;

  return (
    <div style={wrapperStyle}>
      <label htmlFor={inputId} style={labelStyle}>
        {label}
      </label>
      <input
        id={`${inputId}-search`}
        type="text"
        placeholder={placeholder}
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        disabled={disabled || loading}
        style={{ marginTop: 8, ...(inputStyle || {}) }}
      />
      <select
        id={inputId}
        value={value}
        onChange={(event) => {
          const next = flatOptions.find((item) => item.slug === event.target.value);
          if (next && onChange) {
            onChange(next);
          }
        }}
        disabled={disabled || loading}
        required={required}
        style={{ marginTop: 10, ...(selectStyle || inputStyle || {}) }}
      >
        <option value="">
          {loading ? "Loading city catalogue..." : "Select a city"}
        </option>
        {filteredOptions.slice(0, 200).map((item) => (
          <option key={item.slug} value={item.slug}>
            {item.city_name || item.label} | {item.country || item.country_name} | {item.tz_abbr || item.timezone}
          </option>
        ))}
      </select>
      {selectedOption ? (
        <p style={{ marginTop: 8, fontSize: 13, opacity: 0.8 }}>
          Selected: {selectedOption.city_name}, {selectedOption.country} ({selectedOption.timezone})
        </p>
      ) : null}
      {helpText ? <p style={{ marginTop: 8, fontSize: 13, opacity: 0.75 }}>{helpText}</p> : null}
      {error ? <p style={{ marginTop: 8, color: "#a43b17" }}>{error}</p> : null}
    </div>
  );
}

export default SharedBirthCityPicker;
