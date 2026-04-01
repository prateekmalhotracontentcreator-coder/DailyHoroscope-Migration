import React from "react";
import { Link } from "react-router-dom";

function ContinueJourney({ title = "Continue the Journey", bridge, cta, precisionNote }) {
  if (!cta?.label || !cta?.route) {
    return null;
  }

  return (
    <section className="continue-journey">
      <div className="continue-journey__inner">
        <p className="continue-journey__eyebrow">Next Layer</p>
        <h2>{title}</h2>
        {bridge ? <p className="continue-journey__bridge">{bridge}</p> : null}
        <div className="continue-journey__actions">
          <Link to={cta.route} className="continue-journey__cta">
            {cta.label}
          </Link>
          <Link to="/numerology/history" className="continue-journey__secondary">
            View Report History
          </Link>
        </div>
        {precisionNote ? <p className="continue-journey__note">{precisionNote}</p> : null}
      </div>
    </section>
  );
}

export default ContinueJourney;
