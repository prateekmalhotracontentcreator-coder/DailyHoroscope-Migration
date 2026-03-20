import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Footer } from '../components/Footer';
import {
  Star, Heart, Crown, Download, ArrowRight,
  FileText, Sparkles, Clock, RefreshCw
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// ─── Report type config ───────────────────────────────────────────────────────
const REPORT_CONFIG = {
  birth_chart: {
    icon: Star,
    color: 'text-gold',
    bg: 'bg-gold/10',
    border: 'border-gold/30',
    label: 'Birth Chart',
    path: (r) => '/birth-chart',
    pdfPath: (r) => `${API}/birthchart/${r.profile_id}/pdf`,
    filename: (r) => `Birth_Chart_Report_${r.name?.replace(/\s+/g,'_')}.pdf`,
  },
  kundali_milan: {
    icon: Heart,
    color: 'text-pink-500',
    bg: 'bg-pink-500/10',
    border: 'border-pink-500/20',
    label: 'Kundali Milan',
    path: (r) => '/kundali-milan',
    pdfPath: (r) => `${API}/kundali-milan/${r.id}/pdf`,
    filename: (r) => `Kundali_Milan_Report_${r.name?.replace(/\s+/g,'_').replace(/&/g,'and')}.pdf`,
  },
  brihat_kundli: {
    icon: Crown,
    color: 'text-purple-500',
    bg: 'bg-purple-500/10',
    border: 'border-purple-500/20',
    label: 'Brihat Kundli Pro',
    path: (r) => '/brihat-kundli',
    pdfPath: (r) => `${API}/brihat-kundli/${r.id}/pdf`,
    filename: (r) => `Brihat_Kundli_Pro_${r.name?.replace(/\s+/g,'_')}.pdf`,
  },
};

// ─── Single report card ───────────────────────────────────────────────────────
const ReportCard = ({ report, onDownload, onView }) => {
  const config = REPORT_CONFIG[report.type];
  if (!config) return null;
  const Icon = config.icon;

  const formattedDate = report.generated_at
    ? new Date(report.generated_at).toLocaleDateString('en-IN', {
        day: 'numeric', month: 'short', year: 'numeric'
      })
    : '—';

  return (
    <Card className={`p-5 border ${config.border} hover:shadow-md transition-shadow`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1 min-w-0">
          {/* Icon */}
          <div className={`${config.bg} rounded-sm p-2.5 flex-shrink-0`}>
            <Icon className={`h-5 w-5 ${config.color}`} />
          </div>

          {/* Details */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap mb-0.5">
              <span className={`text-xs font-semibold uppercase tracking-wider ${config.color}`}>
                {config.label}
              </span>
            </div>
            <h3 className="font-playfair font-semibold text-base truncate">{report.name}</h3>
            <p className="text-xs text-muted-foreground mt-0.5">{report.subtitle}</p>

            {/* Meta pills */}
            <div className="flex items-center gap-2 mt-2 flex-wrap">
              <span className="inline-flex items-center gap-1 text-xs text-muted-foreground">
                <Clock className="h-3 w-3" />
                {formattedDate}
              </span>
              {report.type === 'birth_chart' && report.lagna?.sign && (
                <span className="text-xs bg-muted px-2 py-0.5 rounded-full">
                  {report.lagna.sign_vedic || report.lagna.sign}
                </span>
              )}
              {report.type === 'birth_chart' && report.nakshatra?.name && (
                <span className="text-xs bg-muted px-2 py-0.5 rounded-full">
                  {report.nakshatra.name}
                </span>
              )}
              {report.type === 'kundali_milan' && (
                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                  report.compatibility_score >= 28 ? 'bg-green-500/10 text-green-600 dark:text-green-400'
                  : report.compatibility_score >= 18 ? 'bg-amber-500/10 text-amber-600'
                  : 'bg-red-500/10 text-red-500'
                }`}>
                  {report.compatibility_score}/36
                </span>
              )}
              {report.type === 'brihat_kundli' && report.current_dasha?.mahadasha && (
                <span className="text-xs bg-muted px-2 py-0.5 rounded-full">
                  {report.current_dasha.mahadasha} Dasha
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-2 flex-shrink-0">
          <Button
            size="sm"
            variant="outline"
            className="gap-1.5 border-gold/40 hover:border-gold hover:bg-gold/10 text-xs"
            onClick={() => onDownload(report, config)}
          >
            <Download className="h-3.5 w-3.5" />
            PDF
          </Button>
          <Button
            size="sm"
            variant="ghost"
            className="gap-1.5 text-xs"
            onClick={() => onView(report, config)}
          >
            View
            <ArrowRight className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>
    </Card>
  );
};

// ─── Empty state ──────────────────────────────────────────────────────────────
const EmptyState = ({ navigate }) => (
  <Card className="p-12 text-center border border-border">
    <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
    <h3 className="font-playfair font-semibold text-xl mb-2">No reports yet</h3>
    <p className="text-muted-foreground text-sm mb-6 max-w-sm mx-auto">
      Generate your first Vedic astrology report to see it saved here for easy access.
    </p>
    <div className="flex flex-col sm:flex-row gap-3 justify-center">
      <Button onClick={() => navigate('/birth-chart')}
        className="bg-gold hover:bg-gold/90 text-primary-foreground gap-2">
        <Star className="h-4 w-4" /> Birth Chart
      </Button>
      <Button onClick={() => navigate('/kundali-milan')} variant="outline" className="gap-2 border-gold/40">
        <Heart className="h-4 w-4" /> Kundali Milan
      </Button>
      <Button onClick={() => navigate('/brihat-kundli')} variant="outline" className="gap-2 border-gold/40">
        <Crown className="h-4 w-4" /> Brihat Kundli Pro
      </Button>
    </div>
  </Card>
);

// ─── Main page ────────────────────────────────────────────────────────────────
export const MyReportsPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    if (user?.email) fetchReports();
  }, [user]);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/my-reports`, {
        params: { user_email: user.email },
        withCredentials: true,
      });
      setReports(res.data.reports || []);
    } catch (err) {
      console.error('Failed to fetch reports:', err);
      toast.error('Failed to load reports. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (report, config) => {
    try {
      toast.info('Preparing your PDF...');
      const res = await axios.get(config.pdfPath(report), {
        responseType: 'blob',
        withCredentials: true,
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', config.filename(report));
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      const pwd = res.headers['x-pdf-password'];
      if (pwd) {
        toast.success(`PDF downloaded! Password: ${pwd}`, { duration: 10000 });
      } else {
        toast.success('PDF downloaded!');
      }
    } catch (err) {
      console.error('PDF download error:', err);
      toast.error('Failed to download PDF. Please try again.');
    }
  };

  const handleView = (report, config) => {
    navigate(config.path(report));
  };

  const filtered = filter === 'all'
    ? reports
    : reports.filter(r => r.type === filter);

  const counts = {
    all: reports.length,
    birth_chart: reports.filter(r => r.type === 'birth_chart').length,
    kundali_milan: reports.filter(r => r.type === 'kundali_milan').length,
    brihat_kundli: reports.filter(r => r.type === 'brihat_kundli').length,
  };

  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">

          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-1">
              <h1 className="text-3xl font-playfair font-semibold">My Reports</h1>
              {!loading && reports.length > 0 && (
                <Button variant="ghost" size="sm" onClick={fetchReports} className="gap-1.5 text-muted-foreground">
                  <RefreshCw className="h-3.5 w-3.5" /> Refresh
                </Button>
              )}
            </div>
            <p className="text-muted-foreground text-sm">
              All your generated Vedic astrology reports in one place
            </p>
          </div>

          {/* Filter tabs */}
          {reports.length > 0 && (
            <div className="flex gap-2 mb-6 flex-wrap">
              {[
                { key: 'all', label: 'All Reports' },
                { key: 'birth_chart', label: 'Birth Chart' },
                { key: 'kundali_milan', label: 'Kundali Milan' },
                { key: 'brihat_kundli', label: 'Brihat Kundli' },
              ].map(({ key, label }) => counts[key] > 0 || key === 'all' ? (
                <button
                  key={key}
                  onClick={() => setFilter(key)}
                  className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-colors border ${
                    filter === key
                      ? 'bg-gold text-primary-foreground border-gold'
                      : 'border-border text-muted-foreground hover:border-gold/50'
                  }`}
                >
                  {label}
                  {counts[key] > 0 && (
                    <span className={`ml-1.5 px-1.5 py-0.5 rounded-full text-xs ${
                      filter === key ? 'bg-white/20' : 'bg-muted'
                    }`}>
                      {counts[key]}
                    </span>
                  )}
                </button>
              ) : null)}
            </div>
          )}

          {/* Content */}
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 gap-4">
              <Sparkles className="h-10 w-10 text-gold animate-pulse" />
              <p className="text-muted-foreground text-sm">Loading your reports...</p>
            </div>
          ) : reports.length === 0 ? (
            <EmptyState navigate={navigate} />
          ) : filtered.length === 0 ? (
            <Card className="p-8 text-center border border-border">
              <p className="text-muted-foreground text-sm">No {filter.replace('_', ' ')} reports found.</p>
            </Card>
          ) : (
            <div className="space-y-4">
              {filtered.map(report => (
                <ReportCard
                  key={report.id}
                  report={report}
                  onDownload={handleDownload}
                  onView={handleView}
                />
              ))}
            </div>
          )}

          {/* Generate more CTA */}
          {!loading && reports.length > 0 && (
            <div className="mt-8 p-5 rounded-sm border border-gold/20 bg-gold/5 text-center">
              <p className="text-sm font-semibold mb-3">Generate a new report</p>
              <div className="flex flex-wrap gap-2 justify-center">
                <Button size="sm" onClick={() => navigate('/birth-chart')}
                  variant="outline" className="gap-1.5 border-gold/40 hover:bg-gold/10 text-xs">
                  <Star className="h-3.5 w-3.5 text-gold" /> Birth Chart
                </Button>
                <Button size="sm" onClick={() => navigate('/kundali-milan')}
                  variant="outline" className="gap-1.5 border-gold/40 hover:bg-gold/10 text-xs">
                  <Heart className="h-3.5 w-3.5 text-pink-500" /> Kundali Milan
                </Button>
                <Button size="sm" onClick={() => navigate('/brihat-kundli')}
                  variant="outline" className="gap-1.5 border-gold/40 hover:bg-gold/10 text-xs">
                  <Crown className="h-3.5 w-3.5 text-purple-500" /> Brihat Kundli Pro
                </Button>
              </div>
            </div>
          )}

        </div>
      </main>
      <Footer />
    </div>
  );
};
