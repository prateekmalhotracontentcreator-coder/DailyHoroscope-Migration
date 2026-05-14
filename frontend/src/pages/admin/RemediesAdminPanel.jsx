import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { CheckCircle2, ChevronDown, ChevronUp, Loader2, RefreshCw, Search, ShieldAlert, ShieldCheck, TriangleAlert } from 'lucide-react';

import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const STATUS_CLASSES = {
  approved: 'bg-green-500/20 text-green-400',
  pending_human_review: 'bg-amber-500/20 text-amber-300',
  flagged: 'bg-red-500/20 text-red-400',
  pending_review: 'bg-yellow-500/20 text-yellow-300',
  rejected: 'bg-zinc-500/20 text-zinc-300',
};

const formatLabel = (value = '') =>
  value
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());

export function RemediesAdminPanel({ getAuthHeaders }) {
  const [records, setRecords] = useState([]);
  const [traditionsSummary, setTraditionsSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [expanded, setExpanded] = useState({});
  const [actionLoading, setActionLoading] = useState('');
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({
    tradition: 'all',
    category: 'all',
    action_type: 'all',
    approval_status: 'all',
    science_id: 'all',
  });

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
      setRecords(recordsRes.data.records || []);
      setTraditionsSummary(traditionsRes.data.traditions || []);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load remedies admin data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const uniqueOptions = useMemo(() => {
    const tradition = new Set();
    const category = new Set();
    const actionType = new Set();
    const approvalStatus = new Set();
    const scienceId = new Set();

    records.forEach((record) => {
      if (record.tradition) tradition.add(record.tradition);
      if (record.category) category.add(record.category);
      if (record.action_type) actionType.add(record.action_type);
      if (record.approval_status) approvalStatus.add(record.approval_status);
      if (record.science_id) scienceId.add(record.science_id);
    });

    return {
      tradition: Array.from(tradition).sort(),
      category: Array.from(category).sort(),
      action_type: Array.from(actionType).sort(),
      approval_status: Array.from(approvalStatus).sort(),
      science_id: Array.from(scienceId).sort(),
    };
  }, [records]);

  const filteredRecords = useMemo(() => {
    const searchValue = search.trim().toLowerCase();
    return records.filter((record) => {
      if (filters.tradition !== 'all' && record.tradition !== filters.tradition) return false;
      if (filters.category !== 'all' && record.category !== filters.category) return false;
      if (filters.action_type !== 'all' && record.action_type !== filters.action_type) return false;
      if (filters.approval_status !== 'all' && record.approval_status !== filters.approval_status) return false;
      if (filters.science_id !== 'all' && record.science_id !== filters.science_id) return false;
      if (!searchValue) return true;
      return record.search_blob?.includes(searchValue);
    });
  }, [records, filters, search]);

  const handleStatusChange = async (record, approvalStatus) => {
    const actionKey = `${record.source_collection}:${record.record_id}:${approvalStatus}`;
    setActionLoading(actionKey);
    try {
      const response = await axios.post(
        `${API}/remedies/admin/status`,
        {
          collection: record.source_collection,
          science_id: record.science_id,
          record_id: record.record_id,
          approval_status: approvalStatus,
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
      toast.success(`Status updated to ${approvalStatus}`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update remedy status');
    } finally {
      setActionLoading('');
    }
  };

  const toggleExpanded = (key) => {
    setExpanded((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  if (loading) {
    return (
      <Card className="p-6 bg-gray-800 border-gray-700">
        <div className="flex items-center gap-3 text-gray-300">
          <Loader2 className="h-5 w-5 animate-spin text-gold" />
          Loading remedies records...
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card className="p-6 bg-gray-800 border-gray-700">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-2">Cross-Collection Remedy Operations</p>
            <h3 className="text-xl font-semibold text-white">Remedies Console</h3>
            <p className="text-sm text-gray-400 mt-2 max-w-3xl">
              Review live remedy records across Jyotish, Lal Kitab, Krishna fallback, and related collections. Legacy statuses remain visible as-is; approvals can be moved into the current operating set.
            </p>
          </div>
          <Button
            onClick={() => loadData('refresh')}
            variant="outline"
            className="border-gray-600 text-gray-200 hover:bg-gray-700"
            disabled={refreshing}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-6 gap-3 mt-6">
          {traditionsSummary.map((item) => (
            <div key={`${item.collection}:${item.science_id}`} className="rounded-lg border border-gray-700 bg-gray-900/60 p-4">
              <p className="text-xs uppercase tracking-widest text-gold/80">{formatLabel(item.tradition)}</p>
              <p className="text-sm text-white font-semibold mt-2">{formatLabel(item.science_id)}</p>
              <div className="text-xs text-gray-400 mt-3 space-y-1">
                <p>Total: {item.total_records}</p>
                <p>Approved: {item.approved_records}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <Card className="p-6 bg-gray-800 border-gray-700">
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-6 gap-3">
          <div className="xl:col-span-2 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
            <Input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search by ID, title, description, or keyword"
              className="pl-9 bg-gray-900 border-gray-700 text-white"
            />
          </div>
          {['tradition', 'category', 'action_type', 'approval_status', 'science_id'].map((key) => (
            <select
              key={key}
              value={filters[key]}
              onChange={(event) => setFilters((prev) => ({ ...prev, [key]: event.target.value }))}
              className="h-10 rounded-md border border-gray-700 bg-gray-900 px-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold"
            >
              <option value="all">{formatLabel(key)}: All</option>
              {uniqueOptions[key].map((option) => (
                <option key={option} value={option}>
                  {formatLabel(option)}
                </option>
              ))}
            </select>
          ))}
        </div>

        <div className="flex items-center justify-between mt-4 text-xs text-gray-400">
          <span>{filteredRecords.length} records visible</span>
          <span>{records.length} total loaded</span>
        </div>
      </Card>

      <div className="space-y-4">
        {filteredRecords.map((record) => {
          const rowKey = `${record.source_collection}:${record.record_id}`;
          const isExpanded = Boolean(expanded[rowKey]);
          const statusClass = STATUS_CLASSES[record.approval_status] || 'bg-gray-500/20 text-gray-300';
          return (
            <Card key={rowKey} className="bg-gray-800 border-gray-700 overflow-hidden">
              <div className="p-5">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <div className="space-y-2">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${statusClass}`}>
                        {record.approval_status}
                      </span>
                      <span className="inline-flex rounded-full px-2 py-1 text-xs font-medium bg-blue-500/15 text-blue-300">
                        {formatLabel(record.tradition)}
                      </span>
                      <span className="inline-flex rounded-full px-2 py-1 text-xs font-medium bg-gray-700 text-gray-300">
                        {formatLabel(record.category)}
                      </span>
                      <span className="inline-flex rounded-full px-2 py-1 text-xs font-medium bg-gray-700 text-gray-300">
                        {formatLabel(record.action_type)}
                      </span>
                    </div>
                    <div>
                      <p className="text-white font-semibold text-lg">{record.title || 'Untitled remedy'}</p>
                      <p className="text-sm text-gray-400 mt-1">{record.description || 'No description available.'}</p>
                    </div>
                    <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                      <span>ID: {record.record_id}</span>
                      <span>Collection: {record.source_collection}</span>
                      <span>Science: {record.science_id}</span>
                    </div>
                  </div>

                  <div className="flex flex-col gap-2 lg:items-end">
                    <div className="flex flex-wrap gap-2">
                      {[
                        { value: 'approved', label: 'Approve', icon: CheckCircle2 },
                        { value: 'pending_human_review', label: 'Needs Review', icon: ShieldAlert },
                        { value: 'flagged', label: 'Flag', icon: TriangleAlert },
                      ].map(({ value, label, icon: Icon }) => {
                        const actionKey = `${record.source_collection}:${record.record_id}:${value}`;
                        const active = record.approval_status === value;
                        return (
                          <Button
                            key={value}
                            size="sm"
                            variant="outline"
                            className={`border-gray-600 text-gray-200 hover:bg-gray-700 ${active ? 'ring-1 ring-gold text-gold' : ''}`}
                            disabled={actionLoading === actionKey}
                            onClick={() => handleStatusChange(record, value)}
                          >
                            {actionLoading === actionKey ? (
                              <Loader2 className="h-3.5 w-3.5 mr-1.5 animate-spin" />
                            ) : (
                              <Icon className="h-3.5 w-3.5 mr-1.5" />
                            )}
                            {label}
                          </Button>
                        );
                      })}
                    </div>
                    <button
                      type="button"
                      onClick={() => toggleExpanded(rowKey)}
                      className="inline-flex items-center gap-1 text-xs text-gold hover:text-gold/80 transition-colors"
                    >
                      {isExpanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                      {isExpanded ? 'Hide full rule detail' : 'View full rule detail'}
                    </button>
                  </div>
                </div>
              </div>

              {isExpanded && (
                <div className="border-t border-gray-700 bg-gray-900/70 p-5">
                  <pre className="overflow-x-auto whitespace-pre-wrap break-words text-xs leading-6 text-gray-300">
                    {JSON.stringify(record.document, null, 2)}
                  </pre>
                </div>
              )}
            </Card>
          );
        })}

        {filteredRecords.length === 0 && (
          <Card className="p-8 bg-gray-800 border-gray-700 text-center">
            <ShieldCheck className="h-8 w-8 text-gold mx-auto mb-3" />
            <p className="text-white font-medium">No remedy records match the current filters.</p>
            <p className="text-sm text-gray-400 mt-2">Try broadening the filters or clearing the search term.</p>
          </Card>
        )}
      </div>
    </div>
  );
}

export default RemediesAdminPanel;
