import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { toast } from 'sonner';
import { Button } from '../../components/ui/button';
import { Coins, Loader2, Save, Sparkles, Trophy } from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export function PunyaRewardsAdminPanel({ getAuthHeaders }) {
  const [overview, setOverview] = useState(null);
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadOverview();
  }, []);

  async function loadOverview() {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/admin/punya/overview`, {
        headers: getAuthHeaders(),
      });
      setOverview(response.data);
      setConfig(response.data.config);
    } catch (error) {
      toast.error(error?.response?.data?.detail || 'Failed to load Punya Rewards admin data');
    } finally {
      setLoading(false);
    }
  }

  function updateConfigField(field, value) {
    setConfig(current => ({ ...current, [field]: value }));
  }

  function updateSegment(index, field, value) {
    setConfig(current => ({
      ...current,
      wheel_segments: current.wheel_segments.map((segment, segmentIndex) => (
        segmentIndex === index ? { ...segment, [field]: value } : segment
      )),
    }));
  }

  function updateActionRule(actionCode, field, value) {
    setConfig(current => ({
      ...current,
      action_rules: {
        ...current.action_rules,
        [actionCode]: {
          ...current.action_rules[actionCode],
          [field]: value,
        },
      },
    }));
  }

  async function handleSave() {
    if (!config) return;
    setSaving(true);
    try {
      const payload = {
        spin_cost_points: Number(config.spin_cost_points || 50),
        daily_free_spin_enabled: Boolean(config.daily_free_spin_enabled),
        wheel_segments: (config.wheel_segments || []).map(segment => ({
          ...segment,
          prize_value: segment.prize_type === 'points' ? Number(segment.prize_value || 0) : segment.prize_value,
          weight: Number(segment.weight || 0),
          active: Boolean(segment.active),
        })),
        action_rules: Object.fromEntries(
          Object.entries(config.action_rules || {}).map(([actionCode, rule]) => [
            actionCode,
            {
              ...rule,
              points: Number(rule.points || 0),
              cap_count: Number(rule.cap_count || 0),
              enabled: Boolean(rule.enabled),
            },
          ]),
        ),
        login_streak_milestones: config.login_streak_milestones || [],
      };
      const response = await axios.put(`${API}/admin/punya/config`, payload, {
        headers: getAuthHeaders(),
      });
      setConfig(response.data);
      toast.success('Punya Rewards config saved');
      await loadOverview();
    } catch (error) {
      toast.error(error?.response?.data?.detail || 'Could not save Punya Rewards config');
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Loader2 className="h-6 w-6 animate-spin text-gold" />
      </div>
    );
  }

  if (!config || !overview) {
    return (
      <div className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
        Punya Rewards admin data is unavailable right now.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-gold/20 bg-gray-800/80 p-4">
          <div className="flex items-center gap-2 text-gold">
            <Coins className="h-4 w-4" />
            <p className="text-xs uppercase tracking-[0.24em]">Accounts</p>
          </div>
          <p className="mt-3 text-2xl font-semibold text-white">{overview.stats?.total_accounts || 0}</p>
        </div>
        <div className="rounded-xl border border-gold/20 bg-gray-800/80 p-4">
          <div className="flex items-center gap-2 text-gold">
            <Sparkles className="h-4 w-4" />
            <p className="text-xs uppercase tracking-[0.24em]">Transactions</p>
          </div>
          <p className="mt-3 text-2xl font-semibold text-white">{overview.stats?.total_transactions || 0}</p>
        </div>
        <div className="rounded-xl border border-gold/20 bg-gray-800/80 p-4">
          <div className="flex items-center gap-2 text-gold">
            <Trophy className="h-4 w-4" />
            <p className="text-xs uppercase tracking-[0.24em]">Spins</p>
          </div>
          <p className="mt-3 text-2xl font-semibold text-white">{overview.stats?.total_spins || 0}</p>
        </div>
      </div>

      <div className="flex items-center justify-between rounded-xl border border-gold/20 bg-gray-800/80 px-5 py-4">
        <div>
          <p className="text-sm font-semibold text-white">Temple Controls</p>
          <p className="text-xs text-gray-400">Wheel probability stays server-side. Temple Team edits the source config here.</p>
        </div>
        <Button onClick={handleSave} disabled={saving} className="bg-gold text-gray-900 hover:bg-gold/90">
          {saving ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
          Save Config
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.75fr,1.25fr]">
        <div className="space-y-6">
          <section className="rounded-xl border border-gray-700 bg-gray-800/80 p-5">
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-[0.24em] text-gold">Core Settings</h3>
            <div className="space-y-4">
              <div>
                <label className="mb-1 block text-xs text-gray-400">Spin cost (Punya Points)</label>
                <input
                  type="number"
                  min="0"
                  value={config.spin_cost_points || 0}
                  onChange={event => updateConfigField('spin_cost_points', event.target.value)}
                  className="w-full rounded-lg border border-gray-600 bg-gray-900 px-3 py-2 text-sm text-white"
                />
              </div>
              <label className="flex items-center gap-3 text-sm text-white">
                <input
                  type="checkbox"
                  checked={Boolean(config.daily_free_spin_enabled)}
                  onChange={event => updateConfigField('daily_free_spin_enabled', event.target.checked)}
                />
                Daily Blessing enabled
              </label>
            </div>
          </section>

          <section className="rounded-xl border border-gray-700 bg-gray-800/80 p-5">
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-[0.24em] text-gold">Weekly Leaders</h3>
            <div className="space-y-3">
              {(overview.leaderboard || []).map(entry => (
                <div key={entry.rank + entry.user_id} className="rounded-lg border border-gray-700 bg-gray-900/60 px-3 py-2">
                  <p className="text-sm font-medium text-white">#{entry.rank} {entry.user_name}</p>
                  <p className="text-xs text-gray-400">{entry.user_email}</p>
                  <p className="mt-1 text-xs text-gold">{entry.weekly_points} pts this week</p>
                </div>
              ))}
            </div>
          </section>
        </div>

        <div className="space-y-6">
          <section className="rounded-xl border border-gray-700 bg-gray-800/80 p-5">
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-[0.24em] text-gold">Wheel Segments</h3>
            <div className="space-y-4">
              {(config.wheel_segments || []).map((segment, index) => (
                <div key={segment.segment_id || index} className="rounded-lg border border-gray-700 bg-gray-900/60 p-4">
                  <div className="grid gap-3 md:grid-cols-2">
                    <div>
                      <label className="mb-1 block text-xs text-gray-400">Label</label>
                      <input
                        value={segment.label || ''}
                        onChange={event => updateSegment(index, 'label', event.target.value)}
                        className="w-full rounded-lg border border-gray-600 bg-gray-900 px-3 py-2 text-sm text-white"
                      />
                    </div>
                    <div>
                      <label className="mb-1 block text-xs text-gray-400">Prize type</label>
                      <select
                        value={segment.prize_type || 'points'}
                        onChange={event => updateSegment(index, 'prize_type', event.target.value)}
                        className="w-full rounded-lg border border-gray-600 bg-gray-900 px-3 py-2 text-sm text-white"
                      >
                        <option value="coupon">coupon</option>
                        <option value="unlock">unlock</option>
                        <option value="points">points</option>
                        <option value="soft_loss">soft_loss</option>
                      </select>
                    </div>
                    <div>
                      <label className="mb-1 block text-xs text-gray-400">Prize value</label>
                      <input
                        value={segment.prize_value ?? ''}
                        onChange={event => updateSegment(index, 'prize_value', event.target.value)}
                        className="w-full rounded-lg border border-gray-600 bg-gray-900 px-3 py-2 text-sm text-white"
                      />
                    </div>
                    <div>
                      <label className="mb-1 block text-xs text-gray-400">Weight</label>
                      <input
                        type="number"
                        min="0"
                        value={segment.weight || 0}
                        onChange={event => updateSegment(index, 'weight', event.target.value)}
                        className="w-full rounded-lg border border-gray-600 bg-gray-900 px-3 py-2 text-sm text-white"
                      />
                    </div>
                  </div>
                  <label className="mt-3 flex items-center gap-3 text-sm text-white">
                    <input
                      type="checkbox"
                      checked={Boolean(segment.active)}
                      onChange={event => updateSegment(index, 'active', event.target.checked)}
                    />
                    Active
                  </label>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-xl border border-gray-700 bg-gray-800/80 p-5">
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-[0.24em] text-gold">Action Rules</h3>
            <div className="space-y-4">
              {Object.entries(config.action_rules || {}).map(([actionCode, rule]) => (
                <div key={actionCode} className="rounded-lg border border-gray-700 bg-gray-900/60 p-4">
                  <div className="mb-3 flex items-center justify-between gap-4">
                    <div>
                      <p className="text-sm font-medium text-white">{rule.label}</p>
                      <p className="text-xs text-gray-400">{actionCode}</p>
                    </div>
                    <label className="flex items-center gap-2 text-xs text-white">
                      <input
                        type="checkbox"
                        checked={Boolean(rule.enabled)}
                        onChange={event => updateActionRule(actionCode, 'enabled', event.target.checked)}
                      />
                      Enabled
                    </label>
                  </div>
                  <div className="grid gap-3 md:grid-cols-3">
                    <div>
                      <label className="mb-1 block text-xs text-gray-400">Points</label>
                      <input
                        type="number"
                        min="0"
                        value={rule.points || 0}
                        onChange={event => updateActionRule(actionCode, 'points', event.target.value)}
                        className="w-full rounded-lg border border-gray-600 bg-gray-900 px-3 py-2 text-sm text-white"
                      />
                    </div>
                    <div>
                      <label className="mb-1 block text-xs text-gray-400">Cap window</label>
                      <select
                        value={rule.cap_window || 'reference'}
                        onChange={event => updateActionRule(actionCode, 'cap_window', event.target.value)}
                        className="w-full rounded-lg border border-gray-600 bg-gray-900 px-3 py-2 text-sm text-white"
                      >
                        <option value="day">day</option>
                        <option value="week">week</option>
                        <option value="month">month</option>
                        <option value="reference">reference</option>
                      </select>
                    </div>
                    <div>
                      <label className="mb-1 block text-xs text-gray-400">Cap count</label>
                      <input
                        type="number"
                        min="1"
                        value={rule.cap_count || 1}
                        onChange={event => updateActionRule(actionCode, 'cap_count', event.target.value)}
                        className="w-full rounded-lg border border-gray-600 bg-gray-900 px-3 py-2 text-sm text-white"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <section className="rounded-xl border border-gray-700 bg-gray-800/80 p-5">
          <h3 className="mb-4 text-sm font-semibold uppercase tracking-[0.24em] text-gold">Recent Transactions</h3>
          <div className="space-y-3">
            {(overview.recent_transactions || []).slice(0, 10).map(entry => (
              <div key={entry.transaction_id} className="rounded-lg border border-gray-700 bg-gray-900/60 px-4 py-3">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm font-medium text-white">{entry.reason_code}</p>
                    <p className="text-xs text-gray-400">{entry.user_email}</p>
                  </div>
                  <p className={`text-sm font-semibold ${entry.direction === 'credit' ? 'text-emerald-400' : 'text-red-300'}`}>
                    {entry.direction === 'credit' ? '+' : '-'}{entry.amount}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-xl border border-gray-700 bg-gray-800/80 p-5">
          <h3 className="mb-4 text-sm font-semibold uppercase tracking-[0.24em] text-gold">Recent Spins</h3>
          <div className="space-y-3">
            {(overview.recent_spins || []).slice(0, 10).map(entry => (
              <div key={entry.spin_id} className="rounded-lg border border-gray-700 bg-gray-900/60 px-4 py-3">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm font-medium text-white">{entry.prize_segment}</p>
                    <p className="text-xs text-gray-400">{entry.user_email}</p>
                  </div>
                  <p className="text-xs text-gold">{entry.is_free_spin ? 'Daily Blessing' : `${entry.spin_cost_points} pts`}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
