import React, { useMemo, useState } from 'react';
import axios from 'axios';
import {
  Activity,
  AlertTriangle,
  Flag,
  RefreshCw,
  Search,
  ShieldAlert,
  ShieldCheck,
  Wallet,
  Zap,
} from 'lucide-react';
import { toast } from 'sonner';

import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Input } from '../ui/input';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

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

const truncateJson = (value) => {
  const raw = JSON.stringify(value || {});
  if (raw.length <= 80) {
    return raw;
  }
  return `${raw.slice(0, 77)}...`;
};

const eventTone = (eventType) => {
  if (eventType.includes('ERROR') || eventType.includes('CRASH')) {
    return 'bg-red-500/15 text-red-300 border-red-500/30';
  }
  if (eventType.includes('RAZORPAY')) {
    return 'bg-amber-500/15 text-amber-200 border-amber-500/30';
  }
  if (eventType === 'PAGE_VIEW') {
    return 'bg-sky-500/15 text-sky-200 border-sky-500/30';
  }
  return 'bg-slate-700/70 text-slate-200 border-slate-600';
};

const StatCard = ({ icon: Icon, label, value, tone = 'text-slate-200' }) => (
  <div className="rounded-xl border border-white/10 bg-slate-950/70 px-4 py-3">
    <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-[0.18em] text-slate-400">
      <Icon className={`h-3.5 w-3.5 ${tone}`} />
      <span>{label}</span>
    </div>
    <div className={`text-2xl font-semibold ${tone}`}>{value ?? '-'}</div>
  </div>
);

export const DiagnosticsTab = ({ getAuthHeaders }) => {
  const [searchValue, setSearchValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [toggling, setToggling] = useState(false);
  const [forceRunningId, setForceRunningId] = useState('');
  const [profile, setProfile] = useState(null);
  const [orders, setOrders] = useState([]);

  const events = useMemo(() => {
    const stream = profile?.event_stream || [];
    return [...stream].reverse();
  }, [profile]);

  const fetchDiagnostics = async (incomingValue) => {
    const lookup = (incomingValue ?? searchValue).trim();
    if (!lookup) {
      toast.error('Enter a user ID or email');
      return;
    }

    setLoading(true);
    try {
      const [diagnosticsResponse, ordersResponse] = await Promise.all([
        axios.get(
          `${API}/admin/diagnostics/${encodeURIComponent(lookup)}`,
          { headers: getAuthHeaders() }
        ),
        axios.get(
          `${API}/admin/orders/${encodeURIComponent(lookup)}`,
          { headers: getAuthHeaders() }
        ),
      ]);
      setProfile(diagnosticsResponse.data);
      setOrders(ordersResponse.data || []);
    } catch (error) {
      setProfile(null);
      setOrders([]);
      toast.error(error.response?.data?.detail || 'Failed to load diagnostics');
    } finally {
      setLoading(false);
    }
  };

  const handleFlagToggle = async () => {
    if (!profile?.user_id) {
      return;
    }

    setToggling(true);
    try {
      const nextFlag = !profile.is_claim_flagged;
      await axios.patch(
        `${API}/admin/diagnostics/${encodeURIComponent(profile.user_id)}/flag`,
        { flagged: nextFlag },
        { headers: getAuthHeaders() }
      );
      setProfile((current) => current ? {
        ...current,
        is_claim_flagged: nextFlag,
        last_updated: new Date().toISOString(),
      } : current);
      toast.success(nextFlag ? 'Dispute flag enabled' : 'Dispute flag removed');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update flag');
    } finally {
      setToggling(false);
    }
  };

  const handleForceRerun = async (orderId) => {
    if (!orderId) {
      return;
    }

    setForceRunningId(orderId);
    try {
      await axios.post(
        `${API}/admin/self-heal/force-trigger`,
        { order_id: orderId },
        { headers: getAuthHeaders() }
      );
      toast.success('Order re-queued for fulfillment');
      await fetchDiagnostics(profile?.user_id || searchValue);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to re-queue order');
    } finally {
      setForceRunningId('');
    }
  };

  const isStepStuck = (previousTimestamp, currentTimestamp) => {
    if (!previousTimestamp || currentTimestamp) {
      return false;
    }
    const previousDate = new Date(previousTimestamp);
    if (Number.isNaN(previousDate.getTime())) {
      return false;
    }
    return (Date.now() - previousDate.getTime()) > 15 * 60 * 1000;
  };

  const getOrderSteps = (order) => ([
    { key: 'cart', label: 'Cart Added', value: order.ts_cart_add },
    { key: 'form', label: 'Form Filled', value: order.ts_checkout_init },
    { key: 'gateway', label: 'Gateway Open', value: order.ts_gateway_open },
    { key: 'paid', label: 'Payment Verified', value: order.ts_pmt_success },
    { key: 'fulfilled', label: 'Claude Fulfilled', value: order.ts_fulfill_done },
  ]).map((step, index, steps) => ({
    ...step,
    stuck: index > 0 ? isStepStuck(steps[index - 1].value, step.value) : false,
  }));

  return (
    <Card className="border border-amber-500/30 bg-slate-900/95 shadow-2xl shadow-amber-950/20">
      <div className="space-y-6 p-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <div className="mb-2 flex items-center gap-2 text-amber-200">
              <Activity className="h-4 w-4" />
              <span className="text-xs font-semibold uppercase tracking-[0.24em]">Self-Heal Diagnostics</span>
            </div>
            <h3 className="text-xl font-semibold text-white">Per-user telemetry timeline</h3>
            <p className="mt-1 text-sm text-slate-400">
              Search by user ID or email to inspect page views, payment touchpoints, and backend errors.
            </p>
          </div>

          <form
            className="flex w-full max-w-2xl gap-2"
            onSubmit={(event) => {
              event.preventDefault();
              fetchDiagnostics();
            }}
          >
            <Input
              value={searchValue}
              onChange={(event) => setSearchValue(event.target.value)}
              placeholder="Enter user ID or email"
              className="border-slate-700 bg-slate-950 text-white placeholder:text-slate-500"
            />
            <Button
              type="submit"
              disabled={loading}
              className="bg-gold text-slate-900 hover:bg-gold/90"
            >
              {loading ? <RefreshCw className="mr-2 h-4 w-4 animate-spin" /> : <Search className="mr-2 h-4 w-4" />}
              Search
            </Button>
          </form>
        </div>

        {profile && (
          <>
            <div className="flex flex-col gap-4 rounded-xl border border-white/10 bg-slate-950/70 p-5 lg:flex-row lg:items-center lg:justify-between">
              <div className="space-y-2">
                <div className="flex flex-wrap items-center gap-3">
                  <h4 className="text-lg font-semibold text-white">{profile.user_id || profile._id}</h4>
                  <span className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-semibold ${
                    profile.is_claim_flagged
                      ? 'border-red-500/40 bg-red-500/10 text-red-200'
                      : 'border-emerald-500/40 bg-emerald-500/10 text-emerald-200'
                  }`}>
                    {profile.is_claim_flagged ? <ShieldAlert className="h-3.5 w-3.5" /> : <ShieldCheck className="h-3.5 w-3.5" />}
                    {profile.is_claim_flagged ? 'Dispute Flagged' : 'Verified'}
                  </span>
                </div>
                <div className="text-sm text-slate-300">{profile.user_email || 'No email on file'}</div>
                <div className="text-xs text-slate-500">Last active: {formatDateTime(profile.last_updated)}</div>
              </div>

              <Button
                onClick={handleFlagToggle}
                disabled={toggling}
                variant="outline"
                className="border-amber-500/40 bg-transparent text-amber-100 hover:bg-amber-500/10"
              >
                <Flag className="mr-2 h-4 w-4" />
                {toggling ? 'Updating...' : profile.is_claim_flagged ? 'Unflag dispute' : 'Flag dispute'}
              </Button>
            </div>

            <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <StatCard icon={Activity} label="Total Events" value={profile.quick_stats?.total_events || 0} tone="text-sky-200" />
              <StatCard icon={Search} label="Unique Pages" value={profile.quick_stats?.unique_pages || 0} tone="text-indigo-200" />
              <StatCard icon={AlertTriangle} label="Errors" value={profile.quick_stats?.error_count || 0} tone="text-red-200" />
              <StatCard icon={Wallet} label="Last Payment" value={profile.quick_stats?.last_payment_status || 'none'} tone="text-amber-200" />
            </div>

            <div className="overflow-hidden rounded-xl border border-white/10">
              <div className="flex items-center justify-between border-b border-white/10 bg-slate-950/80 px-4 py-3">
                <div>
                  <h5 className="text-sm font-semibold text-white">Event stream</h5>
                  <p className="text-xs text-slate-500">Newest events appear first. Metadata is truncated for quick scanning.</p>
                </div>
                <div className="text-xs text-slate-500">
                  Last payment order: {profile.last_payment?.razorpay_order_id || '-'}
                </div>
              </div>

              <div className="max-h-[540px] overflow-auto">
                <table className="min-w-full text-left text-sm">
                  <thead className="sticky top-0 bg-slate-900/95 text-xs uppercase tracking-[0.18em] text-slate-400">
                    <tr>
                      <th className="px-4 py-3 font-medium">Timestamp</th>
                      <th className="px-4 py-3 font-medium">Event</th>
                      <th className="px-4 py-3 font-medium">Page URL</th>
                      <th className="px-4 py-3 font-medium">Metadata</th>
                    </tr>
                  </thead>
                  <tbody>
                    {events.map((event, index) => (
                      <tr key={`${event.timestamp}-${event.event_type}-${index}`} className="border-t border-white/5 text-slate-200">
                        <td className="px-4 py-3 align-top text-xs text-slate-400">{formatDateTime(event.timestamp)}</td>
                        <td className="px-4 py-3 align-top">
                          <span className={`inline-flex rounded-full border px-2.5 py-1 text-[11px] font-semibold ${eventTone(event.event_type || '')}`}>
                            {event.event_type}
                          </span>
                        </td>
                        <td className="px-4 py-3 align-top font-mono text-xs text-slate-300">{event.page_url || '-'}</td>
                        <td className="px-4 py-3 align-top font-mono text-xs text-slate-400">{truncateJson(event.metadata)}</td>
                      </tr>
                    ))}
                    {events.length === 0 && (
                      <tr>
                        <td colSpan="4" className="px-4 py-10 text-center text-sm text-slate-500">
                          No diagnostic events have been captured for this user yet.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="rounded-xl border border-white/10 bg-slate-950/70">
              <div className="border-b border-white/10 px-4 py-3">
                <div className="flex items-center gap-2 text-white">
                  <Wallet className="h-4 w-4 text-amber-300" />
                  <h5 className="text-sm font-semibold">Lifecycle Ledger</h5>
                </div>
                <p className="mt-1 text-xs text-slate-500">
                  Order funnel from cart to fulfillment. Force Re-Run is available for paid orders still awaiting fulfillment.
                </p>
              </div>

              <div className="space-y-4 p-4">
                {orders.map((order) => {
                  const steps = getOrderSteps(order);
                  const showForce = order.current_state === 'PAID' && !order.ts_fulfill_done;
                  return (
                    <div key={order._id || order.razorpay_order_id} className="rounded-xl border border-white/10 bg-slate-900/80 p-4">
                      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                        <div className="space-y-2">
                          <div className="flex flex-wrap items-center gap-3">
                            <div className="text-sm font-semibold text-white">{order.report_type?.replace(/_/g, ' ') || 'Order'}</div>
                            <span className="rounded-full border border-slate-700 bg-slate-800 px-2.5 py-1 text-[11px] uppercase tracking-[0.18em] text-slate-300">
                              {order.current_state || 'unknown'}
                            </span>
                          </div>
                          <div className="text-xs text-slate-400">Internal Order: <span className="font-mono">{order._id || '-'}</span></div>
                          <div className="text-xs text-slate-400">Razorpay Order: <span className="font-mono">{order.razorpay_order_id || '-'}</span></div>
                          <div className="text-xs text-slate-400">Amount: ₹{((order.amount_paise || 0) / 100).toFixed(2)}</div>
                          {order.error_log && (
                            <div className="rounded-lg border border-red-500/20 bg-red-500/10 px-3 py-2 text-xs text-red-200">
                              {order.error_log}
                            </div>
                          )}
                        </div>

                        {showForce && (
                          <Button
                            onClick={() => handleForceRerun(order._id)}
                            disabled={forceRunningId === order._id}
                            variant="outline"
                            className="border-amber-500/40 bg-transparent text-amber-100 hover:bg-amber-500/10"
                          >
                            <Zap className="mr-2 h-4 w-4" />
                            {forceRunningId === order._id ? 'Re-queuing...' : 'Force Re-Run'}
                          </Button>
                        )}
                      </div>

                      <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-5">
                        {steps.map((step) => (
                          <div
                            key={step.key}
                            className={`rounded-xl border px-3 py-3 ${
                              step.value
                                ? 'border-emerald-500/30 bg-emerald-500/10'
                                : step.stuck
                                  ? 'border-red-500/30 bg-red-500/10'
                                  : 'border-slate-700 bg-slate-950/70'
                            }`}
                          >
                            <div className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-300">{step.label}</div>
                            <div className={`mt-2 text-sm ${
                              step.value
                                ? 'text-emerald-200'
                                : step.stuck
                                  ? 'text-red-200'
                                  : 'text-slate-500'
                            }`}>
                              {step.value ? formatDateTime(step.value) : 'Not Reached'}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}

                {orders.length === 0 && (
                  <div className="rounded-xl border border-dashed border-white/10 px-6 py-10 text-center text-sm text-slate-500">
                    No order ledger rows found for this user yet.
                  </div>
                )}
              </div>
            </div>
          </>
        )}

        {!profile && !loading && (
          <div className="rounded-xl border border-dashed border-white/10 bg-slate-950/50 px-6 py-12 text-center">
            <Activity className="mx-auto mb-3 h-8 w-8 text-slate-500" />
            <p className="text-sm text-slate-400">
              Search a user to load telemetry, payment state, and dispute controls.
            </p>
          </div>
        )}
      </div>
    </Card>
  );
};
