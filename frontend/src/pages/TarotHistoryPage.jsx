import React, { useEffect, useState } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function TarotHistoryPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [items, setItems] = useState([]);
  const [filters, setFilters] = useState({ bookmarked: false });
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  useEffect(() => {
    let active = true;
    async function loadHistory() {
      setLoading(true);
      setError("");
      try {
        const params = { page, limit: 10 };
        if (filters.bookmarked) params.bookmarked = true;
        const res = await axios.get(`${API}/tarot/history`, {
          params,
          withCredentials: true,
        });
        if (!active) return;
        setItems(res.data?.items || []);
        setHasMore(Boolean(res.data?.has_more));
      } catch (err) {
        if (!active) return;
        setError(err?.response?.data?.detail || "Unable to load your tarot archive.");
      } finally {
        if (active) setLoading(false);
      }
    }
    loadHistory();
    return () => {
      active = false;
    };
  }, [filters.bookmarked, page]);

  async function toggleBookmark(reportId, bookmarked) {
    try {
      await axios.post(
        `${API}/tarot/bookmark`,
        { report_id: reportId, bookmarked: !bookmarked },
        { withCredentials: true }
      );
      setItems((current) =>
        current
          .map((item) => (item.report_id === reportId ? { ...item, bookmarked: !bookmarked } : item))
          .filter((item) => !filters.bookmarked || item.bookmarked)
      );
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to update bookmark right now.");
    }
  }

  return (
    <div className="tarot-history-page">
      <section className="tarot-history-page__hero">
        <p className="tarot-history-page__eyebrow">Tarot Archive</p>
        <h1>Your sacred reading history</h1>
        <p>Revisit the cards, messages, and moments that shaped your journey.</p>
      </section>

      <section className="tarot-history-page__filters">
        <button
          type="button"
          className={!filters.bookmarked ? "is-active" : ""}
          onClick={() => {
            setPage(1);
            setFilters({ bookmarked: false });
          }}
        >
          All Readings
        </button>
        <button
          type="button"
          className={filters.bookmarked ? "is-active" : ""}
          onClick={() => {
            setPage(1);
            setFilters({ bookmarked: true });
          }}
        >
          Bookmarked
        </button>
      </section>

      {loading ? <div className="tarot-history-page__loading">Opening your archive...</div> : null}
      {error ? <p className="tarot-history-page__error">{error}</p> : null}

      {!loading && !items.length ? (
        <div className="tarot-history-page__empty">Your tarot archive is waiting for its first entry.</div>
      ) : null}

      <div className="tarot-history-page__grid">
        {items.map((item) => (
          <article key={item.id} className="tarot-history-card">
            <div className="tarot-history-card__meta">
              <span>{item.prediction_date}</span>
              <span>{item.focus_area}</span>
              <span>{item.depth_level}</span>
            </div>
            <h2>{item.cards?.[0]?.name || "Daily Tarot Reading"}</h2>
            <p>{item.summary}</p>
            <div className="tarot-history-card__actions">
              <button type="button" onClick={() => toggleBookmark(item.report_id, item.bookmarked)}>
                {item.bookmarked ? "Remove Bookmark" : "Bookmark"}
              </button>
            </div>
          </article>
        ))}
      </div>

      {!loading && hasMore ? (
        <div className="tarot-history-page__pagination">
          <button type="button" onClick={() => setPage((current) => current + 1)}>
            Load More
          </button>
        </div>
      ) : null}
    </div>
  );
}

export default TarotHistoryPage;
