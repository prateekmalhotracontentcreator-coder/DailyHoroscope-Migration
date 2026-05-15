import React from 'react';
import ReportLandingPageShell from './ReportLandingPageShell';
import { REPORT_LANDING_CONTENT } from './reportLandingContent';

export default function LifeCyclesLandingPage() {
  return <ReportLandingPageShell page={REPORT_LANDING_CONTENT['life-cycles']} />;
}
