import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Loader2, PlusCircle, RefreshCw, Target, Trash2 } from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const defaultLead = {
  company_name: '',
  website: '',
  industry: 'other',
  country: 'India',
  contact_name: '',
  contact_email: '',
  contact_phone: '',
  stage: 'discovered',
  alignment_score: 50,
  deal_value_inr: 0,
  partnership_type: 'other',
  notes: '',
  next_action: '',
  next_action_date: '',
};

const stageBadge = (stage) => ({
  discovered: 'bg-gray-500/20 text-gray-300',
  contacted: 'bg-blue-500/20 text-blue-400',
  qualified: 'bg-yellow-500/20 text-yellow-400',
  proposal_sent: 'bg-purple-500/20 text-purple-400',
  closed_won: 'bg-green-500/20 text-green-400',
  closed_lost: 'bg-red-500/20 text-red-400',
}[stage] || 'bg-gray-500/20 text-gray-300');

export const SalesLeadsTab = ({ getAuthHeaders }) => {
  const [summary, setSummary] = useState(null);
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [editingLeadId, setEditingLeadId] = useState(null);
  const [form, setForm] = useState(defaultLead);
  const [filters, setFilters] = useState({ stage: 'all', industry: 'all', search: '' });

  const fetchSummary = async () => {
    const res = await axios.get(`${API}/admin/sales-leads/summary`, { headers: getAuthHeaders() });
    setSummary(res.data);
  };

  const fetchLeads = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams(filters).toString();
      const res = await axios.get(`${API}/admin/sales-leads?${params}`, { headers: getAuthHeaders() });
      setLeads(res.data.leads || []);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to load leads');
    } finally {
      setLoading(false);
    }
  };

  const refreshAll = async () => {
    try {
      await Promise.all([fetchSummary(), fetchLeads()]);
    } catch {}
  };

  useEffect(() => {
    refreshAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    fetchLeads();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.stage, filters.industry, filters.search]);

  const resetForm = () => {
    setEditingLeadId(null);
    setForm(defaultLead);
  };

  const openEdit = (lead) => {
    setEditingLeadId(lead.lead_id);
    setForm({
      ...defaultLead,
      ...lead,
      next_action_date: lead.next_action_date ? lead.next_action_date.slice(0, 16) : '',
    });
  };

  const saveLead = async () => {
    if (!form.company_name.trim()) {
      toast.error('Company Name is required');
      return;
    }
    setSaving(true);
    try {
      const payload = {
        ...form,
        alignment_score: Number(form.alignment_score),
        deal_value_inr: Number(form.deal_value_inr),
        next_action_date: form.next_action_date ? new Date(form.next_action_date).toISOString() : null,
      };
      if (editingLeadId) {
        await axios.put(`${API}/admin/sales-leads/${editingLeadId}`, payload, { headers: getAuthHeaders() });
        toast.success('Lead updated');
      } else {
        await axios.post(`${API}/admin/sales-leads`, payload, { headers: getAuthHeaders() });
        toast.success('Lead created');
      }
      resetForm();
      refreshAll();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save lead');
    } finally {
      setSaving(false);
    }
  };

  const deleteLead = async (leadId) => {
    if (!window.confirm('Soft-delete this lead?')) return;
    try {
      await axios.delete(`${API}/admin/sales-leads/${leadId}`, { headers: getAuthHeaders() });
      toast.success('Lead removed');
      refreshAll();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to delete lead');
    }
  };

  const quickStageUpdate = async (leadId, stage) => {
    try {
      await axios.put(`${API}/admin/sales-leads/${leadId}`, { stage }, { headers: getAuthHeaders() });
      setLeads((prev) => prev.map((lead) => (lead.lead_id === leadId ? { ...lead, stage } : lead)));
      fetchSummary();
      toast.success('Stage updated');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to update stage');
    }
  };

  const stageCards = useMemo(() => summary?.by_stage || {}, [summary]);

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Target className="h-4 w-4 text-gold" />
            B2B Sales Leads
          </h3>
          <p className="text-xs text-gray-400 mt-1">Manual lead pipeline for high-fit partner outreach.</p>
        </div>
        <Button onClick={refreshAll} variant="outline" size="sm" className="border-gray-600 text-gray-300">
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
        </Button>
      </div>

      <div className="grid grid-cols-2 xl:grid-cols-6 gap-3">
        {[
          ['discovered', 'Discovered'],
          ['contacted', 'Contacted'],
          ['qualified', 'Qualified'],
          ['proposal_sent', 'Proposal'],
          ['closed_won', 'Won'],
          ['closed_lost', 'Lost'],
        ].map(([key, label]) => (
          <Card key={key} className="p-4 bg-gray-800 border-gray-700">
            <div className="text-xs uppercase tracking-wide text-gray-400">{label}</div>
            <div className="text-2xl font-bold text-white mt-2">{stageCards?.[key] ?? 0}</div>
          </Card>
        ))}
      </div>

      <Card className="p-4 bg-gray-800 border-gray-700">
        <div className="text-sm text-gray-300">
          Pipeline Value: <span className="text-gold font-semibold">₹{(summary?.total_pipeline_value_inr || 0).toLocaleString()}/month est.</span>
          <span className="ml-4 text-gray-400">Avg Alignment Score: {summary?.avg_alignment_score ?? 0}</span>
        </div>
      </Card>

      <div className="grid grid-cols-1 xl:grid-cols-[1.6fr_1fr] gap-5">
        <Card className="p-5 bg-gray-800 border-gray-700">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3 mb-4">
            <div className="flex flex-wrap gap-2">
              <select value={filters.stage} onChange={(e) => setFilters((prev) => ({ ...prev, stage: e.target.value }))} className="bg-gray-700 border border-gray-600 rounded-md text-white text-sm px-3 py-2">
                <option value="all">All stages</option>
                <option value="discovered">Discovered</option>
                <option value="contacted">Contacted</option>
                <option value="qualified">Qualified</option>
                <option value="proposal_sent">Proposal Sent</option>
                <option value="closed_won">Closed Won</option>
                <option value="closed_lost">Closed Lost</option>
              </select>
              <select value={filters.industry} onChange={(e) => setFilters((prev) => ({ ...prev, industry: e.target.value }))} className="bg-gray-700 border border-gray-600 rounded-md text-white text-sm px-3 py-2">
                <option value="all">All industries</option>
                <option value="yoga_wellness">Yoga / Wellness</option>
                <option value="matrimony">Matrimony</option>
                <option value="astrology_portal">Astrology Portal</option>
                <option value="news_media">News / Media</option>
                <option value="app">App</option>
                <option value="other">Other</option>
              </select>
            </div>
            <Input
              value={filters.search}
              onChange={(e) => setFilters((prev) => ({ ...prev, search: e.target.value }))}
              placeholder="Search by company or contact"
              className="bg-gray-700 border-gray-600 text-white lg:max-w-xs"
            />
          </div>

          {loading && !leads.length ? (
            <div className="text-gray-400 text-sm flex items-center gap-2 py-8 justify-center">
              <Loader2 className="h-4 w-4 animate-spin" /> Loading leads...
            </div>
          ) : leads.length === 0 ? (
            <p className="text-gray-500 text-sm text-center py-8">No leads yet.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-400 border-b border-gray-700">
                    <th className="py-3 pr-4">Company</th>
                    <th className="py-3 pr-4">Industry</th>
                    <th className="py-3 pr-4">Stage</th>
                    <th className="py-3 pr-4">Score</th>
                    <th className="py-3 pr-4">Deal ₹/mo</th>
                    <th className="py-3 pr-4">Next Action</th>
                    <th className="py-3 pr-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map((lead) => (
                    <tr key={lead.lead_id} className="border-b border-gray-800 align-top">
                      <td className="py-3 pr-4">
                        <div className="text-white font-medium">{lead.company_name}</div>
                        <div className="text-xs text-gray-400">{lead.website || '--'}</div>
                      </td>
                      <td className="py-3 pr-4 text-gray-300">{lead.industry}</td>
                      <td className="py-3 pr-4">
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-1 rounded text-xs capitalize ${stageBadge(lead.stage)}`}>{lead.stage.replace('_', ' ')}</span>
                          <select
                            value={lead.stage}
                            onChange={(e) => quickStageUpdate(lead.lead_id, e.target.value)}
                            className="bg-gray-700 border border-gray-600 rounded text-white text-xs px-2 py-1"
                          >
                            <option value="discovered">Discovered</option>
                            <option value="contacted">Contacted</option>
                            <option value="qualified">Qualified</option>
                            <option value="proposal_sent">Proposal Sent</option>
                            <option value="closed_won">Closed Won</option>
                            <option value="closed_lost">Closed Lost</option>
                          </select>
                        </div>
                      </td>
                      <td className="py-3 pr-4 text-gray-300">{lead.alignment_score}</td>
                      <td className="py-3 pr-4 text-gray-300">₹{Number(lead.deal_value_inr || 0).toLocaleString()}</td>
                      <td className="py-3 pr-4 text-gray-300">
                        <div>{lead.next_action || '--'}</div>
                        <div className="text-xs text-gray-500">{lead.next_action_date ? new Date(lead.next_action_date).toLocaleDateString('en-IN') : ''}</div>
                      </td>
                      <td className="py-3 pr-4">
                        <div className="flex gap-2">
                          <Button size="sm" variant="outline" className="border-gray-600 text-gray-300" onClick={() => openEdit(lead)}>
                            Edit
                          </Button>
                          <Button size="sm" variant="outline" className="border-red-700/50 text-red-400" onClick={() => deleteLead(lead.lead_id)}>
                            <Trash2 className="h-3.5 w-3.5" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>

        <Card className="p-5 bg-gray-800 border-gray-700">
          <h4 className="text-white font-semibold flex items-center gap-2 mb-4">
            <PlusCircle className="h-4 w-4 text-gold" />
            {editingLeadId ? 'Edit Lead' : 'Add Lead'}
          </h4>
          <div className="grid grid-cols-1 gap-3">
            {[
              ['company_name', 'Company Name *'],
              ['website', 'Website'],
              ['contact_name', 'Contact Name'],
              ['contact_email', 'Contact Email'],
              ['contact_phone', 'Contact Phone'],
              ['next_action', 'Next Action'],
            ].map(([key, label]) => (
              <div key={key}>
                <Label className="text-gray-300 text-xs mb-1 block">{label}</Label>
                <Input value={form[key]} onChange={(e) => setForm((prev) => ({ ...prev, [key]: e.target.value }))} className="bg-gray-700 border-gray-600 text-white" />
              </div>
            ))}

            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label className="text-gray-300 text-xs mb-1 block">Industry</Label>
                <select value={form.industry} onChange={(e) => setForm((prev) => ({ ...prev, industry: e.target.value }))} className="w-full bg-gray-700 border border-gray-600 rounded-md text-white text-sm px-3 py-2">
                  <option value="yoga_wellness">Yoga / Wellness</option>
                  <option value="matrimony">Matrimony</option>
                  <option value="astrology_portal">Astrology Portal</option>
                  <option value="news_media">News / Media</option>
                  <option value="app">App</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <Label className="text-gray-300 text-xs mb-1 block">Country</Label>
                <Input value={form.country} onChange={(e) => setForm((prev) => ({ ...prev, country: e.target.value }))} className="bg-gray-700 border-gray-600 text-white" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label className="text-gray-300 text-xs mb-1 block">Partnership Type</Label>
                <select value={form.partnership_type} onChange={(e) => setForm((prev) => ({ ...prev, partnership_type: e.target.value }))} className="w-full bg-gray-700 border border-gray-600 rounded-md text-white text-sm px-3 py-2">
                  <option value="api_panchang">API Panchang</option>
                  <option value="api_birth_chart">API Birth Chart</option>
                  <option value="api_horoscope">API Horoscope</option>
                  <option value="content_sponsor">Content Sponsor</option>
                  <option value="co_marketing">Co-marketing</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <Label className="text-gray-300 text-xs mb-1 block">Stage</Label>
                <select value={form.stage} onChange={(e) => setForm((prev) => ({ ...prev, stage: e.target.value }))} className="w-full bg-gray-700 border border-gray-600 rounded-md text-white text-sm px-3 py-2">
                  <option value="discovered">Discovered</option>
                  <option value="contacted">Contacted</option>
                  <option value="qualified">Qualified</option>
                  <option value="proposal_sent">Proposal Sent</option>
                  <option value="closed_won">Closed Won</option>
                  <option value="closed_lost">Closed Lost</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label className="text-gray-300 text-xs mb-1 block">Alignment Score (1-100)</Label>
                <Input type="number" min="1" max="100" value={form.alignment_score} onChange={(e) => setForm((prev) => ({ ...prev, alignment_score: e.target.value }))} className="bg-gray-700 border-gray-600 text-white" />
              </div>
              <div>
                <Label className="text-gray-300 text-xs mb-1 block">Deal Value ₹/month</Label>
                <Input type="number" min="0" value={form.deal_value_inr} onChange={(e) => setForm((prev) => ({ ...prev, deal_value_inr: e.target.value }))} className="bg-gray-700 border-gray-600 text-white" />
              </div>
            </div>

            <div>
              <Label className="text-gray-300 text-xs mb-1 block">Next Action Date</Label>
              <Input type="datetime-local" value={form.next_action_date} onChange={(e) => setForm((prev) => ({ ...prev, next_action_date: e.target.value }))} className="bg-gray-700 border-gray-600 text-white" />
            </div>

            <div>
              <Label className="text-gray-300 text-xs mb-1 block">Notes</Label>
              <textarea value={form.notes} onChange={(e) => setForm((prev) => ({ ...prev, notes: e.target.value }))} rows={5} className="w-full bg-gray-700 border border-gray-600 rounded-md text-white text-sm p-3 resize-y focus:outline-none focus:ring-1 focus:ring-gold" />
            </div>

            <div className="flex gap-3 pt-2">
              <Button onClick={saveLead} disabled={saving} className="bg-gold hover:bg-gold/90 text-gray-900">
                {saving ? <Loader2 className="h-3.5 w-3.5 mr-1.5 animate-spin" /> : <PlusCircle className="h-3.5 w-3.5 mr-1.5" />}
                {editingLeadId ? 'Save Changes' : 'Add Lead'}
              </Button>
              <Button variant="outline" className="border-gray-600 text-gray-300" onClick={resetForm}>
                Cancel
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
