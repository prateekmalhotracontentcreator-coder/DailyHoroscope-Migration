import React from 'react';
import ReportLandingPageShell from './ReportLandingPageShell';
import { REPORT_LANDING_CONTENT } from './reportLandingContent';

export default function EncounterWindowLandingPage() {
  return <ReportLandingPageShell page={REPORT_LANDING_CONTENT['encounter-window-report']} />;
}
