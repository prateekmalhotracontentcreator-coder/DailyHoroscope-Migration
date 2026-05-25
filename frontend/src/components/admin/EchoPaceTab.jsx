import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  AlertTriangle,
  BarChart3,
  ChevronLeft,
  ChevronRight,
  Eye,
  FileDown,
  FileText,
  History,
  Link2,
  Loader2,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Trash2,
} from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Input } from '../ui/input';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/admin/echo-pace`;

const formatDateTime = (value) => {
  if (!value) {
    return '-';
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }

  return date.toLocaleString();
};

const similarityLabel = (value) => `${Math.round((Number(value) || 0) * 100)}%`;

const metricValue = (payload, key) => {
  const value = payload?.[key];
  return value ?? '-';
};

const parseMissingKeywords = (result) => {
  if (Array.isArray(result?.missing_keywords)) {
    return result.missing_keywords;
  }
  const raw = String(result?.keyword_check || '');
  const match = raw.match(/\[(.*)\]/);
  if (!match) {
    return [];
  }
  return match[1]
    .split(',')
    .map((item) => item.trim().replace(/^['"]|['"]$/g, ''))
    .filter(Boolean);
};

const statusTone = (ok, danger = false) => {
  if (ok) {
    return 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200';
  }
  if (danger) {
    return 'border-red-500/30 bg-red-500/10 text-red-200';
  }
  return 'border-amber-500/30 bg-amber-500/10 text-amber-200';
};

const StatusCard = ({ icon: Icon, label, value, detail, ok, danger = false }) => (
  <div className={`rounded-2xl border p-4 ${statusTone(ok, danger)}`}>
    <div className="mb-3 flex items-center gap-2 text-xs uppercase tracking-[0.2em]">
      <Icon className="h-4 w-4" />
      <span>{label}</span>
    </div>
    <div className="text-2xl font-semibold text-white">{value}</div>
    <div className="mt-1 text-sm text-white/70">{detail}</div>
  </div>
);

const DetailModal = ({ record, loading, onClose }) => {
  if (!record && !loading) {
    return null;
  }

  const inputMetrics = record?.input_metrics || {};
  const outputMetrics = record?.output_metrics || {};

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
      <Card className="max-h-[90vh] w-full max-w-4xl overflow-hidden border border-amber-500/30 bg-slate-950 text-white shadow-2xl shadow-amber-950/20">
        <div className="flex items-center justify-between border-b border-white/10 px-6 py-4">
          <div>
            <div className="text-xs uppercase tracking-[0.24em] text-amber-200">Audit Record</div>
            <div className="mt-1 text-lg font-semibold">E.C.H.O. // P.A.C.E. History Detail</div>
          </div>
          <Button variant="outline" onClick={onClose} className="border-white/20 text-white hover:bg-white/10">
            Close
          </Button>
        </div>
        <div className="max-h-[calc(90vh-80px)] overflow-y-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center gap-3 py-16 text-slate-300">
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>Loading audit record...</span>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="grid gap-4 md:grid-cols-3">
                <StatusCard
                  icon={ShieldCheck}
                  label="Copyright"
                  value={record?.copyright_passed ? 'PASSED' : 'RISK'}
                  detail={`Similarity ${similarityLabel(record?.similarity_score)}`}
                  ok={record?.copyright_passed}
                  danger={!record?.copyright_passed}
                />
                <StatusCard
                  icon={Sparkles}
                  label="Keywords"
                  value={record?.keyword_check === 'Pass' ? 'ALL INTACT' : 'CHECK'}
                  detail={record?.keyword_check || '-'}
                  ok={record?.keyword_check === 'Pass'}
                />
                <StatusCard
                  icon={BarChart3}
                  label="Reading Grade"
                  value={`Grade ${metricValue(outputMetrics, 'reading_grade_level')}`}
                  detail={`Input ${metricValue(inputMetrics, 'reading_grade_level')}`}
                  ok
                />
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-xs uppercase tracking-[0.18em] text-slate-400">Meta Tags</div>
                <div className="mt-3 space-y-3">
                  <div>
                    <div className="text-sm text-slate-300">Meta Title</div>
                    <div className="mt-1 text-white">{record?.meta_title || '-'}</div>
                  </div>
                  <div>
                    <div className="text-sm text-slate-300">Meta Description</div>
                    <div className="mt-1 text-white">{record?.meta_desc || '-'}</div>
                  </div>
                </div>
              </div>

              <div className="overflow-x-auto rounded-2xl border border-white/10">
                <table className="w-full text-left text-sm">
                  <thead className="bg-white/5 text-slate-400">
                    <tr>
                      <th className="px-4 py-3">Metric</th>
                      <th className="px-4 py-3">Original</th>
                      <th className="px-4 py-3">Optimised</th>
                    </tr>
                  </thead>
                  <tbody>
                    {[
                      ['Word Count', 'word_count'],
                      ['Flesch Reading Ease', 'flesch_reading_ease'],
                      ['Reading Grade Level', 'reading_grade_level'],
                      ['Lexical Diversity', 'lexical_diversity'],
                    ].map(([label, key]) => (
                      <tr key={key} className="border-t border-white/10">
                        <td className="px-4 py-3 text-white">{label}</td>
                        <td className="px-4 py-3 text-slate-300">{metricValue(inputMetrics, key)}</td>
                        <td className="px-4 py-3 text-slate-300">{metricValue(outputMetrics, key)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-xs uppercase tracking-[0.18em] text-slate-400">Matched Sources</div>
                <div className="mt-3 space-y-3">
                  {(record?.matched_sources || []).length ? (
                    record.matched_sources.map((source, index) => (
                      <div key={`${source.url}-${index}`} className="rounded-xl border border-white/10 bg-slate-950/60 p-3">
                        <div className="text-sm font-medium text-white">{source.title || 'Matched Source'}</div>
                        <div className="mt-1 text-sm text-slate-300">&ldquo;{source.phrase}&rdquo;</div>
                        <a
                          href={source.url}
                          target="_blank"
                          rel="noreferrer"
                          className="mt-2 inline-flex items-center gap-2 text-xs text-amber-200 hover:text-amber-100"
                        >
                          <Link2 className="h-3.5 w-3.5" />
                          {source.url}
                        </a>
                      </div>
                    ))
                  ) : (
                    <div className="text-sm text-slate-400">No matched sources recorded.</div>
                  )}
                </div>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="text-xs uppercase tracking-[0.18em] text-slate-400">Humanised Content</div>
                <textarea
                  readOnly
                  value={record?.humanised_content || ''}
                  className="mt-3 min-h-[320px] w-full rounded-xl border border-white/10 bg-slate-950/70 px-4 py-3 text-sm leading-7 text-white outline-none"
                />
              </div>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};

export const EchoPaceTab = ({ getAuthHeaders }) => {
  const [activeSubTab, setActiveSubTab] = useState('process');
  const [rawText, setRawText] = useState('');
  const [keywordsInput, setKeywordsInput] = useState('');
  const [threshold, setThreshold] = useState(0.2);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [historyItems, setHistoryItems] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyPage, setHistoryPage] = useState(1);
  const [historyTotal, setHistoryTotal] = useState(0);
  const [detailLoading, setDetailLoading] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [deletingId, setDeletingId] = useState('');

  const missingKeywords = parseMissingKeywords(result);
  const inputMetrics = result?.input_metrics || {};
  const outputMetrics = result?.output_metrics || {};
  const pageSize = 20;

  const fetchHistory = async (page = historyPage) => {
    setHistoryLoading(true);
    try {
      const response = await axios.get(`${API}/history`, {
        headers: getAuthHeaders(),
        params: { page, page_size: pageSize },
      });
      setHistoryItems(response.data.items || []);
      setHistoryPage(response.data.page || page);
      setHistoryTotal(response.data.total || 0);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load ECHO//PACE history');
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    if (activeSubTab === 'history') {
      fetchHistory(historyPage);
    }
  }, [activeSubTab, historyPage]);

  const handleProcess = async () => {
    if (!rawText.trim()) {
      toast.error('Paste raw SEO content before running the pipeline');
      return;
    }

    setProcessing(true);
    try {
      const seoKeywords = keywordsInput
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean);
      const response = await axios.post(
        `${API}/process`,
        {
          raw_text: rawText,
          seo_keywords: seoKeywords,
          threshold,
        },
        { headers: getAuthHeaders() }
      );
      setResult(response.data);
      toast.success('ECHO//PACE pipeline complete');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Pipeline run failed');
    } finally {
      setProcessing(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!result) {
      return;
    }

    try {
      const response = await axios.post(
        `${API}/export-pdf`,
        {
          copyright_passed: result.copyright_passed,
          similarity_score: result.similarity_score,
          matched_sources: result.matched_sources || [],
          humanised_content: result.humanised_content || '',
          meta_title: result.meta_title || '',
          meta_desc: result.meta_desc || '',
          input_metrics: result.input_metrics || {},
          output_metrics: result.output_metrics || {},
          keyword_check: result.keyword_check || 'Pass',
          missing_keywords: parseMissingKeywords(result),
          scanned_sentences: result.scanned_sentences ?? null,
        },
        {
          headers: getAuthHeaders(),
          responseType: 'blob',
        }
      );
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      const disposition = response.headers['content-disposition'] || '';
      const match = disposition.match(/filename="?([^"]+)"?/);
      link.href = url;
      link.download = match?.[1] || 'echo_pace_report.pdf';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success('PDF report downloaded');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to export PDF');
    }
  };

  const handleViewRecord = async (logId) => {
    setSelectedRecord(null);
    setDetailLoading(true);
    try {
      const response = await axios.get(`${API}/history/${encodeURIComponent(logId)}`, {
        headers: getAuthHeaders(),
      });
      setSelectedRecord(response.data);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load audit record');
    } finally {
      setDetailLoading(false);
    }
  };

  const handleDeleteRecord = async (logId) => {
    if (!window.confirm('Delete this ECHO//PACE audit record?')) {
      return;
    }

    setDeletingId(logId);
    try {
      await axios.delete(`${API}/history/${encodeURIComponent(logId)}`, {
        headers: getAuthHeaders(),
      });
      toast.success('Audit record deleted');
      await fetchHistory(historyPage);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to delete audit record');
    } finally {
      setDeletingId('');
    }
  };

  const closeModal = () => {
    setSelectedRecord(null);
    setDetailLoading(false);
  };

  return (
    <>
      {(selectedRecord || detailLoading) ? (
        <DetailModal record={selectedRecord} loading={detailLoading} onClose={closeModal} />
      ) : null}

      <Card className="border border-amber-500/30 bg-slate-900/95 shadow-2xl shadow-amber-950/20">
        <div className="space-y-6 p-6">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <div className="mb-2 flex items-center gap-2 text-amber-200">
                <Sparkles className="h-4 w-4" />
                <span className="text-xs font-semibold uppercase tracking-[0.24em]">Editorial Governance Engine</span>
              </div>
              <h3 className="text-xl font-semibold text-white">E.C.H.O. // P.A.C.E.</h3>
              <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
                Run the two-stage content validation pipeline before SEO pages go live: copyright risk scan first, then Claude-driven humanisation and meta optimisation.
              </p>
            </div>

            <div className="flex flex-wrap gap-2">
              {[
                { id: 'process', label: 'Process', icon: Sparkles },
                { id: 'history', label: 'History', icon: History },
              ].map(({ id, label, icon: Icon }) => (
                <Button
                  key={id}
                  size="sm"
                  variant={activeSubTab === id ? 'default' : 'outline'}
                  onClick={() => setActiveSubTab(id)}
                  className={activeSubTab === id ? 'bg-amber-300 text-slate-950 hover:bg-amber-200' : 'border-white/15 text-white hover:bg-white/10'}
                >
                  <Icon className="mr-1.5 h-3.5 w-3.5" />
                  {label}
                </Button>
              ))}
            </div>
          </div>

          {activeSubTab === 'process' ? (
            <div className="grid gap-6 xl:grid-cols-[minmax(0,0.95fr)_minmax(0,1.05fr)]">
              <Card className="border border-white/10 bg-slate-950/60 p-5">
                <div className="mb-4">
                  <div className="text-xs uppercase tracking-[0.18em] text-slate-400">Input</div>
                  <div className="mt-1 text-lg font-semibold text-white">Raw SEO Draft</div>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="mb-2 block text-sm text-slate-300">Paste raw SEO content here</label>
                    <textarea
                      value={rawText}
                      onChange={(event) => setRawText(event.target.value)}
                      placeholder="Paste the full article or landing-page draft..."
                      className="min-h-[320px] w-full rounded-xl border border-white/10 bg-slate-900 px-4 py-3 text-sm leading-7 text-white outline-none ring-0 transition focus:border-amber-300/40"
                    />
                  </div>

                  <div>
                    <label className="mb-2 block text-sm text-slate-300">SEO Keywords to preserve (comma-separated)</label>
                    <Input
                      value={keywordsInput}
                      onChange={(event) => setKeywordsInput(event.target.value)}
                      placeholder="crystal healing, angel number 111, transit meaning"
                      className="border-white/10 bg-slate-900 text-white"
                    />
                  </div>

                  <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <label className="text-sm text-slate-300">Copyright risk threshold</label>
                      <Input
                        type="number"
                        value={threshold}
                        min="0"
                        max="1"
                        step="0.05"
                        onChange={(event) => setThreshold(Number(event.target.value))}
                        className="w-24 border-white/10 bg-slate-900 text-white"
                      />
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={threshold}
                      onChange={(event) => setThreshold(Number(event.target.value))}
                      className="mt-4 h-2 w-full cursor-pointer accent-amber-300"
                    />
                    <div className="mt-2 flex justify-between text-xs text-slate-500">
                      <span>Strict</span>
                      <span>Flexible</span>
                    </div>
                  </div>

                  <Button
                    onClick={handleProcess}
                    disabled={processing}
                    className="w-full bg-amber-300 text-slate-950 hover:bg-amber-200"
                  >
                    {processing ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Sparkles className="mr-2 h-4 w-4" />}
                    {processing ? 'Running pipeline...' : 'Run ECHO//PACE Pipeline'}
                  </Button>
                </div>
              </Card>

              <Card className="border border-white/10 bg-slate-950/60 p-5">
                <div className="mb-4 flex items-center justify-between gap-3">
                  <div>
                    <div className="text-xs uppercase tracking-[0.18em] text-slate-400">Output</div>
                    <div className="mt-1 text-lg font-semibold text-white">Optimised Admin Review</div>
                  </div>
                  {result ? (
                    <Button
                      variant="outline"
                      onClick={handleDownloadPdf}
                      className="border-amber-300/40 text-amber-100 hover:bg-amber-300/10"
                    >
                      <FileDown className="mr-2 h-4 w-4" />
                      Download PDF Report
                    </Button>
                  ) : null}
                </div>

                {!result ? (
                  <div className="flex min-h-[640px] flex-col items-center justify-center rounded-2xl border border-dashed border-white/10 bg-white/[0.03] px-6 text-center">
                    <FileText className="h-10 w-10 text-slate-500" />
                    <div className="mt-4 text-lg font-medium text-white">No processed output yet</div>
                    <p className="mt-2 max-w-lg text-sm leading-6 text-slate-400">
                      Run the pipeline to see copyright risk, keyword integrity, reading-grade changes, meta tags, and the humanised content block.
                    </p>
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div className="grid gap-4 md:grid-cols-3">
                      <StatusCard
                        icon={result.copyright_passed ? ShieldCheck : AlertTriangle}
                        label="Copyright Check"
                        value={result.copyright_passed ? 'PASSED' : 'RISK DETECTED'}
                        detail={`${similarityLabel(result.similarity_score)} similarity`}
                        ok={result.copyright_passed}
                        danger={!result.copyright_passed}
                      />
                      <StatusCard
                        icon={Sparkles}
                        label="SEO Keywords"
                        value={!missingKeywords.length ? 'ALL INTACT' : `MISSING ${missingKeywords.length}`}
                        detail={!missingKeywords.length ? 'Every keyword survived the rewrite' : missingKeywords.join(', ')}
                        ok={!missingKeywords.length}
                      />
                      <StatusCard
                        icon={BarChart3}
                        label="Reading Grade"
                        value={`Grade ${metricValue(outputMetrics, 'reading_grade_level')}`}
                        detail={`Input ${metricValue(inputMetrics, 'reading_grade_level')} → Output ${metricValue(outputMetrics, 'reading_grade_level')}`}
                        ok
                      />
                    </div>

                    {result.matched_sources?.length ? (
                      <details className="rounded-2xl border border-red-500/20 bg-red-500/5 p-4">
                        <summary className="cursor-pointer text-sm font-medium text-red-100">
                          {result.copyright_passed ? 'Matched sources detected during scan' : 'Review matched sources before publishing'}
                        </summary>
                        <div className="mt-4 space-y-3">
                          {result.matched_sources.map((source, index) => (
                            <div key={`${source.url}-${index}`} className="rounded-xl border border-white/10 bg-slate-950/60 p-3">
                              <div className="text-sm font-medium text-white">{source.title || 'Matched Source'}</div>
                              <div className="mt-1 text-sm text-slate-300">&ldquo;{source.phrase}&rdquo;</div>
                              <a
                                href={source.url}
                                target="_blank"
                                rel="noreferrer"
                                className="mt-2 inline-flex items-center gap-2 text-xs text-amber-200 hover:text-amber-100"
                              >
                                <Link2 className="h-3.5 w-3.5" />
                                {source.url}
                              </a>
                            </div>
                          ))}
                        </div>
                      </details>
                    ) : null}

                    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                      <div className="mb-3 flex items-center justify-between gap-4">
                        <div className="text-sm font-medium text-white">Meta Tag Preview</div>
                        <div className="text-xs text-slate-400">
                          Scanned sentences: {result.scanned_sentences ?? '-'}
                        </div>
                      </div>
                      <div className="space-y-4">
                        <div>
                          <div className="flex items-center justify-between gap-3 text-sm text-slate-300">
                            <span>Meta Title</span>
                            <span>{(result.meta_title || '').length}/60</span>
                          </div>
                          <div className="mt-1 rounded-xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white">
                            {result.meta_title || '-'}
                          </div>
                        </div>
                        <div>
                          <div className="flex items-center justify-between gap-3 text-sm text-slate-300">
                            <span>Meta Description</span>
                            <span>{(result.meta_desc || '').length}/155</span>
                          </div>
                          <div className="mt-1 rounded-xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white">
                            {result.meta_desc || '-'}
                          </div>
                        </div>
                      </div>
                    </div>

                    <div>
                      <div className="mb-2 text-sm font-medium text-white">Humanised Content</div>
                      <textarea
                        value={result.humanised_content || ''}
                        onChange={(event) => setResult((current) => (current ? { ...current, humanised_content: event.target.value } : current))}
                        className="min-h-[280px] w-full rounded-2xl border border-white/10 bg-slate-900 px-4 py-3 text-sm leading-7 text-white outline-none transition focus:border-amber-300/40"
                      />
                    </div>

                    <div className="overflow-x-auto rounded-2xl border border-white/10">
                      <table className="w-full text-left text-sm">
                        <thead className="bg-white/5 text-slate-400">
                          <tr>
                            <th className="px-4 py-3">Metric</th>
                            <th className="px-4 py-3">Original</th>
                            <th className="px-4 py-3">Optimised</th>
                          </tr>
                        </thead>
                        <tbody>
                          {[
                            ['Word Count', 'word_count'],
                            ['Flesch Reading Ease', 'flesch_reading_ease'],
                            ['Reading Grade Level', 'reading_grade_level'],
                            ['Lexical Diversity', 'lexical_diversity'],
                          ].map(([label, key]) => (
                            <tr key={key} className="border-t border-white/10">
                              <td className="px-4 py-3 text-white">{label}</td>
                              <td className="px-4 py-3 text-slate-300">{metricValue(inputMetrics, key)}</td>
                              <td className="px-4 py-3 text-slate-300">{metricValue(outputMetrics, key)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </Card>
            </div>
          ) : (
            <Card className="border border-white/10 bg-slate-950/60 p-5">
              <div className="mb-4 flex items-center justify-between gap-3">
                <div>
                  <div className="text-xs uppercase tracking-[0.18em] text-slate-400">History</div>
                  <div className="mt-1 text-lg font-semibold text-white">Audit Trail</div>
                </div>
                <Button
                  variant="outline"
                  onClick={() => fetchHistory(historyPage)}
                  disabled={historyLoading}
                  className="border-white/15 text-white hover:bg-white/10"
                >
                  <RefreshCw className={`mr-2 h-4 w-4 ${historyLoading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>
              </div>

              {historyLoading ? (
                <div className="flex items-center justify-center gap-3 py-16 text-slate-300">
                  <Loader2 className="h-5 w-5 animate-spin" />
                  <span>Loading audit history...</span>
                </div>
              ) : historyItems.length === 0 ? (
                <div className="py-16 text-center">
                  <History className="mx-auto h-10 w-10 text-slate-600" />
                  <div className="mt-4 text-lg font-medium text-white">No audit records yet</div>
                  <p className="mt-2 text-sm text-slate-400">Each completed pipeline run will appear here for later review and deletion.</p>
                </div>
              ) : (
                <>
                  <div className="overflow-x-auto rounded-2xl border border-white/10">
                    <table className="w-full text-left text-sm">
                      <thead className="bg-white/5 text-slate-400">
                        <tr>
                          <th className="px-4 py-3">Timestamp</th>
                          <th className="px-4 py-3">Word Count</th>
                          <th className="px-4 py-3">Copyright</th>
                          <th className="px-4 py-3">SEO Keywords</th>
                          <th className="px-4 py-3">Meta Title</th>
                          <th className="px-4 py-3 text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {historyItems.map((item) => (
                          <tr key={item.id} className="border-t border-white/10">
                            <td className="px-4 py-3 text-white">{formatDateTime(item.timestamp)}</td>
                            <td className="px-4 py-3 text-slate-300">
                              {metricValue(item.input_metrics, 'word_count')} → {metricValue(item.output_metrics, 'word_count')}
                            </td>
                            <td className="px-4 py-3">
                              <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${item.copyright_passed ? 'bg-emerald-500/15 text-emerald-200' : 'bg-red-500/15 text-red-200'}`}>
                                {item.copyright_passed ? 'PASSED' : 'RISK'}
                              </span>
                            </td>
                            <td className="px-4 py-3 text-slate-300">{item.keyword_check}</td>
                            <td className="max-w-[260px] truncate px-4 py-3 text-white">{item.meta_title || '-'}</td>
                            <td className="px-4 py-3">
                              <div className="flex justify-end gap-2">
                                <Button
                                  size="sm"
                                  variant="outline"
                                  onClick={() => handleViewRecord(item.id)}
                                  className="border-white/15 text-white hover:bg-white/10"
                                >
                                  <Eye className="mr-1.5 h-3.5 w-3.5" />
                                  View
                                </Button>
                                <Button
                                  size="sm"
                                  variant="outline"
                                  onClick={() => handleDeleteRecord(item.id)}
                                  disabled={deletingId === item.id}
                                  className="border-red-500/30 text-red-200 hover:bg-red-500/10"
                                >
                                  {deletingId === item.id ? <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" /> : <Trash2 className="mr-1.5 h-3.5 w-3.5" />}
                                  Delete
                                </Button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  <div className="mt-4 flex items-center justify-between gap-4">
                    <div className="text-sm text-slate-400">
                      Showing page {historyPage} of {Math.max(1, Math.ceil(historyTotal / pageSize))}
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setHistoryPage((current) => Math.max(1, current - 1))}
                        disabled={historyPage <= 1}
                        className="border-white/15 text-white hover:bg-white/10"
                      >
                        <ChevronLeft className="mr-1.5 h-3.5 w-3.5" />
                        Previous
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setHistoryPage((current) => current + 1)}
                        disabled={historyPage * pageSize >= historyTotal}
                        className="border-white/15 text-white hover:bg-white/10"
                      >
                        Next
                        <ChevronRight className="ml-1.5 h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </div>
                </>
              )}
            </Card>
          )}
        </div>
      </Card>
    </>
  );
};

export default EchoPaceTab;
