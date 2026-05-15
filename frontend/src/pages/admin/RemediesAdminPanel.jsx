import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import {
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Loader2,
  RefreshCw,
  Search,
  ShieldAlert,
  ShieldCheck,
  TriangleAlert,
} from 'lucide-react';

import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const STATUS_OPTIONS = ['approved', 'pending_human_review', 'flagged'];
const STATUS_CLASSES = {
  approved: 'bg-green-500/20 text-green-300 border border-green-500/30',
  pending_human_review: 'bg-amber-500/20 text-amber-300 border border-amber-500/30',
  flagged: 'bg-red-500/20 text-red-300 border border-red-500/30',
  pending_review: 'bg-yellow-500/20 text-yellow-200 border border-yellow-500/30',
  rejected: 'bg-zinc-500/20 text-zinc-300 border border-zinc-500/30',
  unknown: 'bg-gray-500/20 text-gray-300 border border-gray-500/30',
};

const COLLECTION_LABELS = {
  all: 'All Collections',
  jyotish_remedies: 'jyotish_remedies',
  lk_remedies: 'lk_remedies',
  krishna_prashnavali_remedies: 'krishna_prashnavali_remedies',
};

const formatLabel = (value = '') =>
  value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());

const DETAIL_FIELDS = [
  { key: 'mantra', label: 'Mantra' },
  { key: 'ritual_remedy', label: 'Ritual Remedy' },
  { key: 'behavioral_display_hint', label: 'Behavioral Remedy' },
];

function DetailBlock({ label, payload }) {
  if (!payload) return null;
  const sanskrit = payload.sanskrit_block;
  const english = payload.english_block;
  if (!sanskrit && !english) return null;
  return (
    <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
      <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-gold/80">{label}</p>
      {sanskrit ? <p className="mt-3 text-sm leading-6 text-white">{sanskrit}</p> : null}
      {english ? <p className="mt-2 text-sm leading-6 text-gray-300">{english}</p> : null}
    </div>
  );
}

export function RemediesAdminPanel({ getAuthHeaders }) {
  const [records, setRecords] = useState([]);
  const [traditionsSummary, setTraditionsSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [expanded, setExpanded] = useState({});
  const [statusDrafts, setStatusDrafts] = useState({});
  const [actionLoading, setActionLoading] = useState('');
  const [search, setSearch] = useState('');
  const [collectionFilter, setCollectionFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async (mode = 'initial') => {
    if (mode === 'refresh') {
      setRefreshing(true);
    } else {
      setLoading(true);
    }
    try {
      const [recordsRes, traditionsRes] = await Promise.all([
        axios.get(`${API}/remedies/admin/records`, { headers: getAuthHeaders() }),
        axios.get(`${API}/remedies/traditions`, { headers: getAuthHeaders() }),
      ]);
      const nextRecords = recordsRes.data.records || [];
      setRecords(nextRecords);
      setTraditionsSummary(traditionsRes.data.traditions || []);
      setStatusDrafts(
        Object.fromEntries(
          nextRecords.map((record) => [
            `${record.source_collection}:${record.record_id}`,
            STATUS_OPTIONS.includes(record.approval_status) ? record.approval_status : '',
          ])
        )
      );
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load remedies admin data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const filteredRecords = useMemo(() => {
    const searchValue = search.trim().toLowerCase();
    return records.filter((record) => {
      if (collectionFilter !== 'all' && record.collection_key !== collectionFilter) return false;
      if (statusFilter !== 'all' && record.approval_status !== statusFilter) return false;
      if (!searchValue) return true;
      return record.search_blob?.includes(searchValue);
    });
  }, [records, search, collectionFilter, statusFilter]);

  const toggleExpanded = (key) => {
    setExpanded((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleStatusSave = async (record) => {
    const rowKey = `${record.source_collection}:${record.record_id}`;
    const nextStatus = statusDrafts[rowKey];
    if (!nextStatus || nextStatus === record.approval_status) return;
    const actionKey = `${rowKey}:${nextStatus}`;
    setActionLoading(actionKey);
    try {
      const response = await axios.patch(
        `${API}/remedies/admin/records/${record.record_id}/status`,
        {
          collection: record.source_collection,
          science_id: record.science_id,
          approval_status: nextStatus,
        },
        { headers: getAuthHeaders() }
      );
      setRecords((prev) =>
        prev.map((item) =>
          item.source_collection === record.source_collection && item.record_id === record.record_id
            ? response.data.record
            : item
        )
      );
      toast.success(`Status updated to ${nextStatus}`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update remedy status');
    } finally {
      setActionLoading('');
    }
  };

  if (loading) {
    return (
      <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6">
        <div className="flex items-center gap-3 text-gray-300">
          <Loader2 className="h-5 w-5 animate-spin text-gold" />
          Loading remedies records...
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold/80">Cross-Collection Remedy Operations</p>
            <h3 className="mt-2 text-2xl font-semibold text-white">Remedies Console</h3>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-gray-300">
              Review Krishna fallback records, Jyotish remedies, and Lal Kitab entries in one place. Legacy statuses remain visible as-is; operators can move any record into the active approval set.
            </p>
          </div>
          <Button
            onClick={() => loadData('refresh')}
            variant="outline"
            className="border-gold/30 text-gold hover:bg-gold/10"
            disabled={refreshing}
          >
            <RefreshCw className={`mr-2 h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-3 md:grid-cols-3 xl:grid-cols-6">
          {traditionsSummary.map((item) => (
            <div key={`${item.collection}:${item.science_id}`} className="rounded-xl border border-gold/20 bg-black/20 p-4">
              <p className="text-[11px] uppercase tracking-[0.24em] text-gold/75">{formatLabel(item.tradition)}</p>
              <p className="mt-2 text-sm font-semibold text-white">{formatLabel(item.science_id)}</p>
              <div className="mt-3 space-y-1 text-xs text-gray-400">
                <p>Total: {item.total_records}</p>
                <p>Approved: {item.approved_records}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
        <div className="grid grid-cols-1 gap-3 lg:grid-cols-[1.4fr,0.9fr,0.9fr,auto]">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
            <Input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search by remedy_id, planet, tradition, or keyword"
              className="border-gold/20 bg-black/30 pl-9 text-white"
            />
          </div>
          <select
            value={collectionFilter}
            onChange={(event) => setCollectionFilter(event.target.value)}
            className="h-10 rounded-md border border-gold/20 bg-black/30 px-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold"
          >
            {Object.entries(COLLECTION_LABELS).map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
          <select
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
            className="h-10 rounded-md border border-gold/20 bg-black/30 px-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold"
          >
            <option value="all">All Statuses</option>
            <option value="approved">approved</option>
            <option value="pending_human_review">pending_human_review</option>
            <option value="flagged">flagged</option>
            <option value="pending_review">pending_review</option>
            <option value="rejected">rejected</option>
          </select>
          <div className="inline-flex items-center justify-center rounded-md border border-gold/20 bg-black/20 px-4 text-sm font-medium text-gold">
            {filteredRecords.length} results
          </div>
        </div>
      </Card>

      <Card className="overflow-hidden rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="border-b border-gold/20 bg-black/25 text-xs uppercase tracking-[0.22em] text-gold/70">
              <tr>
                <th className="px-4 py-3">remedy_id</th>
                <th className="px-4 py-3">tradition / science</th>
                <th className="px-4 py-3">planet</th>
                <th className="px-4 py-3">status</th>
                <th className="px-4 py-3">updated</th>
                <th className="px-4 py-3">actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredRecords.map((record) => {
                const rowKey = `${record.source_collection}:${record.record_id}`;
                const isExpanded = Boolean(expanded[rowKey]);
                const currentStatusClass = STATUS_CLASSES[record.approval_status] || STATUS_CLASSES.unknown;
                const draftStatus = statusDrafts[rowKey] ?? '';
                const saveDisabled = !draftStatus || draftStatus === record.approval_status || Boolean(actionLoading);

                return (
                  <React.Fragment key={rowKey}>
                    <tr className="border-b border-gold/10 align-top text-gray-200">
                      <td className="px-4 py-4 font-mono text-xs text-gold">{record.remedy_id || record.record_id}</td>
                      <td className="px-4 py-4">
                        <p className="font-medium text-white">{formatLabel(record.tradition)}</p>
                        <p className="mt-1 text-xs text-gray-400">{record.science_id}</p>
                        <p className="mt-1 text-[11px] text-gray-500">{record.collection_key}</p>
                      </td>
                      <td className="px-4 py-4 text-gray-300">{record.planet || '--'}</td>
                      <td className="px-4 py-4">
                        <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-medium ${currentStatusClass}`}>
                          {record.approval_status}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-xs text-gray-400">{record.updated_at || '--'}</td>
                      <td className="px-4 py-4">
                        <div className="flex min-w-[220px] flex-col gap-2">
                          <select
                            value={draftStatus}
                            onChange={(event) =>
                              setStatusDrafts((prev) => ({ ...prev, [rowKey]: event.target.value }))
                            }
                            className="h-9 rounded-md border border-gold/20 bg-black/30 px-3 text-xs text-white focus:outline-none focus:ring-1 focus:ring-gold"
                          >
                            <option value="">Change status...</option>
                            {STATUS_OPTIONS.map((value) => (
                              <option key={value} value={value}>{value}</option>
                            ))}
                          </select>
                          <div className="flex items-center gap-2">
                            <Button
                              size="sm"
                              onClick={() => handleStatusSave(record)}
                              disabled={saveDisabled}
                              className="bg-gold text-black hover:bg-gold/90"
                            >
                              {actionLoading === `${rowKey}:${draftStatus}` ? (
                                <Loader2 className="mr-1.5 h-3.5 w-3.5 animate-spin" />
                              ) : (
                                <CheckCircle2 className="mr-1.5 h-3.5 w-3.5" />
                              )}
                              Save
                            </Button>
                            <button
                              type="button"
                              onClick={() => toggleExpanded(rowKey)}
                              className="inline-flex items-center gap-1 text-xs font-medium text-gold hover:text-gold/80"
                            >
                              {isExpanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                              {isExpanded ? 'Collapse' : 'Expand'}
                            </button>
                          </div>
                        </div>
                      </td>
                    </tr>
                    {isExpanded ? (
                      <tr className="border-b border-gold/10 bg-black/20">
                        <td colSpan={6} className="px-4 py-5">
                          <div className="space-y-4">
                            <div className="grid gap-4 lg:grid-cols-2">
                              {DETAIL_FIELDS.map(({ key, label }) => (
                                <DetailBlock key={key} label={label} payload={record.document?.[key]} />
                              ))}
                              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-gold/80">Remedy Ref</p>
                                <p className="mt-3 font-mono text-sm text-white">
                                  {record.document?.remedy_ref || record.document?.remedy_id || '--'}
                                </p>
                              </div>
                            </div>
                            <details className="rounded-xl border border-gold/20 bg-black/20 p-4">
                              <summary className="cursor-pointer text-sm font-medium text-white">Full JSON viewer</summary>
                              <pre className="mt-4 overflow-x-auto whitespace-pre-wrap break-words text-xs leading-6 text-gray-300">
                                {JSON.stringify(record.document, null, 2)}
                              </pre>
                            </details>
                          </div>
                        </td>
                      </tr>
                    ) : null}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>

        {filteredRecords.length === 0 ? (
          <div className="p-8 text-center">
            <ShieldCheck className="mx-auto mb-3 h-8 w-8 text-gold" />
            <p className="font-medium text-white">No remedy records match the current filters.</p>
            <p className="mt-2 text-sm text-gray-400">Broaden the filters or clear the search term.</p>
          </div>
        ) : null}
      </Card>
    </div>
  );
}

export default RemediesAdminPanel;
