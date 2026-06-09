import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { AlertTriangle, CheckCircle2, Copy, Globe2, Loader2, RefreshCw, SearchCheck } from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const summaryCard = (label, value, tone = 'text-white') => (
  <Card className="p-4 bg-gray-800 border-gray-700">
    <div className="text-xs text-gray-400 uppercase tracking-wider">{label}</div>
    <div className={`text-2xl font-bold mt-2 ${tone}`}>{value ?? '--'}</div>
  </Card>
);

export const IntelligenceTab = ({ getAuthHeaders }) => {
  const [subTab, setSubTab] = useState('gsc');
  const [gscStatus, setGscStatus] = useState(null);
  const [gscLoading, setGscLoading] = useState(false);
  const [gscData, setGscData] = useState(null);
  const [serperLoading, setSerperLoading] = useState(false);
  const [serperData, setSerperData] = useState(null);

  const fetchGscStatus = async () => {
    try {
      const res = await axios.get(`${API}/admin/gsc/status`, { headers: getAuthHeaders() });
      setGscStatus(res.data);
    } catch {}
  };

  const fetchGscData = async () => {
    setGscLoading(true);
    try {
      const res = await axios.get(`${API}/admin/intelligence/gsc`, { headers: getAuthHeaders() });
      setGscData(res.data);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to load GSC data');
    } finally {
      setGscLoading(false);
    }
  };

  const refreshGsc = async () => {
    setGscLoading(true);
    try {
      const res = await axios.get(`${API}/admin/intelligence/gsc/refresh`, { headers: getAuthHeaders() });
      setGscData(res.data);
      toast.success('GSC intelligence refreshed');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to refresh GSC data');
    } finally {
      setGscLoading(false);
    }
  };

  const connectGsc = async () => {
    try {
      const res = await axios.get(`${API}/admin/gsc/auth-url`, { headers: getAuthHeaders() });
      const popup = window.open(res.data.auth_url, 'gsc_oauth', 'width=600,height=720,left=320,top=100');
      const handler = (event) => {
        if (event.data?.type === 'gsc_connected') {
          window.removeEventListener('message', handler);
          fetchGscStatus();
          fetchGscData();
          toast.success('GSC connected');
        }
      };
      window.addEventListener('message', handler);
      const timer = setInterval(() => {
        if (popup?.closed) {
          clearInterval(timer);
          window.removeEventListener('message', handler);
          fetchGscStatus();
        }
      }, 1000);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to start GSC OAuth');
    }
  };

  const disconnectGsc = async () => {
    try {
      await axios.post(`${API}/admin/gsc/disconnect`, {}, { headers: getAuthHeaders() });
      setGscStatus({ connected: false, site_url: null, connected_at: null });
      setGscData(null);
      toast.success('GSC disconnected');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to disconnect GSC');
    }
  };

  const fetchSerperData = async () => {
    setSerperLoading(true);
    try {
      const res = await axios.get(`${API}/admin/intelligence/serper`, { headers: getAuthHeaders() });
      setSerperData(res.data);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to load SERPER data');
    } finally {
      setSerperLoading(false);
    }
  };

  const refreshSerper = async () => {
    setSerperLoading(true);
    try {
      const res = await axios.get(`${API}/admin/intelligence/serper/refresh`, { headers: getAuthHeaders() });
      setSerperData(res.data);
      toast.success('SERPER intelligence refreshed');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to refresh SERPER data');
    } finally {
      setSerperLoading(false);
    }
  };

  useEffect(() => {
    fetchGscStatus();
    fetchGscData();
    fetchSerperData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const serperMissing = useMemo(
    () => serperData?.configured === false,
    [serperData, serperLoading],
  );

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap gap-2">
        {[
          { id: 'gsc', label: 'GSC -- Index Health', icon: Globe2 },
          { id: 'serper', label: 'SERPER -- Keyword Intel', icon: SearchCheck },
        ].map(({ id, label, icon: Icon }) => (
          <Button
            key={id}
            size="sm"
            variant="outline"
            onClick={() => setSubTab(id)}
            className={subTab === id ? 'bg-gold/20 text-gold border-gold/40' : 'border-gray-600 text-gray-300'}
          >
            <Icon className="h-3.5 w-3.5 mr-1.5" />
            {label}
          </Button>
        ))}
      </div>

      {subTab === 'gsc' && (
        <div className="space-y-4">
          <Card className="p-5 bg-gray-800 border-gray-700">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3">
              <div>
                <h3 className="text-white font-semibold">Google Search Console</h3>
                {gscStatus?.connected
                  ? <p className="text-green-400 text-sm mt-1">Connected to {gscStatus.site_url}</p>
                  : <p className="text-yellow-400 text-sm mt-1">Not connected yet</p>}
              </div>
              <div className="flex gap-2">
                {gscStatus?.connected ? (
                  <Button onClick={disconnectGsc} variant="outline" size="sm" className="border-red-700/50 text-red-400">
                    Disconnect
                  </Button>
                ) : (
                  <Button onClick={connectGsc} size="sm" className="bg-gold hover:bg-gold/90 text-gray-900">
                    Connect Google Search Console
                  </Button>
                )}
                <Button onClick={refreshGsc} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                  <RefreshCw className={`h-3.5 w-3.5 ${gscLoading ? 'animate-spin' : ''}`} />
                </Button>
              </div>
            </div>
          </Card>

          {gscLoading && !gscData ? (
            <Card className="p-6 bg-gray-800 border-gray-700 text-gray-400 text-sm flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" /> Loading GSC index health...
            </Card>
          ) : gscData?.data ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
                {summaryCard('Indexed', gscData.data.summary?.indexed, 'text-green-400')}
                {summaryCard('Crawled -- Not Indexed', gscData.data.summary?.crawled_not_indexed, 'text-yellow-400')}
                {summaryCard('Excluded', gscData.data.summary?.excluded, 'text-orange-400')}
                {summaryCard('Errors', gscData.data.summary?.errors, 'text-red-400')}
              </div>

              <Card className="p-5 bg-gray-800 border-gray-700 overflow-x-auto">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-white font-semibold">Flagged URLs</h4>
                  <span className="text-xs text-gray-400">{gscData.fetched_at ? `Last fetched ${new Date(gscData.fetched_at).toLocaleString('en-IN')}` : 'No cache yet'}</span>
                </div>
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-gray-400 border-b border-gray-700">
                      <th className="py-2 pr-4">URL</th>
                      <th className="py-2 pr-4">Coverage State</th>
                      <th className="py-2 pr-4">Impressions</th>
                      <th className="py-2 pr-4">Clicks</th>
                      <th className="py-2 pr-4">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(gscData.data.flagged_urls || []).map((row) => (
                      <tr key={row.url} className="border-b border-gray-800 align-top">
                        <td className="py-3 pr-4 text-gray-300">
                          <div className="flex items-start gap-2">
                            <span className="break-all">{row.url}</span>
                            <button onClick={() => navigator.clipboard.writeText(row.url).then(() => toast.success('URL copied'))} className="text-gray-500 hover:text-gold">
                              <Copy className="h-3.5 w-3.5" />
                            </button>
                          </div>
                        </td>
                        <td className="py-3 pr-4 text-gray-400">{row.coverage_state}</td>
                        <td className="py-3 pr-4 text-gray-300">{row.impressions_30d}</td>
                        <td className="py-3 pr-4 text-gray-300">{row.clicks_30d}</td>
                        <td className="py-3 pr-4">
                          {row.verdict === 'PASS'
                            ? <span className="text-green-400 inline-flex items-center gap-1"><CheckCircle2 className="h-3.5 w-3.5" />PASS</span>
                            : <span className="text-yellow-400 inline-flex items-center gap-1"><AlertTriangle className="h-3.5 w-3.5" />{row.verdict}</span>}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Card>

              <Card className="p-5 bg-gray-800 border-gray-700 overflow-x-auto">
                <h4 className="text-white font-semibold mb-4">Top Queries (Last 30 Days)</h4>
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-gray-400 border-b border-gray-700">
                      <th className="py-2 pr-4">Query</th>
                      <th className="py-2 pr-4">Clicks</th>
                      <th className="py-2 pr-4">Impressions</th>
                      <th className="py-2 pr-4">Avg Position</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(gscData.data.top_queries || []).map((row) => (
                      <tr key={row.query} className="border-b border-gray-800">
                        <td className="py-3 pr-4 text-gray-300">{row.query}</td>
                        <td className="py-3 pr-4 text-gray-300">{row.clicks}</td>
                        <td className="py-3 pr-4 text-gray-300">{row.impressions}</td>
                        <td className="py-3 pr-4 text-gray-300">{Number(row.position || 0).toFixed(1)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </Card>
            </>
          ) : (
            <Card className="p-6 bg-gray-800 border-gray-700 text-gray-400 text-sm">
              Connect GSC and run a refresh to populate the Intelligence cache.
            </Card>
          )}
        </div>
      )}

      {subTab === 'serper' && (
        <div className="space-y-4">
          {serperMissing ? (
            <Card className="p-5 bg-gray-800 border-yellow-700/40 text-yellow-300">
              SERPER_API_KEY missing -- add it to Render env vars, then refresh this panel.
            </Card>
          ) : !serperData?.data && !serperLoading ? (
            <Card className="p-5 bg-gray-800 border-gray-700 text-gray-300">
              SERPER is configured, but no cache exists yet. Run a refresh to fetch the first keyword snapshot.
            </Card>
          ) : (
            <>
              <div className="flex justify-end">
                <Button onClick={refreshSerper} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                  <RefreshCw className={`h-3.5 w-3.5 mr-1.5 ${serperLoading ? 'animate-spin' : ''}`} />
                  Refresh now
                </Button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {summaryCard('Ranking Top 10', `${serperData?.data?.summary?.queries_where_we_rank_top10 ?? 0}/10`, 'text-green-400')}
                {summaryCard('Not Ranking', serperData?.data?.summary?.queries_where_we_are_absent ?? 0, 'text-red-400')}
                {summaryCard('Top Competitor', serperData?.data?.summary?.most_frequent_competitor || '--', 'text-gold')}
              </div>

              <Card className="p-5 bg-gray-800 border-gray-700 overflow-x-auto">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-white font-semibold">Query Rankings</h4>
                  <span className="text-xs text-gray-400">{serperData?.fetched_at ? `Last fetched ${new Date(serperData.fetched_at).toLocaleString('en-IN')}` : 'No cache yet'}</span>
                </div>
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-gray-400 border-b border-gray-700">
                      <th className="py-2 pr-4">Query</th>
                      <th className="py-2 pr-4">Our Position</th>
                      <th className="py-2 pr-4">Our URL</th>
                      <th className="py-2 pr-4">Top Competitor</th>
                      <th className="py-2 pr-4">Their Position</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(serperData?.data?.queries || []).map((row) => {
                      const topCompetitor = row.competitor_results?.[0];
                      const positionTone = row.our_position == null ? 'text-red-400' : row.our_position <= 3 ? 'text-green-400' : 'text-yellow-400';
                      return (
                        <tr key={row.query} className="border-b border-gray-800 align-top">
                          <td className="py-3 pr-4 text-gray-300">{row.query}</td>
                          <td className={`py-3 pr-4 font-medium ${positionTone}`}>{row.our_position ? `#${row.our_position}` : '--'}</td>
                          <td className="py-3 pr-4 text-gray-400 break-all">{row.our_url || '--'}</td>
                          <td className="py-3 pr-4 text-gray-300">{topCompetitor?.domain || row.top_result?.domain || '--'}</td>
                          <td className="py-3 pr-4 text-gray-300">{topCompetitor?.position ? `#${topCompetitor.position}` : '--'}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </Card>
            </>
          )}
        </div>
      )}
    </div>
  );
};
