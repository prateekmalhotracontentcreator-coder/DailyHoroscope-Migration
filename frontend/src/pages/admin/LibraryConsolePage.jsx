import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'sonner';
import {
  AlertCircle,
  BarChart3,
  BookOpen,
  Bug,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Eye,
  FileJson,
  FlaskConical,
  Loader2,
  Pencil,
  Play,
  RefreshCw,
  Save,
  Upload,
  Volume2,
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
  { id: 'cases', label: 'Case Studies' },
  { id: 'coverage', label: 'Coverage Dashboard' },
  { id: 'test', label: 'Test Console' },
  { id: 'voices', label: 'Voice Profiles' },
];

const STATUS_BADGES = {
  pending_review: 'bg-yellow-500/20 text-yellow-400',
  approved: 'bg-green-500/20 text-green-400',
  rejected: 'bg-red-500/20 text-red-400',
  auto_approved: 'bg-green-500/20 text-green-400',
  pending_human_review: 'bg-amber-500/20 text-amber-400',
  flagged: 'bg-red-500/20 text-red-400',
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

function truncateText(value, count = 28) {
  if (!value) {
    return '-';
  }
  return value.length > count ? `${value.slice(0, count)}...` : value;
}

function formatPercent(value) {
  if (value === null || value === undefined || value === '') {
    return '—';
  }
  const numeric = Number(value);
  if (Number.isNaN(numeric)) {
    return '—';
  }
  const pct = numeric <= 1 ? Math.round(numeric * 100) : Math.round(numeric);
  return `${pct}%`;
}

function dataQualityBadge(value) {
  if (value === 'high') {
    return 'bg-green-500/15 text-green-400 border-green-500/30';
  }
  if (value === 'medium') {
    return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
  }
  if (value === 'low') {
    return 'bg-red-500/15 text-red-400 border-red-500/30';
  }
  return 'bg-zinc-500/15 text-zinc-400 border-zinc-500/30';
}

async function readJsonFile(file) {
  const text = await file.text();
  return JSON.parse(text);
}

function normalizeImportedCases(payload) {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (Array.isArray(payload?.cases)) {
    return payload.cases;
  }
  return [];
}

function estimateConfidencePct(prediction) {
  if (prediction?.confidence_pct !== undefined && prediction?.confidence_pct !== null) {
    return formatPercent(prediction.confidence_pct);
  }
  if (prediction?.confidence !== undefined && prediction?.confidence !== null) {
    return formatPercent(prediction.confidence);
  }
  return '—';
}

function averagePercent(values) {
  const normalized = values
    .filter((value) => value !== null && value !== undefined && !Number.isNaN(Number(value)))
    .map((value) => {
      const numeric = Number(value);
      return numeric <= 1 ? numeric * 100 : numeric;
    });
  if (normalized.length === 0) {
    return null;
  }
  return Math.round(normalized.reduce((sum, value) => sum + value, 0) / normalized.length);
}

function aggregateCoverageCategories(categoryCounts = {}) {
  const buckets = {
    career: 0,
    health: 0,
    relationships: 0,
    wealth: 0,
    spirituality: 0,
    other: 0,
  };
  Object.entries(categoryCounts || {}).forEach(([key, value]) => {
    const numeric = Number(value) || 0;
    if (key === 'career') {
      buckets.career += numeric;
    } else if (key === 'health' || key === 'longevity') {
      buckets.health += numeric;
    } else if (key === 'relationships' || key === 'family' || key === 'social') {
      buckets.relationships += numeric;
    } else if (key === 'wealth' || key === 'finances') {
      buckets.wealth += numeric;
    } else if (key === 'spirituality') {
      buckets.spirituality += numeric;
    } else {
      buckets.other += numeric;
    }
  });
  return buckets;
}

function normalizeVoices(payload) {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (Array.isArray(payload?.voices)) {
    return payload.voices;
  }
  return [];
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
  const [statusFilter, setStatusFilter] = useState('');
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
  const [validationBatchId, setValidationBatchId] = useState(null);
  const [indexStatus, setIndexStatus] = useState(null);
  const [indexLoading, setIndexLoading] = useState(false);
  const [refreshingIndex, setRefreshingIndex] = useState(false);
  const [cases, setCases] = useState([]);
  const [casesLoading, setCasesLoading] = useState(false);
  const [casesError, setCasesError] = useState('');
  const [casesSearch, setCasesSearch] = useState('');
  const [caseDomainFilter, setCaseDomainFilter] = useState('');
  const [expandedCaseId, setExpandedCaseId] = useState(null);
  const [showImportModal, setShowImportModal] = useState(false);
  const [showValidationModal, setShowValidationModal] = useState(false);
  const [caseImportPreview, setCaseImportPreview] = useState([]);
  const [caseImportFileName, setCaseImportFileName] = useState('');
  const [importingCases, setImportingCases] = useState(false);
  const [validatingCases, setValidatingCases] = useState(false);
  const [coverageData, setCoverageData] = useState(null);
  const [coverageLoading, setCoverageLoading] = useState(false);
  const [coverageError, setCoverageError] = useState('');
  const [testForm, setTestForm] = useState({
    birth_date: '',
    birth_time: '',
    birth_place: '',
    report_type: 'career',
    voice_blend: 'classical+modern_analytical',
    depth: 'detailed',
  });
  const [testLoading, setTestLoading] = useState(false);
  const [testError, setTestError] = useState('');
  const [testResult, setTestResult] = useState(null);
  const [testOutputTab, setTestOutputTab] = useState('narrative');
  const [voices, setVoices] = useState([]);
  const [voicesLoading, setVoicesLoading] = useState(false);
  const [voicesError, setVoicesError] = useState('');
  const [editingVoiceId, setEditingVoiceId] = useState(null);
  const [voiceDrafts, setVoiceDrafts] = useState({});
  const [savingVoiceId, setSavingVoiceId] = useState(null);

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
      strength_band: strengthBand || undefined,
    }),
    [debouncedScienceId, strengthBand]
  );

  const displayedRules = useMemo(() => {
    if (!statusFilter) {
      return rules;
    }
    return rules.filter((rule) => rule.approval_status === statusFilter);
  }, [rules, statusFilter]);

  const filteredCases = useMemo(() => {
    const query = casesSearch.trim().toLowerCase();
    return cases.filter((entry) => {
      const matchesQuery =
        !query ||
        String(entry.case_id || '').toLowerCase().includes(query) ||
        String(entry.subject || '').toLowerCase().includes(query);
      const primaryDomain = entry.known_outcomes?.[0]?.life_domain || '';
      const matchesDomain = !caseDomainFilter || primaryDomain === caseDomainFilter;
      return matchesQuery && matchesDomain;
    });
  }, [caseDomainFilter, cases, casesSearch]);

  const caseStats = useMemo(() => {
    const validatedCount = cases.filter((entry) => entry.validated === true).length;
    const pendingCount = cases.filter((entry) => entry.validated !== true).length;
    const scores = cases
      .map((entry) => entry.accuracy_score)
      .filter((value) => value !== null && value !== undefined && !Number.isNaN(Number(value)))
      .map((value) => Number(value));
    const average = scores.length
      ? Math.round(
          scores.reduce((sum, value) => sum + (value <= 1 ? value * 100 : value), 0) / scores.length
        )
      : null;
    return {
      total: cases.length,
      validated: validatedCount,
      pending: pendingCount,
      averageAccuracy: average,
    };
  }, [cases]);

  const coverageCategoryBuckets = useMemo(
    () => aggregateCoverageCategories(coverageData?.category_counts || {}),
    [coverageData]
  );

  const coverageDonutSegments = useMemo(() => {
    const colors = {
      career: '#60a5fa',
      health: '#34d399',
      relationships: '#f472b6',
      wealth: '#d4af37',
      spirituality: '#a78bfa',
      other: '#9ca3af',
    };
    const entries = Object.entries(coverageCategoryBuckets).map(([key, value]) => ({
      key,
      value,
      color: colors[key],
    }));
    const total = entries.reduce((sum, entry) => sum + entry.value, 0);
    let offset = 0;
    return entries.map((entry) => {
      const fraction = total > 0 ? entry.value / total : 0;
      const length = fraction * 100;
      const segment = { ...entry, total, percent: Math.round(fraction * 100), offset, length };
      offset += length;
      return segment;
    });
  }, [coverageCategoryBuckets]);

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

  const fetchCases = async () => {
    if (!canLoad) {
      return;
    }
    setCasesLoading(true);
    setCasesError('');
    try {
      const response = await axios.get(`${API}/knowledge-engine/case-studies`, {
        headers: getAuthHeaders(),
      });
      setCases(response.data.cases || []);
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to load case studies';
      setCasesError(message);
      toast.error(message);
    } finally {
      setCasesLoading(false);
    }
  };

  const fetchCoverage = async () => {
    if (!canLoad) {
      return;
    }
    setCoverageLoading(true);
    setCoverageError('');
    try {
      const response = await axios.get(`${API}/knowledge-engine/coverage`, {
        headers: getAuthHeaders(),
      });
      setCoverageData(response.data || {});
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to load coverage dashboard';
      setCoverageError(message);
      toast.error(message);
    } finally {
      setCoverageLoading(false);
    }
  };

  const fetchVoices = async () => {
    if (!canLoad) {
      return;
    }
    setVoicesLoading(true);
    setVoicesError('');
    try {
      const response = await axios.get(`${API}/knowledge-engine/voices`, {
        headers: getAuthHeaders(),
      });
      setVoices(normalizeVoices(response.data));
    } catch (error) {
      const message = error.response?.data?.detail || 'Failed to load voice profiles';
      setVoicesError(message);
      toast.error(message);
    } finally {
      setVoicesLoading(false);
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

  useEffect(() => {
    if (activeTab === 'cases' && canLoad && cases.length === 0 && !casesLoading) {
      fetchCases();
    }
  }, [activeTab, canLoad, cases.length, casesLoading]);

  useEffect(() => {
    if (activeTab === 'coverage' && canLoad && !coverageData && !coverageLoading) {
      fetchCoverage();
    }
  }, [activeTab, canLoad, coverageData, coverageLoading]);

  useEffect(() => {
    if (activeTab === 'voices' && canLoad && voices.length === 0 && !voicesLoading) {
      fetchVoices();
    }
  }, [activeTab, canLoad, voices.length, voicesLoading]);

  const handleLoadRules = async () => {
    const nextFilters = {
      science_id: scienceInput.trim() || undefined,
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

  const handleRunValidation = async (batchId) => {
    setValidationBatchId(batchId);
    try {
      const headers = getAuthHeaders();
      const response = await fetch(
        `${BACKEND_URL}/api/knowledge/validate-batch?batch_id=${encodeURIComponent(batchId)}`,
        { method: 'POST', headers }
      );
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.detail || data?.message || 'Validation request failed');
      }
      toast.success(data.message || 'Validation started - check Rules Browser in ~3 minutes.');
    } catch (error) {
      toast.error(`Validation request failed: ${error.message}`);
    } finally {
      setValidationBatchId(null);
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

  const handleCaseImportFile = async (event) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    try {
      const payload = await readJsonFile(file);
      const normalized = normalizeImportedCases(payload);
      if (normalized.length === 0) {
        throw new Error('No case study rows found in JSON');
      }
      const validRows = normalized.filter(
        (entry) => entry?.case_id && entry?.subject && entry?.birth_data?.date
      );
      if (validRows.length === 0) {
        throw new Error('JSON does not match expected case study structure');
      }
      setCaseImportPreview(validRows);
      setCaseImportFileName(file.name);
      toast.success(`${validRows.length} case study rows ready to import`);
    } catch (error) {
      setCaseImportPreview([]);
      setCaseImportFileName('');
      toast.error(error.message || 'Invalid case study JSON file');
    } finally {
      event.target.value = '';
    }
  };

  const handleConfirmCaseImport = async () => {
    if (caseImportPreview.length === 0) {
      toast.error('Upload a valid JSON file first');
      return;
    }
    setImportingCases(true);
    try {
      const response = await axios.post(
        `${API}/knowledge-engine/case-studies/import`,
        { cases: caseImportPreview },
        { headers: getAuthHeaders() }
      );
      toast.success(
        response.data?.message ||
          `${response.data?.cases_imported || caseImportPreview.length} cases imported`
      );
      setShowImportModal(false);
      setCaseImportPreview([]);
      setCaseImportFileName('');
      await fetchCases();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to import case studies');
    } finally {
      setImportingCases(false);
    }
  };

  const handleRunCaseValidation = async () => {
    setValidatingCases(true);
    try {
      const response = await axios.post(
        `${API}/knowledge-engine/case-studies/validate-batch`,
        {},
        { headers: getAuthHeaders() }
      );
      toast.success(
        response.data?.message || 'Batch validation started. Check back in a few minutes.'
      );
      setShowValidationModal(false);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to start case study validation');
    } finally {
      setValidatingCases(false);
    }
  };

  const handleGenerateTestReport = async () => {
    setTestLoading(true);
    setTestError('');
    setTestResult(null);
    try {
      const response = await axios.post(
        `${API}/knowledge-engine/test`,
        testForm,
        { headers: getAuthHeaders() }
      );
      setTestResult(response.data || {});
      setTestOutputTab('narrative');
    } catch (error) {
      const message = error.response?.data?.detail || error.message || 'Failed to generate test report';
      setTestError(message);
      toast.error(message);
    } finally {
      setTestLoading(false);
    }
  };

  const startEditingVoice = (voice) => {
    setEditingVoiceId(voice.voice_id);
    setVoiceDrafts((current) => ({
      ...current,
      [voice.voice_id]: {
        display_name: voice.display_name || '',
        description: voice.description || '',
        style_tokens: (voice.style_tokens || []).join(', '),
        sample_phrase: voice.sample_phrase || '',
      },
    }));
  };

  const handleVoiceDraftChange = (voiceId, field, value) => {
    setVoiceDrafts((current) => ({
      ...current,
      [voiceId]: {
        ...(current[voiceId] || {}),
        [field]: value,
      },
    }));
  };

  const handleSaveVoice = async (voiceId) => {
    const draft = voiceDrafts[voiceId];
    if (!draft) {
      return;
    }
    setSavingVoiceId(voiceId);
    try {
      const payload = {
        display_name: draft.display_name,
        description: draft.description,
        style_tokens: draft.style_tokens
          .split(',')
          .map((item) => item.trim())
          .filter(Boolean),
        sample_phrase: draft.sample_phrase,
      };
      await axios.put(`${API}/knowledge-engine/voices/${voiceId}`, payload, {
        headers: getAuthHeaders(),
      });
      setVoices((current) =>
        current.map((voice) =>
          voice.voice_id === voiceId
            ? { ...voice, ...payload }
            : voice
        )
      );
      setEditingVoiceId(null);
      toast.success('Voice profile updated');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update voice profile');
    } finally {
      setSavingVoiceId(null);
    }
  };

  if (authLoading) {
    return <div className="text-center py-8 text-gray-400">Loading...</div>;
  }

  function ValidationBadge({ rule }) {
    const status = rule.approval_status;
    const reason = rule.validation?.flag_reason || rule.validation?.contradiction_summary || '';
    const map = {
      auto_approved: {
        label: 'Auto-approved',
        color: 'bg-green-500/15 text-green-400 border-green-500/30',
      },
      pending_human_review: {
        label: 'Spot-check',
        color: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
      },
      flagged: {
        label: 'Flagged',
        color: 'bg-red-500/15 text-red-400 border-red-500/30',
      },
      rejected: {
        label: 'Rejected',
        color: 'bg-zinc-500/15 text-zinc-400 border-zinc-500/30',
      },
      pending_review: {
        label: 'Pending',
        color: 'bg-blue-500/15 text-blue-400 border-blue-500/30',
      },
      approved: {
        label: 'Approved',
        color: 'bg-green-500/15 text-green-400 border-green-500/30',
      },
    };
    const cfg = map[status] || map.pending_review;
    return (
      <span
        className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${cfg.color}`}
        title={reason || undefined}
      >
        {cfg.label}
      </span>
    );
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
            {activeTab === 'cases' && `${cases.length} case studies`}
            {activeTab === 'coverage' && 'Coverage monitor'}
            {activeTab === 'test' && 'Engine test harness'}
            {activeTab === 'voices' && `${voices.length} voice profiles`}
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
                    Validation Status
                  </label>
                  <select
                    value={statusFilter}
                    onChange={(event) => setStatusFilter(event.target.value)}
                    className="w-full rounded-md border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-white focus:outline-none"
                  >
                    <option value="">All statuses</option>
                    <option value="pending_review">Pending</option>
                    <option value="auto_approved">Auto-approved</option>
                    <option value="pending_human_review">Spot-check</option>
                    <option value="flagged">Flagged</option>
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
                    {displayedRules.map((rule) => {
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
                              <ValidationBadge rule={rule} />
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
                    {displayedRules.length === 0 && (
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
                    <div className="flex gap-2 flex-wrap">
                      <button
                        onClick={() => handleRunValidation(batch.batch_id)}
                        disabled={validationBatchId === batch.batch_id}
                        className="rounded-lg border border-indigo-500/30 bg-indigo-500/10 px-3 py-1.5 text-xs text-indigo-400 hover:bg-indigo-500/20 disabled:opacity-60"
                      >
                        {validationBatchId === batch.batch_id ? 'Starting...' : 'Run Validation'}
                      </button>
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

        {activeTab === 'coverage' && (
          <div className="space-y-4">
            {coverageError ? (
              <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4">
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="mt-0.5 h-4 w-4 text-red-400" />
                    <div>
                      <p className="text-sm font-medium text-red-300">Coverage dashboard failed to load</p>
                      <p className="mt-1 text-sm text-red-200/80">{coverageError}</p>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={fetchCoverage}
                    className="border-red-400/30 text-red-300 hover:bg-red-500/10"
                  >
                    Retry
                  </Button>
                </div>
              </div>
            ) : coverageLoading && !coverageData ? (
              <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-8">
                <div className="flex items-center justify-center gap-3 text-gray-400">
                  <Loader2 className="h-5 w-5 animate-spin" />
                  <span>Loading coverage dashboard...</span>
                </div>
              </Card>
            ) : (
              <>
                <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
                  <div className="flex items-center gap-2 mb-4">
                    <BarChart3 className="h-4 w-4 text-gold" />
                    <h3 className="text-lg font-semibold text-white">House × Planet Heatmap</h3>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="min-w-[760px] border-separate border-spacing-2">
                      <thead>
                        <tr>
                          <th className="px-2 py-1 text-left text-xs uppercase tracking-wide text-gray-400">House</th>
                          {['Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury', 'Ketu', 'Venus'].map((planet) => (
                            <th key={planet} className="px-2 py-1 text-center text-xs uppercase tracking-wide text-gray-400">
                              {planet}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {Array.from({ length: 12 }, (_, index) => index + 1).map((house) => (
                          <tr key={`heatmap-house-${house}`}>
                            <td className="px-2 py-1 text-sm text-gray-300">House {house}</td>
                            {['Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury', 'Ketu', 'Venus'].map((planet) => {
                              const cell = (coverageData?.heatmap || []).find(
                                (entry) => entry.house === house && entry.planet === planet
                              );
                              const tier = cell?.tier || 'gap';
                              const color =
                                tier === 'covered'
                                  ? 'bg-emerald-500/70'
                                  : tier === 'sparse'
                                    ? 'bg-amber-400/70'
                                    : 'bg-red-500/70';
                              return (
                                <td key={`${house}-${planet}`} className="px-2 py-1">
                                  <div
                                    className={`mx-auto h-8 w-8 rounded-md border border-black/20 ${color}`}
                                    title={`${planet} in House ${house} — ${cell?.count || 0} rules`}
                                  />
                                </td>
                              );
                            })}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </Card>

                <div className="grid gap-4 lg:grid-cols-[1.05fr_1fr]">
                  <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
                    <h3 className="text-lg font-semibold text-white">Category Coverage</h3>
                    <div className="mt-4 flex flex-col items-center gap-4">
                      <svg viewBox="0 0 120 120" className="h-48 w-48">
                        <circle
                          cx="60"
                          cy="60"
                          r="42"
                          fill="transparent"
                          stroke="rgba(255,255,255,0.08)"
                          strokeWidth="14"
                        />
                        {coverageDonutSegments.map((segment) =>
                          segment.length > 0 ? (
                            <circle
                              key={segment.key}
                              cx="60"
                              cy="60"
                              r="42"
                              fill="transparent"
                              stroke={segment.color}
                              strokeWidth="14"
                              strokeDasharray={`${segment.length} ${100 - segment.length}`}
                              strokeDashoffset={25 - segment.offset}
                              pathLength="100"
                              transform="rotate(-90 60 60)"
                            />
                          ) : null
                        )}
                        <text x="60" y="56" textAnchor="middle" className="fill-white text-[12px] font-semibold">
                          {(coverageDonutSegments[0]?.total || 0)}
                        </text>
                        <text x="60" y="72" textAnchor="middle" className="fill-[#9ca3af] text-[8px] uppercase tracking-[1px]">
                          categories
                        </text>
                      </svg>
                      <div className="grid w-full gap-2">
                        {coverageDonutSegments.map((segment) => (
                          <div key={`legend-${segment.key}`} className="flex items-center justify-between gap-3 text-sm">
                            <div className="flex items-center gap-2">
                              <span className="inline-block h-2.5 w-2.5 rounded-full" style={{ backgroundColor: segment.color }} />
                              <span className="capitalize text-gray-200">{segment.key}</span>
                            </div>
                            <span className="text-gray-400">
                              {segment.value} ({segment.percent}%)
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </Card>

                  <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
                    <h3 className="text-lg font-semibold text-white">Source Coverage</h3>
                    <div className="mt-4 space-y-3">
                      {Object.entries(coverageData?.source_counts || {})
                        .sort(([, countA], [, countB]) => Number(countB) - Number(countA))
                        .map(([source, count], index, entries) => {
                          const max = Number(entries[0]?.[1] || 1);
                          const width = max > 0 ? `${(Number(count) / max) * 100}%` : '0%';
                          return (
                            <div key={source} className="grid grid-cols-[140px_1fr_48px] items-center gap-3">
                              <span className="truncate text-sm text-gray-200">{source}</span>
                              <div className="h-3 rounded-full bg-white/5">
                                <div className="h-3 rounded-full bg-gold/60" style={{ width }} />
                              </div>
                              <span className="text-right text-sm text-gray-400">{count}</span>
                            </div>
                          );
                        })}
                      {Object.keys(coverageData?.source_counts || {}).length === 0 && (
                        <p className="text-sm text-gray-500">No source counts available.</p>
                      )}
                    </div>
                  </Card>
                </div>

                <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
                  <h3 className="text-lg font-semibold text-white">Gap Analysis</h3>
                  <div className="mt-4 space-y-2">
                    {(coverageData?.gap_analysis || [])
                      .slice()
                      .sort((a, b) => Number(a.count) - Number(b.count))
                      .slice(0, 10)
                      .map((gap, index) => (
                        <div
                          key={`gap-${gap.house}-${gap.planet}-${index}`}
                          className="flex items-center justify-between gap-3 rounded-xl border border-gold/10 bg-black/10 px-4 py-3"
                        >
                          <span className="text-sm text-gray-200">
                            House {gap.house} × {gap.planet} — {gap.count} rules
                          </span>
                          <span className="inline-flex rounded-full border border-red-500/30 bg-red-500/15 px-2 py-0.5 text-xs font-medium text-red-400">
                            GAP
                          </span>
                        </div>
                      ))}
                    {(coverageData?.gap_analysis || []).length === 0 && (
                      <p className="text-sm text-gray-500">No gap analysis available.</p>
                    )}
                  </div>
                </Card>
              </>
            )}
          </div>
        )}

        {activeTab === 'test' && (
          <div className="grid gap-4 xl:grid-cols-[0.85fr_1.15fr]">
            <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
              <div className="flex items-center gap-2 mb-4">
                <Bug className="h-4 w-4 text-gold" />
                <h3 className="text-lg font-semibold text-white">Test Console</h3>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Date</label>
                  <Input
                    value={testForm.birth_date}
                    onChange={(event) => setTestForm((current) => ({ ...current, birth_date: event.target.value }))}
                    placeholder="YYYY-MM-DD"
                    className="bg-card border-gold/20 text-foreground"
                  />
                </div>
                <div>
                  <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Time</label>
                  <Input
                    value={testForm.birth_time}
                    onChange={(event) => setTestForm((current) => ({ ...current, birth_time: event.target.value }))}
                    placeholder="HH:MM"
                    className="bg-card border-gold/20 text-foreground"
                  />
                </div>
                <div>
                  <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Place</label>
                  <Input
                    value={testForm.birth_place}
                    onChange={(event) => setTestForm((current) => ({ ...current, birth_place: event.target.value }))}
                    placeholder="City, Country"
                    className="bg-card border-gold/20 text-foreground"
                  />
                </div>
                <div>
                  <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Report Type</label>
                  <select
                    value={testForm.report_type}
                    onChange={(event) => setTestForm((current) => ({ ...current, report_type: event.target.value }))}
                    className="w-full rounded-lg border border-gold/20 bg-card px-3 py-2 text-sm text-foreground"
                  >
                    <option value="career">career</option>
                    <option value="health">health</option>
                    <option value="relationships">relationships</option>
                    <option value="wealth">wealth</option>
                    <option value="spirituality">spirituality</option>
                    <option value="longevity">longevity</option>
                    <option value="comprehensive">comprehensive</option>
                  </select>
                </div>
                <div>
                  <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Voice Blend</label>
                  <select
                    value={testForm.voice_blend}
                    onChange={(event) => setTestForm((current) => ({ ...current, voice_blend: event.target.value }))}
                    className="w-full rounded-lg border border-gold/20 bg-card px-3 py-2 text-sm text-foreground"
                  >
                    <option value="classical">classical</option>
                    <option value="modern_analytical">modern_analytical</option>
                    <option value="classical+modern_analytical">classical+modern_analytical</option>
                    <option value="empathetic">empathetic</option>
                  </select>
                </div>
                <div>
                  <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Depth</label>
                  <select
                    value={testForm.depth}
                    onChange={(event) => setTestForm((current) => ({ ...current, depth: event.target.value }))}
                    className="w-full rounded-lg border border-gold/20 bg-card px-3 py-2 text-sm text-foreground"
                  >
                    <option value="summary">summary</option>
                    <option value="detailed">detailed</option>
                    <option value="full">full</option>
                  </select>
                </div>
                <Button
                  onClick={handleGenerateTestReport}
                  disabled={testLoading}
                  className="w-full bg-gold text-background hover:bg-gold/90"
                >
                  {testLoading ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    <Play className="mr-2 h-4 w-4" />
                  )}
                  Generate Report
                </Button>
              </div>
            </Card>

            <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
              <div className="flex items-center justify-between gap-3 flex-wrap mb-4">
                <h3 className="text-lg font-semibold text-white">Output</h3>
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setTestOutputTab('narrative')}
                    className={
                      testOutputTab === 'narrative'
                        ? 'border-gold/40 bg-gold/10 text-gold'
                        : 'border-gold/20 text-gray-300 hover:bg-gold/10'
                    }
                  >
                    Narrative
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setTestOutputTab('matched')}
                    className={
                      testOutputTab === 'matched'
                        ? 'border-gold/40 bg-gold/10 text-gold'
                        : 'border-gold/20 text-gray-300 hover:bg-gold/10'
                    }
                  >
                    Matched Rules
                  </Button>
                </div>
              </div>

              {testLoading ? (
                <div className="flex min-h-[320px] items-center justify-center gap-3 text-gray-400">
                  <Loader2 className="h-5 w-5 animate-spin" />
                  <span>Generating report…</span>
                </div>
              ) : testError ? (
                <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4">
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div>
                      <p className="text-sm font-medium text-red-300">Engine error: {testError}</p>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={handleGenerateTestReport}
                      className="border-red-400/30 text-red-300 hover:bg-red-500/10"
                    >
                      Retry
                    </Button>
                  </div>
                </div>
              ) : !testResult ? (
                <div className="flex min-h-[320px] items-center justify-center text-sm text-gray-500">
                  Fill in the test inputs and generate a report to inspect engine output.
                </div>
              ) : testOutputTab === 'narrative' ? (
                <div className="space-y-4">
                  <div className="min-h-[240px] whitespace-pre-wrap rounded-xl border border-gold/10 bg-black/10 p-4 text-sm leading-relaxed text-gray-200">
                    {testResult.narrative || 'No narrative returned.'}
                  </div>
                  <div className="rounded-xl border border-gold/10 bg-black/10 p-4">
                    <div className="flex items-center gap-2 mb-3">
                      <BookOpen className="h-4 w-4 text-gold" />
                      <p className="text-sm font-medium text-white">Citation Trail</p>
                    </div>
                    <div className="space-y-2">
                      {(testResult.citations || []).map((citation, index) => (
                        <p key={`citation-${index}`} className="text-xs text-gray-400">
                          Para {Number(citation.paragraph_index || 0) + 1}: {(citation.books || []).join(', ') || 'Unknown source'}
                        </p>
                      ))}
                      {(testResult.citations || []).length === 0 && (
                        <p className="text-xs text-gray-500">No citations returned.</p>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full min-w-[760px]">
                    <thead>
                      <tr className="text-left text-xs uppercase tracking-wide text-gray-400">
                        <th className="pb-3">Rule ID</th>
                        <th className="pb-3">Life Domain</th>
                        <th className="pb-3">Claim Axis</th>
                        <th className="pb-3">Effective Confidence</th>
                        <th className="pb-3">Tranche Adjusted</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(testResult.matched_rules || []).map((rule) => {
                        const confidence = Number(rule.effective_confidence || 0);
                        const width = `${Math.max(0, Math.min(100, confidence * 100))}%`;
                        return (
                          <tr key={rule.rule_id} className="border-t border-gold/10 text-sm text-gray-200">
                            <td className="py-3 pr-3 font-mono text-xs">{truncateId(rule.rule_id, 18)}</td>
                            <td className="py-3 pr-3">{rule.life_domain || '—'}</td>
                            <td className="py-3 pr-3">{rule.claim_axis || '—'}</td>
                            <td className="py-3 pr-3">
                              <div className="flex min-w-[180px] items-center gap-3">
                                <div className="h-2 flex-1 rounded-full bg-white/5">
                                  <div className="h-2 rounded-full bg-gold" style={{ width }} />
                                </div>
                                <span className="text-xs text-gray-400">{confidence.toFixed(2)}</span>
                              </div>
                            </td>
                            <td className="py-3 pr-3">
                              {rule._tranche_adjusted ? (
                                <CheckCircle2 className="h-4 w-4 text-green-400" />
                              ) : (
                                <span className="text-gray-500">—</span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                      {(testResult.matched_rules || []).length === 0 && (
                        <tr>
                          <td colSpan={5} className="py-8 text-center text-sm text-gray-500">
                            No matched rules returned.
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              )}
            </Card>
          </div>
        )}

        {activeTab === 'voices' && (
          <div className="space-y-4">
            {voicesError ? (
              <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4">
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="mt-0.5 h-4 w-4 text-red-400" />
                    <div>
                      <p className="text-sm font-medium text-red-300">Voice profiles failed to load</p>
                      <p className="mt-1 text-sm text-red-200/80">{voicesError}</p>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={fetchVoices}
                    className="border-red-400/30 text-red-300 hover:bg-red-500/10"
                  >
                    Retry
                  </Button>
                </div>
              </div>
            ) : voicesLoading && voices.length === 0 ? (
              <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-8">
                <div className="flex items-center justify-center gap-3 text-gray-400">
                  <Loader2 className="h-5 w-5 animate-spin" />
                  <span>Loading voice profiles...</span>
                </div>
              </Card>
            ) : (
              <div className="grid gap-4 xl:grid-cols-2">
                {voices.map((voice) => {
                  const isEditing = editingVoiceId === voice.voice_id;
                  const draft = voiceDrafts[voice.voice_id] || {};
                  return (
                    <Card
                      key={voice.voice_id}
                      className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <div className="flex items-center gap-2">
                            <Volume2 className="h-4 w-4 text-gold" />
                            <h3 className="text-lg font-semibold text-white">{voice.display_name}</h3>
                          </div>
                          <p className="mt-2 text-sm text-gray-300">{voice.description}</p>
                        </div>
                        {!isEditing && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => startEditingVoice(voice)}
                            className="border-gold/40 text-gold hover:bg-gold/10"
                          >
                            <Pencil className="mr-2 h-3.5 w-3.5" />
                            Edit
                          </Button>
                        )}
                      </div>

                      <div className="mt-4 flex flex-wrap gap-2">
                        {(voice.style_tokens || []).map((token) => (
                          <span
                            key={`${voice.voice_id}-${token}`}
                            className="inline-flex rounded-full bg-white/5 px-2 py-0.5 text-xs text-gray-300"
                          >
                            {token}
                          </span>
                        ))}
                      </div>

                      <p className="mt-4 italic text-sm text-gray-400">{voice.sample_phrase}</p>

                      {isEditing && (
                        <div className="mt-5 space-y-4 border-t border-gold/10 pt-4">
                          <div>
                            <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Display Name</label>
                            <Input
                              value={draft.display_name || ''}
                              onChange={(event) => handleVoiceDraftChange(voice.voice_id, 'display_name', event.target.value)}
                              className="bg-card border-gold/20 text-foreground"
                            />
                          </div>
                          <div>
                            <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Description</label>
                            <textarea
                              value={draft.description || ''}
                              onChange={(event) => handleVoiceDraftChange(voice.voice_id, 'description', event.target.value)}
                              rows={3}
                              className="w-full rounded-lg border border-gold/20 bg-card px-3 py-2 text-sm text-foreground"
                            />
                          </div>
                          <div>
                            <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Style Tokens</label>
                            <Input
                              value={draft.style_tokens || ''}
                              onChange={(event) => handleVoiceDraftChange(voice.voice_id, 'style_tokens', event.target.value)}
                              placeholder="formal, reverent, precise"
                              className="bg-card border-gold/20 text-foreground"
                            />
                          </div>
                          <div>
                            <label className="mb-2 block text-xs uppercase tracking-wide text-gray-400">Sample Phrase</label>
                            <textarea
                              value={draft.sample_phrase || ''}
                              onChange={(event) => handleVoiceDraftChange(voice.voice_id, 'sample_phrase', event.target.value)}
                              rows={3}
                              className="w-full rounded-lg border border-gold/20 bg-card px-3 py-2 text-sm text-foreground"
                            />
                          </div>
                          <div className="flex gap-2">
                            <Button
                              onClick={() => handleSaveVoice(voice.voice_id)}
                              disabled={savingVoiceId === voice.voice_id}
                              className="bg-gold text-background hover:bg-gold/90"
                            >
                              {savingVoiceId === voice.voice_id ? (
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                              ) : (
                                <Save className="mr-2 h-4 w-4" />
                              )}
                              Save
                            </Button>
                            <Button
                              variant="outline"
                              onClick={() => setEditingVoiceId(null)}
                              className="border-gold/40 text-gold hover:bg-gold/10"
                            >
                              Cancel
                            </Button>
                          </div>
                        </div>
                      )}
                    </Card>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {activeTab === 'cases' && (
          <div className="space-y-4">
            <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
              <div className="flex items-center justify-between gap-4 flex-wrap">
                <div className="flex items-center gap-3">
                  <div>
                    <h2 className="text-xl font-semibold text-white">Case Studies</h2>
                    <p className="text-sm text-gray-400 mt-1">
                      Review imported public-case validation data and monitor engine accuracy.
                    </p>
                  </div>
                  <span className="inline-flex rounded-full bg-gray-700 px-3 py-1 text-xs font-medium text-gray-200">
                    {cases.length}
                  </span>
                </div>
                <div className="flex gap-2 flex-wrap">
                  <button
                    onClick={() => setShowImportModal(true)}
                    className="rounded-lg border border-gold/40 px-3 py-2 text-sm text-gold hover:bg-gold/10"
                  >
                    Import Cases
                  </button>
                  <button
                    onClick={() => setShowValidationModal(true)}
                    className="rounded-lg bg-gold px-3 py-2 text-sm font-medium text-background hover:bg-gold/90"
                  >
                    Run Batch Validation
                  </button>
                </div>
              </div>
            </Card>

            <div className="grid gap-4 md:grid-cols-4">
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                <p className="text-xs uppercase tracking-wide text-gray-400">Total Cases</p>
                <p className="mt-2 text-2xl font-semibold text-white">{caseStats.total}</p>
              </div>
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                <p className="text-xs uppercase tracking-wide text-gray-400">Validated</p>
                <p className="mt-2 text-2xl font-semibold text-white">{caseStats.validated}</p>
              </div>
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                <p className="text-xs uppercase tracking-wide text-gray-400">Avg Accuracy</p>
                <p className="mt-2 text-2xl font-semibold text-white">
                  {caseStats.averageAccuracy === null ? '—' : `${caseStats.averageAccuracy}%`}
                </p>
              </div>
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                <p className="text-xs uppercase tracking-wide text-gray-400">Pending</p>
                <p className="mt-2 text-2xl font-semibold text-white">{caseStats.pending}</p>
              </div>
            </div>

            <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-4">
              <div className="flex items-center justify-between gap-3 flex-wrap">
                <div className="min-w-[260px] flex-1">
                  <Input
                    value={casesSearch}
                    onChange={(event) => setCasesSearch(event.target.value)}
                    placeholder="Search by case ID or subject"
                    className="bg-card border-gold/20 text-foreground"
                  />
                </div>
                <div className="min-w-[220px]">
                  <select
                    value={caseDomainFilter}
                    onChange={(event) => setCaseDomainFilter(event.target.value)}
                    className="w-full rounded-lg border border-gold/20 bg-card px-3 py-2 text-sm text-foreground"
                  >
                    <option value="">All domains</option>
                    <option value="career_status">career_status</option>
                    <option value="partnership">partnership</option>
                    <option value="health">health</option>
                    <option value="financial_security">financial_security</option>
                    <option value="spirituality">spirituality</option>
                  </select>
                </div>
              </div>
            </Card>

            {casesError ? (
              <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4">
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="mt-0.5 h-4 w-4 text-red-400" />
                    <div>
                      <p className="text-sm font-medium text-red-300">Failed to load case studies</p>
                      <p className="text-sm text-red-200/80 mt-1">{casesError}</p>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={fetchCases}
                    className="border-red-400/30 text-red-300 hover:bg-red-500/10"
                  >
                    Retry
                  </Button>
                </div>
              </div>
            ) : (
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm overflow-x-auto">
                <table className="w-full min-w-[1120px]">
                  <thead className="bg-black/20">
                    <tr className="text-left text-xs uppercase tracking-wide text-gray-400">
                      <th className="px-4 py-3">Case ID</th>
                      <th className="px-4 py-3">Subject</th>
                      <th className="px-4 py-3">Life Domain</th>
                      <th className="px-4 py-3">Data Quality</th>
                      <th className="px-4 py-3">Accuracy</th>
                      <th className="px-4 py-3">Validated</th>
                      <th className="px-4 py-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {casesLoading
                      ? Array.from({ length: 3 }).map((_, index) => (
                          <tr key={`case-skeleton-${index}`} className="border-t border-gold/10">
                            <td className="px-4 py-4"><div className="h-4 w-20 rounded bg-white/5" /></td>
                            <td className="px-4 py-4"><div className="h-4 w-44 rounded bg-white/5" /></td>
                            <td className="px-4 py-4"><div className="h-4 w-24 rounded bg-white/5" /></td>
                            <td className="px-4 py-4"><div className="h-4 w-16 rounded bg-white/5" /></td>
                            <td className="px-4 py-4"><div className="h-4 w-12 rounded bg-white/5" /></td>
                            <td className="px-4 py-4"><div className="h-4 w-10 rounded bg-white/5" /></td>
                            <td className="px-4 py-4"><div className="h-8 w-16 rounded bg-white/5" /></td>
                          </tr>
                        ))
                      : filteredCases.map((entry) => {
                          const isExpanded = expandedCaseId === entry.case_id;
                          const primaryOutcome = entry.known_outcomes?.[0] || {};
                          return (
                            <React.Fragment key={entry.case_id}>
                              <tr className="border-t border-gold/10 text-sm text-gray-200">
                                <td className="px-4 py-3 font-mono text-xs">{entry.case_id || '—'}</td>
                                <td className="px-4 py-3" title={entry.subject}>{truncateText(entry.subject, 28)}</td>
                                <td className="px-4 py-3">{primaryOutcome.life_domain || '—'}</td>
                                <td className="px-4 py-3">
                                  <span className={`inline-flex rounded-full border px-2 py-0.5 text-xs font-medium ${dataQualityBadge(entry.data_quality)}`}>
                                    {entry.data_quality || 'unknown'}
                                  </span>
                                </td>
                                <td className="px-4 py-3">{formatPercent(entry.accuracy_score)}</td>
                                <td className="px-4 py-3">
                                  {entry.validated ? (
                                    <CheckCircle2 className="h-4 w-4 text-green-400" />
                                  ) : (
                                    <X className="h-4 w-4 text-gray-500" />
                                  )}
                                </td>
                                <td className="px-4 py-3">
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() =>
                                      setExpandedCaseId((current) =>
                                        current === entry.case_id ? null : entry.case_id
                                      )
                                    }
                                    className="border-gold/30 text-gold hover:bg-gold/10"
                                  >
                                    View
                                    {isExpanded ? (
                                      <ChevronUp className="ml-1 h-3.5 w-3.5" />
                                    ) : (
                                      <ChevronDown className="ml-1 h-3.5 w-3.5" />
                                    )}
                                  </Button>
                                </td>
                              </tr>
                              {isExpanded && (
                                <tr className="border-t border-gold/10 bg-black/10">
                                  <td colSpan={7} className="px-4 py-4">
                                    <div className="space-y-4">
                                      <div className="grid gap-3 md:grid-cols-3">
                                        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                          <p className="text-xs uppercase tracking-wide text-gray-400">Birth Date</p>
                                          <p className="mt-1 text-sm text-white">{entry.birth_data?.date || '—'}</p>
                                        </div>
                                        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                          <p className="text-xs uppercase tracking-wide text-gray-400">Birth Time</p>
                                          <p className="mt-1 text-sm text-white">{entry.birth_data?.time || '—'}</p>
                                        </div>
                                        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                          <p className="text-xs uppercase tracking-wide text-gray-400">Birth Place</p>
                                          <p className="mt-1 text-sm text-white">{entry.birth_data?.place || '—'}</p>
                                        </div>
                                        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                          <p className="text-xs uppercase tracking-wide text-gray-400">Latitude</p>
                                          <p className="mt-1 text-sm text-white">{entry.birth_data?.latitude ?? '—'}</p>
                                        </div>
                                        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                          <p className="text-xs uppercase tracking-wide text-gray-400">Longitude</p>
                                          <p className="mt-1 text-sm text-white">{entry.birth_data?.longitude ?? '—'}</p>
                                        </div>
                                        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                          <p className="text-xs uppercase tracking-wide text-gray-400">Timezone</p>
                                          <p className="mt-1 text-sm text-white">{entry.birth_data?.timezone || '—'}</p>
                                        </div>
                                      </div>

                                      <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                        <h4 className="text-sm font-semibold text-white mb-3">Known Outcomes</h4>
                                        <div className="overflow-x-auto">
                                          <table className="w-full min-w-[760px]">
                                            <thead>
                                              <tr className="text-left text-xs uppercase tracking-wide text-gray-400">
                                                <th className="pb-2">Life Domain</th>
                                                <th className="pb-2">Claim Axis</th>
                                                <th className="pb-2">Outcome</th>
                                                <th className="pb-2">Timing</th>
                                                <th className="pb-2">Notes</th>
                                              </tr>
                                            </thead>
                                            <tbody>
                                              {(entry.known_outcomes || []).map((outcome, index) => (
                                                <tr key={`${entry.case_id}-outcome-${index}`} className="border-t border-gold/10 text-sm text-gray-200">
                                                  <td className="py-2 pr-3">{outcome.life_domain || '—'}</td>
                                                  <td className="py-2 pr-3">{outcome.claim_axis || '—'}</td>
                                                  <td className="py-2 pr-3">{outcome.outcome || '—'}</td>
                                                  <td className="py-2 pr-3">{outcome.timing || '—'}</td>
                                                  <td className="py-2 pr-3">{outcome.notes || '—'}</td>
                                                </tr>
                                              ))}
                                              {(entry.known_outcomes || []).length === 0 && (
                                                <tr>
                                                  <td colSpan={5} className="py-3 text-sm text-gray-500">
                                                    No known outcomes recorded.
                                                  </td>
                                                </tr>
                                              )}
                                            </tbody>
                                          </table>
                                        </div>
                                      </div>

                                      {(entry.engine_predictions || []).length > 0 && (
                                        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                                          <h4 className="text-sm font-semibold text-white mb-3">Engine Predictions</h4>
                                          <div className="overflow-x-auto">
                                            <table className="w-full min-w-[640px]">
                                              <thead>
                                                <tr className="text-left text-xs uppercase tracking-wide text-gray-400">
                                                  <th className="pb-2">Domain</th>
                                                  <th className="pb-2">Predicted Quality</th>
                                                  <th className="pb-2">Confidence</th>
                                                  <th className="pb-2">Match</th>
                                                </tr>
                                              </thead>
                                              <tbody>
                                                {entry.engine_predictions.map((prediction, index) => {
                                                  const matchValue =
                                                    prediction.match ??
                                                    prediction.is_match ??
                                                    prediction.correct ??
                                                    null;
                                                  return (
                                                    <tr key={`${entry.case_id}-prediction-${index}`} className="border-t border-gold/10 text-sm text-gray-200">
                                                      <td className="py-2 pr-3">{prediction.life_domain || prediction.domain || '—'}</td>
                                                      <td className="py-2 pr-3">
                                                        {prediction.predicted_quality ||
                                                          prediction.period_quality ||
                                                          prediction.predicted_outcome ||
                                                          '—'}
                                                      </td>
                                                      <td className="py-2 pr-3">{estimateConfidencePct(prediction)}</td>
                                                      <td className="py-2 pr-3">
                                                        {matchValue === true ? (
                                                          <CheckCircle2 className="h-4 w-4 text-green-400" />
                                                        ) : matchValue === false ? (
                                                          <X className="h-4 w-4 text-red-400" />
                                                        ) : (
                                                          <span className="text-gray-500">—</span>
                                                        )}
                                                      </td>
                                                    </tr>
                                                  );
                                                })}
                                              </tbody>
                                            </table>
                                          </div>
                                        </div>
                                      )}

                                      <div className="flex items-center gap-6 flex-wrap text-sm text-gray-300">
                                        <p>
                                          Accuracy score:{' '}
                                          <span className="font-medium text-white">{formatPercent(entry.accuracy_score)}</span>
                                        </p>
                                        <p>
                                          Validated:{' '}
                                          <span className={`font-medium ${entry.validated ? 'text-green-400' : 'text-gray-400'}`}>
                                            {entry.validated ? 'Yes' : 'No'}
                                          </span>
                                        </p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              )}
                            </React.Fragment>
                          );
                        })}
                    {!casesLoading && filteredCases.length === 0 && (
                      <tr>
                        <td colSpan={7} className="px-4 py-8 text-center text-gray-500">
                          No case studies found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {showImportModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
            <div className="w-full max-w-3xl rounded-xl border border-gold/20 bg-background shadow-xl">
              <div className="flex items-center justify-between border-b border-gold/10 px-6 py-4">
                <div>
                  <h3 className="text-lg font-semibold text-white">Import Cases</h3>
                  <p className="text-sm text-gray-400 mt-1">
                    Upload a JSON file, preview the rows, then import into the case study library.
                  </p>
                </div>
                <button onClick={() => setShowImportModal(false)} className="text-gray-400 hover:text-white">
                  <X className="h-5 w-5" />
                </button>
              </div>
              <div className="space-y-4 px-6 py-5">
                <label className="flex cursor-pointer items-center justify-center gap-3 rounded-xl border border-dashed border-gold/30 bg-gold/[0.04] px-4 py-6 text-sm text-gray-300 hover:bg-gold/[0.08]">
                  <Upload className="h-4 w-4 text-gold" />
                  <span>{caseImportFileName ? `Loaded: ${caseImportFileName}` : 'Upload JSON file'}</span>
                  <input type="file" accept="application/json,.json" className="hidden" onChange={handleCaseImportFile} />
                </label>

                <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
                  <div className="flex items-center gap-2">
                    <FileJson className="h-4 w-4 text-gold" />
                    <p className="text-sm font-medium text-white">Preview</p>
                  </div>
                  <div className="mt-3 max-h-72 overflow-auto">
                    {caseImportPreview.length === 0 ? (
                      <p className="text-sm text-gray-500">No file loaded yet.</p>
                    ) : (
                      <table className="w-full min-w-[640px]">
                        <thead>
                          <tr className="text-left text-xs uppercase tracking-wide text-gray-400">
                            <th className="pb-2">Case ID</th>
                            <th className="pb-2">Subject</th>
                            <th className="pb-2">Birth Date</th>
                            <th className="pb-2">Known Outcomes</th>
                          </tr>
                        </thead>
                        <tbody>
                          {caseImportPreview.map((entry) => (
                            <tr key={`preview-${entry.case_id}`} className="border-t border-gold/10 text-sm text-gray-200">
                              <td className="py-2 pr-3 font-mono text-xs">{entry.case_id}</td>
                              <td className="py-2 pr-3">{truncateText(entry.subject, 40)}</td>
                              <td className="py-2 pr-3">{entry.birth_data?.date || '—'}</td>
                              <td className="py-2 pr-3">{entry.known_outcomes?.length || 0}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-end gap-3 border-t border-gold/10 px-6 py-4">
                <Button
                  variant="outline"
                  onClick={() => setShowImportModal(false)}
                  className="border-gold/40 text-gold hover:bg-gold/10"
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleConfirmCaseImport}
                  disabled={importingCases || caseImportPreview.length === 0}
                  className="bg-gold text-background hover:bg-gold/90"
                >
                  {importingCases ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    <Upload className="mr-2 h-4 w-4" />
                  )}
                  Confirm Import
                </Button>
              </div>
            </div>
          </div>
        )}

        {showValidationModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
            <div className="w-full max-w-xl rounded-xl border border-gold/20 bg-background shadow-xl">
              <div className="flex items-center justify-between border-b border-gold/10 px-6 py-4">
                <div>
                  <h3 className="text-lg font-semibold text-white">Run Batch Validation</h3>
                  <p className="text-sm text-gray-400 mt-1">
                    This will run all unvalidated cases through the live engine.
                  </p>
                </div>
                <button onClick={() => setShowValidationModal(false)} className="text-gray-400 hover:text-white">
                  <X className="h-5 w-5" />
                </button>
              </div>
              <div className="space-y-4 px-6 py-5">
                <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4 text-sm text-gray-200">
                  <p>
                    Estimated time: approximately{' '}
                    <span className="font-semibold text-white">
                      {Math.ceil(caseStats.pending * 0.5)} minute{Math.ceil(caseStats.pending * 0.5) === 1 ? '' : 's'}
                    </span>
                    .
                  </p>
                  <p className="mt-2 text-gray-400">
                    The request returns immediately. Validation continues in the background, so results may take a few minutes to appear.
                  </p>
                </div>
              </div>
              <div className="flex items-center justify-end gap-3 border-t border-gold/10 px-6 py-4">
                <Button
                  variant="outline"
                  onClick={() => setShowValidationModal(false)}
                  className="border-gold/40 text-gold hover:bg-gold/10"
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleRunCaseValidation}
                  disabled={validatingCases}
                  className="bg-gold text-background hover:bg-gold/90"
                >
                  {validatingCases ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    <FlaskConical className="mr-2 h-4 w-4" />
                  )}
                  Start Validation
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default LibraryConsolePage;
