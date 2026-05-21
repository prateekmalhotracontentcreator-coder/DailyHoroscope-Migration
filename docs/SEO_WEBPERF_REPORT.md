# SEO Web Performance Report

Date: 2026-05-22
Scope: SEO-20K M1

## Summary

This milestone focused on foundational SEO infrastructure for the current React and FastAPI architecture, plus the first two programmatic page groups:

- City Panchang pages
- Regional Choghadiya pages
- Dynamic XML sitemap plumbing
- Canonical and hreflang support in the shared SEO component
- Vercel route-level caching headers for key programmatic routes

## Implemented in M1

### Shared SEO infrastructure

- Extended `frontend/src/components/SEO.jsx` with:
  - `canonical`
  - `hreflang`
  - `jsonLd`
- Preserved backward compatibility with the existing `url` and `schema` props.

### Sitemap infrastructure

- Added backend-served dynamic sitemap endpoints:
  - `/api/seo/sitemap/panchang`
  - `/api/seo/sitemap/choghadiya`
  - `/api/seo/sitemap/horoscope`
- Added `frontend/public/sitemap-index.xml`
- Updated `frontend/public/robots.txt` to point to `sitemap-index.xml`

### Cache policy

- Added route-specific `Cache-Control` headers in `frontend/vercel.json` for:
  - `/panchang/:citySlug/:date`
  - `/choghadiya/:citySlug/:period`
  - `/horoscope/:sign/tomorrow`
  - `/horoscope/:sign/weekly`
  - `/horoscope/:sign/monthly`

### Programmatic page delivery

- Added `CityPanchangPage.jsx`
- Added `ChoghadiyaPage.jsx`
- Wired both into `App.js`

## Lighthouse baseline

An automated Lighthouse baseline was not captured inside this coding session because no local browser audit pipeline was already configured in the repo, and M1 was implemented primarily as code and route infrastructure. The next recommended step is to run Lighthouse on:

- `/`
- `/panchang/new-delhi-india/2026-05-22`
- `/choghadiya/new-delhi-india/today`
- `/horoscope/aries/tomorrow`

Recommended metrics to record:

- LCP
- CLS
- INP
- SEO score
- Structured data warnings

## Remaining M1 follow-up checks

- Confirm `sitemap-index.xml` is referenced in production robots.txt after deploy
- Confirm Render exposes the three sitemap endpoints with `application/xml`
- Smoke-test canonical tags and hreflang tags on the new programmatic routes
- Spot-check cache headers on Vercel once deployed

## Notes

- The current architecture remains client-rendered React, so this milestone improves discoverability and metadata consistency but does not introduce SSR or static prerendering.
- Future M2 and M3 sitemap endpoints should be added to `sitemap-index.xml` only when those route groups are live.
