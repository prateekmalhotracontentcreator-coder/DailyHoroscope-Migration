import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'sonner';
import {
  BookOpen,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Eye,
  Loader2,
  RefreshCw,
  X,
} from 'lucide-react';

import { useAdminAuth } from '../../context/AdminAuthContext';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SUB_TABS = [
  { id: 'rules', label: 'Rules Browser' },
  { id: 'batches', label: 'Import Batches' },
  { id: 'index', label: 'Index Status' },
];

const STATUS_BADGES = {
  pending_review: 'bg-yellow-500/20 text-yellow-400',
  approved: 'bg-green-500/20 text-green-400',
  rejected: 'bg-red-500/20 text-red-400',
};

const STRENGTH_BADGES = {
  low: 'bg-gray-500/20 text-gray-300',
  medium: 'bg-blue-500/20 text-blue-400',
  high: 'bg-orange-500/20 text-orange-400',
  extreme: 'bg-red-500/20 text-red-400',
};

const BATCH_STATUS_BADGES = {
  staged: 'bg-gray-500/20 text-gray-300',
  validated: 'bg-blue-500/20 text-blue-400',
  imported: 'bg-green-500/20 text-green-400',
  failed: 'bg-red-500/20 text-red-400',
};

function formatDate(value) {
  if (!value) {
    return 'Not set';
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return 'Not set';
  }
  return date.toLocaleString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

function truncateId(value, count = 12) {
  if (!value) {
    return '-';
  }
  return value.length > count ? `${value.slice(0, count)}...` : value;
}

function badgeClass(map, value) {
  return map[value] || 'bg-gray-500/20 text-gray-300';
}

function sleep(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

export function LibraryConsolePage({ getAuthHeaders: getAuthHeadersProp }) {
  const navigate = useNavigate();
  const {
    getAuthHeaders: getAuthHeadersHook,
    isAuthenticated,
    loading: authLoading,
  } = useAdminAuth();
  const getAuthHeaders = getAuthHeadersProp ?? getAuthHeadersHook;

  const [activeTab, setActiveTab] = useState('rules');
  const [scienceInput, setScienceInput] = useState('');
  const [debouncedScienceId, setDebouncedScienceId] = useState('');
  const [approvalStatus, setApprovalStatus] = useState('');
  const [strengthBand, setStrengthBand] = useState('');
  const [rules, setRules] = useState([]);
  const [rulesLoading, setRulesLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [totalRules, setTotalRules] = useState(0);
  const [expandedRuleId, setExpandedRuleId] = useState(null);
  const [expandedRuleDetails, setExpandedRuleDetails] = useState({});
  const [detailLoadingId, setDetailLoadingId] = useState(null);
  const [ruleActionId, setRuleActionId] = useState(null);
  const [batches, setBatches] = useState([]);
  const [batchesLoading, setBatchesLoading] = useState(false);
  const [batchActionId, setBatchActionId] = useState(null);
  const [indexStatus, setIndexStatus] = useState(null);
  const [indexLoading, setIndexLoading] = useState(false);
  const [refreshingIndex, setRefreshingIndex] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedScienceId(scienceInput.trim()), 400);
    return () => window.clearTimeout(timer);
  }, [scienceInput]);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate('/admin/login');
    }
  }, [authLoading, isAuthenticated, navigate]);

  const canLoad = !authLoading && isAuthenticated;

  const currentRuleFilters = useMemo(
    () => ({
      science_id: debouncedScienceId || undefined,
      approval_status: approvalStatus || undefined,
      strength_band: strengthBand || undefined,
    }),
    [approvalStatus, debouncedScienceId, strengthBand]
  );

  const fetchRules = async (targetPage = page, filtersOverride = null) => {
    if (!canLoad) {
      return;
    }
    setRulesLoading(true);
    try {
      const response = await axios.get(`${API}/knowledge/rules`, {
        headers: getAuthHeaders(),
        params: {
          page: targetPage,
          page_size: 50,
          ...(filtersOverride || currentRuleFilters),
        },
      });
      setRules(response.data.rules || []);
      setTotalRules(response.data.total || 0);
      setPages(response.data.pages || 1);
      setPage(response.data.page || targetPage);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load rules');
    } finally {
      setRulesLoading(false);
    }
  };

  const fetchBatches = async () => {
    if (!canLoad) {
      return;
    }
    setBatchesLoading(true);
    try {
      const response = await axios.get(`${API}/knowledge/import-batches`, {
        headers: getAuthHeaders(),
      });
      setBatches(response.data.batches || []);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load import batches');
    } finally {
      setBatchesLoading(false);
    }
  };

  const fetchIndexStatus = async () => {
    if (!canLoad) {
      return null;
    }
    setIndexLoading(true);
    try {
      const response = await axios.get(`${API}/knowledge/index/status`, {
        headers: getAuthHeaders(),
      });
      setIndexStatus(response.data);
      return response.data;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load index status');
      return null;
    } finally {
      setIndexLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'rules' && canLoad) {
      fetchRules(page);
    }
  }, [activeTab, canLoad, page]);

  useEffect(() => {
    if (activeTab === 'batches' && canLoad && batches.length === 0) {
      fetchBatches();
    }
  }, [activeTab, batches.length, canLoad]);

  useEffect(() => {
    if (activeTab === 'index' && canLoad && !indexStatus) {
      fetchIndexStatus();
    }
  }, [activeTab, canLoad, indexStatus]);

  const handleLoadRules = async () => {
    const nextFilters = {
      science_id: scienceInput.trim() || undefined,
      approval_status: approvalStatus || undefined,
      strength_band: strengthBand || undefined,
    };
    setDebouncedScienceId(scienceInput.trim());
    setExpandedRuleId(null);
    setPage(1);
    await fetchRules(1, nextFilters);
  };

  const handleRuleDecision = async (ruleId, nextStatus) => {
    setRuleActionId(ruleId);
    try {
      await axios.patch(
        `${API}/knowledge/rules/${ruleId}/${nextStatus === 'approved' ? 'approve' : 'reject'}`,
        {},
        { headers: getAuthHeaders() }
      );
      setRules((current) =>
        current.map((rule) =>
          rule.rule_id === ruleId
            ? { ...rule, approval_status: nextStatus, updated_at: new Date().toISOString() }
            : rule
        )
      );
      setExpandedRuleDetails((current) => {
        if (!current[ruleId]) {
          return current;
        }
        return {
          ...current,
          [ruleId]: {
            ...current[ruleId],
            approval_status: nextStatus,
            updated_at: new Date().toISOString(),
          },
        };
      });
      toast.success(`Rule ${nextStatus === 'approved' ? 'approved' : 'rejected'}`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update rule');
    } finally {
      setRuleActionId(null);
    }
  };

  const handleViewRule = async (ruleId) => {
    if (expandedRuleId === ruleId) {
      setExpandedRuleId(null);
      return;
    }
    setExpandedRuleId(ruleId);
    if (expandedRuleDetails[ruleId]) {
      return;
    }
    setDetailLoadingId(ruleId);
    try {
      const response = await axios.get(`${API}/knowledge/rules/${ruleId}`, {
        headers: getAuthHeaders(),
      });
      setExpandedRuleDetails((current) => ({
        ...current,
        [ruleId]: response.data,
      }));
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load rule details');
      setExpandedRuleId(null);
    } finally {
      setDetailLoadingId(null);
    }
  };

  const handleApproveAll = async (batchId) => {
    if (!window.confirm('Approve all pending rules in this batch?')) {
      return;
    }
    setBatchActionId(batchId);
    try {
      const response = await axios.post(
        `${API}/knowledge/import-batches/${batchId}/approve-all`,
        {},
        { headers: getAuthHeaders() }
      );
      setBatches((current) =>
        current.map((batch) =>
          batch.batch_id === batchId
            ? {
                ...batch,
                approval_status: 'approved',
                updated_at: new Date().toISOString(),
              }
            : batch
        )
      );
      toast.success(`${response.data.rules_approved || 0} rules approved`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to approve batch rules');
    } finally {
      setBatchActionId(null);
    }
  };

  const handleRefreshIndex = async () => {
    const preRefreshBuiltAt = indexStatus?.built_at || null;
    setRefreshingIndex(true);
    try {
      await axios.post(
        `${API}/knowledge/index/refresh`,
        {},
        { headers: getAuthHeaders() }
      );
      toast.success('Index refresh triggered');
      for (let attempt = 0; attempt < 20; attempt += 1) {
        if (attempt > 0) {
          await sleep(3000);
        }
        const latest = await fetchIndexStatus();
        if (!latest) {
          continue;
        }
        if ((latest.built_at || null) !== preRefreshBuiltAt) {
          toast.success(`Index refreshed - ${latest.rule_count || 0} rules loaded`);
          setRefreshingIndex(false);
          return;
        }
      }
      toast.success('Refresh triggered - check again in a moment');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to trigger index refresh');
    } finally {
      setRefreshingIndex(false);
    }
  };

  if (authLoading) {
    return <div className="text-center py-8 text-gray-400">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <div className="space-y-6">
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <div>
            <h2 className="text-xl font-semibold text-white flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-yellow-400" />
              Library Console
            </h2>
            <p className="text-sm text-gray-400 mt-1">
              Review imported rules, approve batches, and manage the live knowledge index.
            </p>
          </div>
          <div className="text-sm text-gray-400">
            {activeTab === 'rules' && `${totalRules} rules`}
            {activeTab === 'batches' && `${batches.length} batches`}
            {activeTab === 'index' && 'Index monitor'}
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {SUB_TABS.map((tab) => (
            <Button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              size="sm"
              className={
                activeTab === tab.id
                  ? 'bg-yellow-400/10 text-yellow-400 border border-yellow-400/30'
                  : 'border-gray-600 text-gray-300 hover:bg-gray-700'
              }
              variant="outline"
            >
              {tab.label}
            </Button>
          ))}
        </div>

        {activeTab === 'rules' && (
          <div className="space-y-4">
            <Card className="rounded-xl border border-yellow-400/20 bg-yellow-400/[0.04] shadow-sm p-4">
              <div className="flex flex-wrap items-end gap-3">
                <div className="min-w-[220px] flex-1">
                  <label className="text-xs uppercase tracking-wide text-gray-400 mb-2 block">
                    Science ID
                  </label>
                  <Input
                    value={scienceInput}
                    onChange={(event) => setScienceInput(event.target.value)}
                    placeholder="vedic_astrology"
                    className="bg-gray-800 border-gray-700 text-white"
                  />
                </div>
                <div className="min-w-[180px]">
                  <label className="text-xs uppercase tracking-wide text-gray-400 mb-2 block">
                    Approval Status
                  </label>
                  <select
                    value={approvalStatus}
                    onChange={(event) => setApprovalStatus(event.target.value)}
                    className="w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-white focus:outline-none"
                  >
                    <option value="">All</option>
                    <option value="pending_review">Pending Review</option>
                    <option value="approved">Approved</option>
                    <option value="rejected">Rejected</option>
                  </select>
                </div>
                <div className="min-w-[180px]">
                  <label className="text-xs uppercase tracking-wide text-gray-400 mb-2 block">
                    Strength Band
                  </label>
                  <select
                    value={strengthBand}
                    onChange={(event) => setStrengthBand(event.target.value)}
                    className="w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-white focus:outline-none"
                  >
                    <option value="">All</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="extreme">Extreme</option>
                  </select>
                </div>
                <Button
                  onClick={handleLoadRules}
                  className="bg-yellow-400/10 text-yellow-400 border border-yellow-400/30 hover:bg-yellow-400/20"
                  variant="outline"
                >
                  Load
                </Button>
              </div>
            </Card>

            <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-x-auto">
              {rulesLoading ? (
                <div className="py-8 text-center text-gray-400">Loading...</div>
              ) : (
                <table className="w-full min-w-[980px]">
                  <thead className="bg-gray-900/70">
                    <tr className="text-left text-xs uppercase tracking-wide text-gray-400">
                      <th className="px-4 py-3">Rule ID</th>
                      <th className="px-4 py-3">Science</th>
                      <th className="px-4 py-3">Domain</th>
                      <th className="px-4 py-3">Categories</th>
                      <th className="px-4 py-3">Strength</th>
                      <th className="px-4 py-3">Status</th>
                      <th className="px-4 py-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rules.map((rule) => {
                      const detail = expandedRuleDetails[rule.rule_id];
                      const isExpanded = expandedRuleId === rule.rule_id;
                      const isDetailLoading = detailLoadingId === rule.rule_id;
                      const isActionLoading = ruleActionId === rule.rule_id;
                      return (
                        <React.Fragment key={rule.rule_id}>
                          <tr className="border-t border-gray-700 text-sm text-gray-200">
                            <td className="px-4 py-3 font-mono text-xs" title={rule.rule_id}>
                              {truncateId(rule.rule_id)}
                            </td>
                            <td className="px-4 py-3">{rule.science_id}</td>
                            <td className="px-4 py-3">{rule.life_domain}</td>
                            <td className="px-4 py-3 text-gray-300">
                              {(rule.categories || []).join(', ') || '-'}
                            </td>
                            <td className="px-4 py-3">
                              <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${badgeClass(STRENGTH_BADGES, rule.strength_band)}`}>
                                {rule.strength_band}
                              </span>
                            </td>
                            <td className="px-4 py-3">
                              <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${badgeClass(STATUS_BADGES, rule.approval_status)}`}>
                                {rule.approval_status}
                              </span>
                            </td>
                            <td className="px-4 py-3">
                              <div className="flex flex-wrap gap-2">
                                <Button
                                  size="sm"
                                  variant="outline"
                                  disabled={isActionLoading || rule.approval_status === 'approved'}
                                  onClick={() => handleRuleDecision(rule.rule_id, 'approved')}
                                  className="border-green-500/30 text-green-400 hover:bg-green-500/10"
                                >
                                  {isActionLoading ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Check className="h-3.5 w-3.5 mr-1" />}
                                  Approve
                                </Button>
                                <Button
                                  size="sm"
                                  variant="outline"
                                  disabled={isActionLoading || rule.approval_status === 'rejected'}
                                  onClick={() => handleRuleDecision(rule.rule_id, 'rejected')}
                                  className="border-red-500/30 text-red-400 hover:bg-red-500/10"
                                >
                                  <X className="h-3.5 w-3.5 mr-1" />
                                  Reject
                                </Button>
                                <Button
                                  size="sm"
                                  variant="outline"
                                  onClick={() => handleViewRule(rule.rule_id)}
                                  className="border-gray-600 text-gray-300 hover:bg-gray-700"
                                >
                                  <Eye className="h-3.5 w-3.5 mr-1" />
                                  View
                                  {isExpanded ? <ChevronUp className="h-3.5 w-3.5 ml-1" /> : <ChevronDown className="h-3.5 w-3.5 ml-1" />}
                                </Button>
                              </div>
                            </td>
                          </tr>
                          {isExpanded && (
                            <tr className="border-t border-gray-700/60 bg-gray-900/40">
                              <td colSpan={7} className="px-4 py-4">
                                {isDetailLoading ? (
                                  <div className="text-sm text-gray-400">Loading...</div>
                                ) : detail ? (
                                  <div className="space-y-4">
                                    <div>
                                      <p className="text-xs uppercase tracking-wide text-gray-500 mb-1">Summary</p>
                                      <p className="text-sm text-gray-200">{detail.interpretation?.summary || '-'}</p>
                                    </div>
                                    <div>
                                      <p className="text-xs uppercase tracking-wide text-gray-500 mb-1">Detailed</p>
                                      <p className="text-sm text-gray-300 whitespace-pre-line">
                                        {detail.interpretation?.detailed || '-'}
                                      </p>
                                    </div>
                                    <div className="grid gap-4 md:grid-cols-2">
                                      <div>
                                        <p className="text-xs uppercase tracking-wide text-gray-500 mb-2">Positive Aspects</p>
                                        <div className="space-y-1">
                                          {(detail.interpretation?.positive_aspects || []).length > 0 ? (
                                            detail.interpretation.positive_aspects.map((item, index) => (
                                              <p key={`${detail.rule_id}-positive-${index}`} className="text-sm text-green-300">{item}</p>
                                            ))
                                          ) : (
                                            <p className="text-sm text-gray-500">None listed.</p>
                                          )}
                                        </div>
                                      </div>
                                      <div>
                                        <p className="text-xs uppercase tracking-wide text-gray-500 mb-2">Challenging Aspects</p>
                                        <div className="space-y-1">
                                          {(detail.interpretation?.challenging_aspects || []).length > 0 ? (
                                            detail.interpretation.challenging_aspects.map((item, index) => (
                                              <p key={`${detail.rule_id}-challenge-${index}`} className="text-sm text-red-300">{item}</p>
                                            ))
                                          ) : (
                                            <p className="text-sm text-gray-500">None listed.</p>
                                          )}
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                ) : (
                                  <div className="text-sm text-gray-400">No details available.</div>
                                )}
                              </td>
                            </tr>
                          )}
                        </React.Fragment>
                      );
                    })}
                    {rules.length === 0 && (
                      <tr>
                        <td colSpan={7} className="px-4 py-8 text-center text-gray-500">
                          No rules found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              )}
            </div>

            <div className="flex items-center justify-between gap-3 flex-wrap">
              <p className="text-sm text-gray-400">
                Page {page} of {pages}
              </p>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  disabled={page <= 1 || rulesLoading}
                  onClick={() => setPage((current) => Math.max(1, current - 1))}
                  className="border-gray-600 text-gray-300 hover:bg-gray-700"
                >
                  Prev
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  disabled={page >= pages || rulesLoading}
                  onClick={() => setPage((current) => Math.min(pages, current + 1))}
                  className="border-gray-600 text-gray-300 hover:bg-gray-700"
                >
                  Next
                </Button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'batches' && (
          <div className="space-y-4">
            {batchesLoading ? (
              <div className="text-center py-8 text-gray-400">Loading...</div>
            ) : batches.length === 0 ? (
              <div className="bg-gray-800 rounded-lg border border-gray-700 py-8 text-center text-gray-500">
                No import batches found.
              </div>
            ) : (
              batches.map((batch) => (
                <Card
                  key={batch.batch_id}
                  className="bg-gray-800 rounded-lg border border-gray-700 p-5"
                >
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div>
                      <h3 className="text-lg font-semibold text-white">{batch.source_book}</h3>
                      <p className="font-mono text-xs text-gray-500 mt-1">{batch.batch_id}</p>
                    </div>
                    <div className="flex gap-2 flex-wrap">
                      <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${badgeClass(BATCH_STATUS_BADGES, batch.import_status)}`}>
                        {batch.import_status}
                      </span>
                      <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${badgeClass(STATUS_BADGES, batch.approval_status)}`}>
                        {batch.approval_status}
                      </span>
                    </div>
                  </div>

                  <div className="grid gap-3 md:grid-cols-5 mt-4 text-sm">
                    <div className="rounded-lg border border-gray-700 bg-gray-900/40 p-3">
                      <p className="text-gray-500 text-xs uppercase tracking-wide">Submitted</p>
                      <p className="text-white mt-1">{batch.rules_submitted || 0}</p>
                    </div>
                    <div className="rounded-lg border border-gray-700 bg-gray-900/40 p-3">
                      <p className="text-gray-500 text-xs uppercase tracking-wide">Imported</p>
                      <p className="text-white mt-1">{batch.rules_imported || 0}</p>
                    </div>
                    <div className="rounded-lg border border-gray-700 bg-gray-900/40 p-3">
                      <p className="text-gray-500 text-xs uppercase tracking-wide">Duplicates</p>
                      <p className="text-white mt-1">{batch.duplicate_count || 0}</p>
                    </div>
                    <div className="rounded-lg border border-gray-700 bg-gray-900/40 p-3">
                      <p className="text-gray-500 text-xs uppercase tracking-wide">Errors</p>
                      <p className="text-white mt-1">{batch.error_count || 0}</p>
                    </div>
                    <div className="rounded-lg border border-gray-700 bg-gray-900/40 p-3">
                      <p className="text-gray-500 text-xs uppercase tracking-wide">Index Refreshed</p>
                      <p className={`mt-1 ${batch.index_refreshed ? 'text-green-400' : 'text-gray-400'}`}>
                        {batch.index_refreshed ? 'Yes' : 'No'}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between gap-4 flex-wrap mt-4">
                    <p className="text-sm text-gray-400">
                      Created {formatDate(batch.created_at)}
                    </p>
                    <Button
                      size="sm"
                      variant="outline"
                      disabled={batch.approval_status === 'approved' || batchActionId === batch.batch_id}
                      onClick={() => handleApproveAll(batch.batch_id)}
                      className="border-yellow-400/30 text-yellow-400 hover:bg-yellow-400/10"
                    >
                      {batchActionId === batch.batch_id ? (
                        <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                      ) : (
                        <CheckCircle2 className="h-3.5 w-3.5 mr-1.5" />
                      )}
                      Approve All Rules
                    </Button>
                  </div>
                </Card>
              ))
            )}
          </div>
        )}

        {activeTab === 'index' && (
          <Card className="rounded-xl border border-yellow-400/20 bg-yellow-400/[0.04] shadow-sm p-5">
            {indexLoading && !indexStatus ? (
              <div className="text-center py-8 text-gray-400">Loading...</div>
            ) : (
              <div className="space-y-5">
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div>
                    <h3 className="text-lg font-semibold text-white">Knowledge Index</h3>
                    <p className="text-sm text-gray-400 mt-1">
                      Current live rule index state for `scan_chart()`.
                    </p>
                  </div>
                  <Button
                    onClick={handleRefreshIndex}
                    disabled={refreshingIndex}
                    className="border-yellow-400/30 text-yellow-400 hover:bg-yellow-400/10"
                    variant="outline"
                  >
                    {refreshingIndex ? (
                      <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                    ) : (
                      <RefreshCw className="h-3.5 w-3.5 mr-1.5" />
                    )}
                    {refreshingIndex ? 'Refreshing...' : 'Refresh Index'}
                  </Button>
                </div>

                <div className="grid gap-4 md:grid-cols-3">
                  <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                    <p className="text-xs uppercase tracking-wide text-gray-500">Rule Count</p>
                    <p className="text-2xl font-semibold text-white mt-2">
                      {indexStatus?.rule_count ?? 0}
                    </p>
                  </div>
                  <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                    <p className="text-xs uppercase tracking-wide text-gray-500">Built At</p>
                    <p className="text-sm text-white mt-2">
                      {indexStatus?.built_at ? formatDate(indexStatus.built_at) : 'Not yet built'}
                    </p>
                  </div>
                  <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                    <p className="text-xs uppercase tracking-wide text-gray-500">Index Refreshed</p>
                    <div className="mt-2 flex items-center gap-2">
                      {indexStatus?.index_refreshed ? (
                        <>
                          <CheckCircle2 className="h-4 w-4 text-green-400" />
                          <span className="text-green-400 text-sm">Yes</span>
                        </>
                      ) : (
                        <>
                          <span className="text-gray-500 text-lg leading-none">-</span>
                          <span className="text-gray-400 text-sm">No</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </Card>
        )}
      </div>
    </div>
  );
}

export default LibraryConsolePage;
