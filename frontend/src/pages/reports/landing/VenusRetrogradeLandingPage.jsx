import React from 'react';
import ReportLandingPageShell from './ReportLandingPageShell';
import { REPORT_LANDING_CONTENT } from './reportLandingContent';

export default function VenusRetrogradeLandingPage() {
  return <ReportLandingPageShell page={REPORT_LANDING_CONTENT['venus-retrograde-report']} />;
}
