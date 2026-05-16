import React from 'react';
import ReportLandingPageShell from './ReportLandingPageShell';
import { REPORT_LANDING_CONTENT } from './reportLandingContent';

export default function SoulmateLandingPage() {
  return <ReportLandingPageShell page={REPORT_LANDING_CONTENT['soulmate-timing-report']} />;
}
