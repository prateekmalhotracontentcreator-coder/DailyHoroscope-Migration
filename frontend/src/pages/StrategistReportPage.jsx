import React, { useState } from 'react';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

export default function StrategistReportPage() {
  const [loading, setLoading] = useState(false);
  const [reportHtml, setReportHtml] = useState('');
  const token = localStorage.getItem('token') || '';

  const generateReport = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${BACKEND}/api/strategist/report/pdf`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const html = await res.text();
      setReportHtml(html);
    } catch {
      setReportHtml('<p style="color:red">Report generation failed. Complete LK Onboarding first.</p>');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground px-4 py-8 max-w-3xl mx-auto">
      <div className="rounded-xl border border-gold/30 bg-gradient-to-br from-gold/15 to-gold/5 shadow-sm p-5 mb-5">
        <h1 className="text-xl font-bold text-gold mb-1">Executive Intelligence Brief</h1>
        <p className="text-sm text-muted-foreground mb-4">
          Premium report: Conquest Probability, Active Missions, Remedy Roadmap, and 43-Day Forecast.
        </p>
        <button
          onClick={generateReport}
          disabled={loading}
          className="bg-gold text-background font-semibold rounded-lg px-5 py-2.5 disabled:opacity-50"
        >
          {loading ? 'Generating…' : 'Generate Intelligence Brief'}
        </button>
      </div>

      {reportHtml && (
        <div className="rounded-xl border border-gold/20 bg-card shadow-sm overflow-hidden">
          <iframe
            srcDoc={reportHtml}
            title="Executive Intelligence Brief"
            className="w-full min-h-[600px] border-0"
            sandbox="allow-same-origin"
          />
        </div>
      )}
    </div>
  );
}
