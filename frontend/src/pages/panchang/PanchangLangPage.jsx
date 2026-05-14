/**
 * PanchangLangPage — thin wrapper that renders PanchangPage with a language prop.
 * All layout, sub-nav, and data fetching lives in PanchangPage; labels are translated there.
 */
import React from 'react';
import { PanchangPage } from './PanchangPage';

export function PanchangLangPage({ lang }) {
  return <PanchangPage lang={lang} />;
}

export default PanchangLangPage;
