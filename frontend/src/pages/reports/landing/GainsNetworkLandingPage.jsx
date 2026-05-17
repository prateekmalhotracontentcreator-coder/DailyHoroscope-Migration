import React from 'react';
import ReportLandingPageShell from './ReportLandingPageShell';
import { REPORT_LANDING_CONTENT } from './reportLandingContent';

export default function GainsNetworkLandingPage() {
  return <ReportLandingPageShell page={REPORT_LANDING_CONTENT['gains-network-report']} />;
}
