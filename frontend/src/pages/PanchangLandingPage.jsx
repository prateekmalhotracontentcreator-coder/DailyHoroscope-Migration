import React from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";

import PanchangCosmicMap from "../components/PanchangCosmicMap";
import PanchangLanguageToggle from "../components/PanchangLanguageToggle";
import { buildPanchangPath, getPanchangCopy, getPanchangLanguage } from "../components/panchangLocale";

function PanchangLandingPage() {
  const { lang } = useParams();
  const [searchParams] = useSearchParams();
  const language = getPanchangLanguage(lang);
  const copy = getPanchangCopy(language);
  const locationSlug = searchParams.get("location_slug") || "new-delhi-india";

  return (
    <div className="panchang-page panchang-landing-page">
      {/* Interactive cosmic time-map hero */}
      <PanchangCosmicMap locationSlug={locationSlug} dayOffset={0} />

      {/* Language toggle row */}
      <div className="panchang-shell" style={{ paddingTop: "0.5rem", paddingBottom: "0.5rem" }}>
        <PanchangLanguageToggle />
      </div>

      {/* Hero CTA */}
      <section className="panchang-shell panchang-hero">
        <p className="panchang-eyebrow">{copy.landingEyebrow}</p>
        <h1>{copy.landingTitle}</h1>
        <p>{copy.landingBody}</p>
        <div className="panchang-hero__actions">
          <Link to={buildPanchangPath(language, "/today")} className="panchang-button">
            {copy.ctaToday}
          </Link>
          <Link to={buildPanchangPath(language, "/tomorrow")} className="panchang-button panchang-button--secondary">
            {copy.ctaTomorrow}
          </Link>
          <Link
            to={buildPanchangPath(language, `/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`)}
            className="panchang-button panchang-button--secondary"
          >
            {copy.ctaCalendar}
          </Link>
        </div>
      </section>

      {/* Regional Panchangam cards */}
      <section className="panchang-grid panchang-grid--double">
        <article className="panchang-card">
          <p className="panchang-card__label">Tamil Panchangam</p>
          <h2>Calendar-first Tamil month browsing</h2>
          <p>Explore a Tamil Panchangam surface built for monthly discovery, daily date opening, and Tamil calendar SEO depth.</p>
          <Link
            to={buildPanchangPath("ta", `/tamil-calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`)}
            className="panchang-button panchang-button--secondary"
          >
            Open Tamil Panchangam
          </Link>
        </article>
        <article className="panchang-card">
          <p className="panchang-card__label">Telugu Panchangam</p>
          <h2>Calendar-first Telugu month browsing</h2>
          <p>Open a dedicated Telugu Panchangam month view designed for repeat use, date-level linking, and regional search entry.</p>
          <Link
            to={buildPanchangPath("te", `/telugu-calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`)}
            className="panchang-button panchang-button--secondary"
          >
            Open Telugu Panchangam
          </Link>
        </article>
      </section>

      {/* Utility cards */}
      <section className="panchang-grid panchang-grid--triple">
        <article className="panchang-card">
          <p className="panchang-card__label">Daily Utility</p>
          <h2>Today, tomorrow, and next observances</h2>
          <p>Open the day view for sunrise, sunset, tithi, nakshatra, yoga, karana, and day-quality windows.</p>
          <Link to={buildPanchangPath(language, "/today")} className="panchang-button">
            {copy.ctaToday}
          </Link>
        </article>
        <article className="panchang-card">
          <p className="panchang-card__label">Festival Discovery</p>
          <h2>Browse festival and vrat dates</h2>
          <p>Use the observance hub to move from one festival to exact date pages and monthly calendar views.</p>
          <Link to={buildPanchangPath(language, "/festivals")} className="panchang-button">
            {copy.navFestivals}
          </Link>
        </article>
        <article className="panchang-card">
          <p className="panchang-card__label">Calendar Depth</p>
          <h2>Month-level Hindu calendar navigation</h2>
          <p>Jump by month, browse observance-heavy dates, and use Panchang as a full utility suite instead of a single page.</p>
          <Link to={buildPanchangPath(language, `/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`)} className="panchang-button">
            {copy.navCalendar}
          </Link>
        </article>
      </section>
    </div>
  );
}

export default PanchangLandingPage;
