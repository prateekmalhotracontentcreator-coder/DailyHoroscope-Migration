import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdminAuth } from '../../context/AdminAuthContext';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import {
  Users, CreditCard, FileText, TrendingUp,
  LogOut, Crown, IndianRupee, BarChart3,
  ArrowUpRight, Settings, Lock, Eye, EyeOff,
  BookOpen, Ban, ShieldOff, ShieldCheck, Trash2,
  Search, RefreshCw, MessageSquare, Mail, Activity,
  AlertTriangle, CheckCircle, Zap, Star,
  Heart, Copy, Send, X, Bell, Phone, Tag,
  Clock, CalendarClock, PlusCircle, History, Wifi, WifiOff,
  Globe, Image
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';
import { AdminBlogManager } from './AdminBlogManager';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const copyToClipboard = (text, label) =>
  navigator.clipboard.writeText(text).then(() => toast.success(`${label} copied`));

const StatusBadge = ({ status }) => {
  const map = {
    completed: 'bg-green-500/20 text-green-400', generated: 'bg-green-500/20 text-green-400',
    created: 'bg-yellow-500/20 text-yellow-400', pending: 'bg-yellow-500/20 text-yellow-400',
    failed: 'bg-red-500/20 text-red-400', active: 'bg-green-500/20 text-green-400',
    suspended: 'bg-orange-500/20 text-orange-400', restricted: 'bg-yellow-500/20 text-yellow-400',
  };
  return <span className={`px-2 py-0.5 rounded text-xs font-medium capitalize ${map[status] || 'bg-gray-500/20 text-gray-400'}`}>{status}</span>;
};

const MonoID = ({ id, label }) => (
  <span className="inline-flex items-center gap-1 font-mono text-xs text-gray-400 group">
    {id ? id.slice(0, 10) + '...' : '\u2014'}
    {id && (
      <button onClick={() => copyToClipboard(id, label || 'ID')}
        className="opacity-0 group-hover:opacity-100 transition-opacity p-0.5 hover:text-gold" title={id}>
        <Copy className="h-3 w-3" />
      </button>
    )}
  </span>
);

// ─── In-app Reply Modal ───────────────────────────────────────────────────────
const ReplyModal = ({ msg, onClose, getAuthHeaders }) => {
  const [subject, setSubject] = useState(`Re: ${msg.subject || 'Your message'}`);
  const [body, setBody]       = useState('');
  const [sending, setSending] = useState(false);

  const handleSend = async () => {
    if (!body.trim()) { toast.error('Please write a reply'); return; }
    setSending(true);
    try {
      await axios.post(`${API}/admin/contact/reply`,
        { to_email: msg.email, to_name: msg.name, subject, message: body },
        { headers: getAuthHeaders() }
      );
      toast.success(`Reply sent to ${msg.email}`);
      onClose();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to send reply');
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
      <div className="w-full max-w-lg bg-gray-800 border border-gray-600 rounded-xl p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-white font-semibold flex items-center gap-2">
            <Mail className="h-4 w-4 text-gold" />Reply to {msg.name}
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-white"><X className="h-4 w-4" /></button>
        </div>
        <div className="text-xs text-gray-400 mb-4 p-3 bg-gray-700/50 rounded-lg">
          <p className="font-medium text-gray-300 mb-1">Original message:</p>
          <p className="line-clamp-3">{msg.message}</p>
        </div>
        <div className="space-y-3">
          <div>
            <Label className="text-gray-300 text-xs">To</Label>
            <Input value={`${msg.name} <${msg.email}>`} readOnly className="bg-gray-700/50 border-gray-600 text-gray-400 text-sm" />
          </div>
          <div>
            <Label className="text-gray-300 text-xs">Subject</Label>
            <Input value={subject} onChange={e => setSubject(e.target.value)} className="bg-gray-700 border-gray-600 text-white text-sm" />
          </div>
          <div>
            <Label className="text-gray-300 text-xs">Message</Label>
            <textarea
              value={body}
              onChange={e => setBody(e.target.value)}
              className="w-full h-32 px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white text-sm resize-none focus:outline-none focus:ring-1 focus:ring-gold"
              placeholder="Type your reply here..."
            />
          </div>
        </div>
        <div className="flex gap-3 mt-4">
          <Button onClick={onClose} variant="outline" className="flex-1 border-gray-600 text-gray-300">Cancel</Button>
          <Button onClick={handleSend} disabled={sending} className="flex-1 bg-gold hover:bg-gold/90 text-gray-900">
            <Send className="h-3.5 w-3.5 mr-1.5" />{sending ? 'Sending...' : 'Send Reply'}
          </Button>
        </div>
      </div>
    </div>
  );
};

export const AdminDashboard = () => {
  const navigate = useNavigate();
  const { logout, getAuthHeaders, isAuthenticated, loading: authLoading } = useAdminAuth();

  const [stats,    setStats]    = useState(null);
  const [loading,  setLoading]  = useState(true);
  const [activeTab,setActiveTab]= useState('overview');

  const [users,    setUsers]    = useState([]);
  const [payments, setPayments] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [reports,  setReports]  = useState({ birth_charts: [], kundali_milans: [] });
  const [healthData, setHealthData] = useState(null);
  const [healthLoading, setHealthLoading] = useState(false);
  const [prefetchLoading, setPrefetchLoading] = useState(false);
  const [replyMsg, setReplyMsg] = useState(null);

  // ── Notifications state ──────────────────────────────────────────────────
  const [subscribers,     setSubscribers]     = useState([]);
  const [subLoading,      setSubLoading]       = useState(false);
  const [notifLogs,       setNotifLogs]        = useState([]);
  const [scheduled,       setScheduled]        = useState([]);
  const [notifTab,        setNotifTab]         = useState('subscribers'); // subscribers | compose | scheduled | history | social
  const [socialForm,      setSocialForm]       = useState({ message: '', image_url: '', channels: ['facebook'] });
  const [socialPosting,   setSocialPosting]    = useState(false);
  const [socialResults,   setSocialResults]    = useState(null);
  const [socialLogs,      setSocialLogs]       = useState([]);
  const [subForm,         setSubForm]          = useState({ name: '', email: '', phone: '', tags: '' });
  const [editingSub,      setEditingSub]       = useState(null);
  const [subSearch,       setSubSearch]        = useState('');
  const [notifForm,       setNotifForm]        = useState({ subject: '', body: '', channels: ['email'], audience: 'all', tags: '', scheduled_at: '' });
  const [notifSending,    setNotifSending]     = useState(false);
  const [notifResult,     setNotifResult]      = useState(null);

  const [userSearch,    setUserSearch]    = useState('');
  const [reportSearch,  setReportSearch]  = useState('');
  const [reportFilter,  setReportFilter]  = useState('all');
  const [paymentFilter, setPaymentFilter] = useState('all');
  const [actionLoading, setActionLoading] = useState(null);

  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [currentPassword,   setCurrentPassword]   = useState('');
  const [newPassword,       setNewPassword]       = useState('');
  const [confirmPassword,   setConfirmPassword]   = useState('');
  const [showCurrentPwd,    setShowCurrentPwd]    = useState(false);
  const [showNewPwd,        setShowNewPwd]        = useState(false);
  const [changingPassword,  setChangingPassword]  = useState(false);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) navigate('/admin/login');
  }, [isAuthenticated, authLoading, navigate]);

  useEffect(() => {
    if (isAuthenticated) fetchDashboardData();
  }, [isAuthenticated]);

  useEffect(() => {
    if (activeTab === 'contacts')      fetchContacts();
    if (activeTab === 'reports')       fetchReports();
    if (activeTab === 'health')        fetchHealth();
    if (activeTab === 'notifications') { fetchSubscribers(); fetchNotifLogs(); fetchScheduled(); fetchSocialLogs(); }
  }, [activeTab]);

  const fetchSubscribers = async () => {
    setSubLoading(true);
    try {
      const res = await axios.get(`${API}/admin/subscribers?active_only=false`, { headers: getAuthHeaders() });
      setSubscribers(res.data.subscribers || []);
    } catch { toast.error('Failed to load subscribers'); }
    finally { setSubLoading(false); }
  };

  const fetchNotifLogs = async () => {
    try {
      const res = await axios.get(`${API}/admin/notify/logs`, { headers: getAuthHeaders() });
      setNotifLogs(res.data.logs || []);
    } catch {}
  };

  const fetchSocialLogs = async () => {
    try {
      const res = await axios.get(`${API}/admin/social/logs`, { headers: getAuthHeaders() });
      setSocialLogs(res.data.logs || []);
    } catch {}
  };

  const fetchScheduled = async () => {
    try {
      const res = await axios.get(`${API}/admin/notify/scheduled`, { headers: getAuthHeaders() });
      setScheduled(res.data.scheduled || []);
    } catch {}
  };

  const handleAddSubscriber = async () => {
    if (!subForm.name.trim()) { toast.error('Name is required'); return; }
    try {
      await axios.post(`${API}/admin/subscribers`, {
        name: subForm.name, email: subForm.email || null,
        phone: subForm.phone || null,
        tags: subForm.tags ? subForm.tags.split(',').map(t => t.trim()).filter(Boolean) : [],
      }, { headers: getAuthHeaders() });
      toast.success('Subscriber added');
      setSubForm({ name: '', email: '', phone: '', tags: '' });
      fetchSubscribers();
    } catch (err) { toast.error(err.response?.data?.detail || 'Failed to add subscriber'); }
  };

  const handleUpdateSubscriber = async (id, data) => {
    try {
      await axios.put(`${API}/admin/subscribers/${id}`, data, { headers: getAuthHeaders() });
      toast.success('Updated'); setEditingSub(null); fetchSubscribers();
    } catch (err) { toast.error(err.response?.data?.detail || 'Failed to update'); }
  };

  const handleDeleteSubscriber = async (id, name) => {
    if (!window.confirm(`Remove ${name} from subscribers?`)) return;
    try {
      await axios.delete(`${API}/admin/subscribers/${id}`, { headers: getAuthHeaders() });
      toast.success('Subscriber removed'); fetchSubscribers();
    } catch { toast.error('Failed to remove subscriber'); }
  };

  const handleSendNotification = async (scheduleMode) => {
    if (!notifForm.subject.trim()) { toast.error('Subject is required'); return; }
    if (!notifForm.body.trim())    { toast.error('Message body is required'); return; }
    if (!notifForm.channels.length){ toast.error('Select at least one channel'); return; }
    if (scheduleMode && !notifForm.scheduled_at) { toast.error('Pick a schedule date/time'); return; }
    setNotifSending(true); setNotifResult(null);
    try {
      const payload = {
        subject: notifForm.subject, body: notifForm.body,
        channels: notifForm.channels, audience: notifForm.audience,
        tags: notifForm.tags ? notifForm.tags.split(',').map(t => t.trim()).filter(Boolean) : [],
        scheduled_at: scheduleMode ? new Date(notifForm.scheduled_at).toISOString() : null,
      };
      const url = scheduleMode ? `${API}/admin/notify/schedule` : `${API}/admin/notify/send`;
      const res = await axios.post(url, payload, { headers: getAuthHeaders() });
      if (scheduleMode) {
        toast.success('Notification scheduled'); fetchScheduled();
      } else {
        toast.success(`Sent: ${res.data.sent} ✓  Failed: ${res.data.failed}`);
        setNotifResult(res.data); fetchNotifLogs();
      }
    } catch (err) { toast.error(err.response?.data?.detail || 'Send failed'); }
    finally { setNotifSending(false); }
  };

  const handleCancelScheduled = async (id) => {
    try {
      await axios.delete(`${API}/admin/notify/scheduled/${id}`, { headers: getAuthHeaders() });
      toast.success('Cancelled'); fetchScheduled();
    } catch { toast.error('Failed to cancel'); }
  };

  const handleSocialPost = async () => {
    if (!socialForm.message.trim()) { toast.error('Message is required'); return; }
    if (!socialForm.channels.length) { toast.error('Select at least one channel'); return; }
    setSocialPosting(true); setSocialResults(null);
    try {
      const res = await axios.post(`${API}/admin/social/post`, {
        message: socialForm.message,
        image_url: socialForm.image_url || null,
        channels: socialForm.channels,
      }, { headers: getAuthHeaders() });
      setSocialResults(res.data.results);
      const allOk = res.data.results.every(r => r.success);
      if (allOk) { toast.success('Posted successfully!'); setSocialForm(p => ({ ...p, message: '', image_url: '' })); }
      else toast.error('Some posts failed — check results below');
      fetchSocialLogs();
    } catch (err) { toast.error(err.response?.data?.detail || 'Post failed'); }
    finally { setSocialPosting(false); }
  };

  const fetchDashboardData = async () => {
    try {
      const h = getAuthHeaders();
      const [statsRes, usersRes, paymentsRes] = await Promise.all([
        axios.get(`${API}/admin/dashboard`, { headers: h }),
        axios.get(`${API}/admin/users?limit=100`, { headers: h }),
        axios.get(`${API}/admin/payments?limit=100`, { headers: h }),
      ]);
      setStats(statsRes.data);
      setUsers(usersRes.data.users);
      setPayments(paymentsRes.data.payments);
    } catch (err) {
      if (err.response?.status === 401) navigate('/admin/login');
      toast.error('Failed to load dashboard data');
    } finally { setLoading(false); }
  };

  const fetchContacts = async () => {
    try {
      const res = await axios.get(`${API}/admin/contacts`, { headers: getAuthHeaders() });
      setContacts(res.data.messages || []);
    } catch { toast.error('Failed to load messages'); }
  };

  const fetchReports = async () => {
    try {
      const res = await axios.get(`${API}/admin/reports?limit=100`, { headers: getAuthHeaders() });
      setReports(res.data);
    } catch (err) {
      toast.error('Failed to load reports');
    }
  };

  const fetchHealth = async () => {
    setHealthLoading(true);
    try {
      const res = await axios.get(`${API}/horoscope/prefetch-status`);
      setHealthData({ prefetch: res.data });
    } catch { toast.error('Failed to load health data'); }
    finally { setHealthLoading(false); }
  };

  const triggerPrefetch = async () => {
    setPrefetchLoading(true);
    try {
      const signs = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces'];
      const types = ['daily','weekly','monthly'];
      let generated = 0;
      for (const type of types) {
        for (const sign of signs) {
          try { await axios.get(`${API}/horoscope/${sign}/${type}`); generated++; } catch {}
        }
      }
      toast.success(`Prefetch complete: ${generated}/36 horoscopes checked`);
      fetchHealth();
    } catch { toast.error('Prefetch failed'); }
    finally { setPrefetchLoading(false); }
  };

  const handleUserAction = async (userId, action) => {
    setActionLoading(userId + action);
    try {
      await axios.post(`${API}/admin/user/${userId}/action`, { action }, { headers: getAuthHeaders() });
      toast.success(`User ${action}ed`);
      fetchDashboardData();
    } catch (err) {
      toast.error(err.response?.data?.detail || `Failed to ${action} user`);
    } finally { setActionLoading(null); }
  };

  const handleDeleteUser = async (userId, userName) => {
    if (!window.confirm(`Permanently delete ${userName}?`)) return;
    setActionLoading(userId + 'delete');
    try {
      await axios.delete(`${API}/admin/user/${userId}`, { headers: getAuthHeaders() });
      toast.success('User deleted');
      fetchDashboardData();
    } catch { toast.error('Failed to delete user'); }
    finally { setActionLoading(null); }
  };

  const handleLogout = async () => { await logout(); navigate('/admin/login'); };

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) { toast.error('Passwords do not match'); return; }
    if (newPassword.length < 8) { toast.error('Min 8 characters'); return; }
    setChangingPassword(true);
    try {
      await axios.post(
        `${API}/admin/change-password`,
        { current_password: currentPassword, new_password: newPassword },
        { headers: getAuthHeaders() }
      );
      toast.success('Password changed');
      setShowPasswordModal(false);
      setCurrentPassword(''); setNewPassword(''); setConfirmPassword('');
    } catch (err) {
      // ← FIX: properly surface the backend error
      toast.error(err.response?.data?.detail || 'Failed to change password');
    } finally { setChangingPassword(false); }
  };

  const getUserStatus = (user) => {
    if (user.is_suspended) return { label: 'Suspended',  color: 'bg-orange-500/20 text-orange-400' };
    if (user.is_restricted) return { label: 'Restricted', color: 'bg-yellow-500/20 text-yellow-400' };
    if (user.locked_until && new Date(user.locked_until) > new Date()) return { label: 'Locked', color: 'bg-purple-500/20 text-purple-400' };
    return { label: 'Active', color: 'bg-green-500/20 text-green-400' };
  };

  const filteredUsers = users.filter(u =>
    u.name?.toLowerCase().includes(userSearch.toLowerCase()) ||
    u.email?.toLowerCase().includes(userSearch.toLowerCase()) ||
    u.user_id?.toLowerCase().includes(userSearch.toLowerCase())
  );

  const allReports = [
    ...(reports.birth_charts || []).map(r => ({ ...r, type: 'Birth Chart', icon: Star, color: 'text-gold' })),
    ...(reports.kundali_milans || []).map(r => ({ ...r, type: 'Kundali Milan', icon: Heart, color: 'text-pink-400' })),
  ].sort((a, b) => new Date(b.generated_at || 0) - new Date(a.generated_at || 0));

  const filteredReports = allReports.filter(r => {
    const matchType = reportFilter === 'all' || r.type.toLowerCase().includes(reportFilter);
    const matchSearch = !reportSearch ||
      r.id?.toLowerCase().includes(reportSearch.toLowerCase()) ||
      r.profile_id?.toLowerCase().includes(reportSearch.toLowerCase()) ||
      r.person1_id?.toLowerCase().includes(reportSearch.toLowerCase());
    return matchType && matchSearch;
  });

  const filteredPayments = payments.filter(p =>
    paymentFilter === 'all' || p.status === paymentFilter
  );

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-gold text-xl animate-pulse">Loading admin panel...</div>
      </div>
    );
  }

  const statCards = [
    { label: 'Total Users',          value: stats?.total_users || 0,       icon: Users,       color: 'text-blue-400',   bgColor: 'bg-blue-400/10',   change: stats?.users_today,    changeLabel: 'new today' },
    { label: 'Total Revenue',        value: `\u20b9${(stats?.total_revenue||0).toLocaleString()}`, icon: IndianRupee, color: 'text-green-400', bgColor: 'bg-green-400/10', change: stats?.payments_today, changeLabel: 'payments today' },
    { label: 'Birth Charts',         value: stats?.total_birth_charts || 0,  icon: Star,        color: 'text-purple-400', bgColor: 'bg-purple-400/10' },
    { label: 'Kundali Milans',       value: stats?.total_kundali_milans || 0,icon: Heart,       color: 'text-pink-400',   bgColor: 'bg-pink-400/10' },
    { label: 'Active Subscriptions', value: stats?.active_subscriptions || 0,icon: TrendingUp,  color: 'text-gold',       bgColor: 'bg-gold/10' },
    { label: 'Total Payments',       value: stats?.total_payments || 0,      icon: CreditCard,  color: 'text-cyan-400',   bgColor: 'bg-cyan-400/10' },
  ];

  const tabs = [
    { id: 'overview',       label: 'Overview',       icon: BarChart3 },
    { id: 'health',         label: 'System',         icon: Activity },
    { id: 'users',          label: 'Users',          icon: Users },
    { id: 'reports',        label: 'Reports',        icon: FileText },
    { id: 'payments',       label: 'Payments',       icon: CreditCard },
    { id: 'contacts',       label: 'Messages',       icon: MessageSquare },
    { id: 'blog',           label: 'Blog',           icon: BookOpen },
    { id: 'notifications',  label: 'Notifications',  icon: Bell },
  ];

  return (
    <div className="min-h-screen bg-gray-900">

      {/* Reply Modal */}
      {replyMsg && <ReplyModal msg={replyMsg} onClose={() => setReplyMsg(null)} getAuthHeaders={getAuthHeaders} />}

      {/* Password Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
          <Card className="w-full max-w-md p-6 bg-gray-800 border-gray-700 mx-4">
            <div className="flex items-center gap-2 mb-6">
              <Lock className="h-5 w-5 text-gold" />
              <h2 className="text-xl font-bold text-white">Change Admin Password</h2>
            </div>
            <div className="space-y-4">
              {[['Current Password', currentPassword, setCurrentPassword, showCurrentPwd, setShowCurrentPwd],
                ['New Password (min 8)', newPassword, setNewPassword, showNewPwd, setShowNewPwd]].map(([label, val, setter, show, setShow]) => (
                <div key={label}>
                  <Label className="text-gray-300">{label}</Label>
                  <div className="relative">
                    <Input type={show ? 'text' : 'password'} value={val} onChange={e => setter(e.target.value)}
                      className="bg-gray-700 border-gray-600 text-white pr-10" />
                    <button type="button" onClick={() => setShow(!show)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                      {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                </div>
              ))}
              <div>
                <Label className="text-gray-300">Confirm New Password</Label>
                <Input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} className="bg-gray-700 border-gray-600 text-white" />
              </div>
            </div>
            <div className="flex gap-3 mt-6">
              <Button onClick={() => { setShowPasswordModal(false); setCurrentPassword(''); setNewPassword(''); setConfirmPassword(''); }}
                variant="outline" className="flex-1 border-gray-600 text-gray-300">Cancel</Button>
              <Button onClick={handleChangePassword} disabled={changingPassword} className="flex-1 bg-gold hover:bg-gold/90 text-gray-900">
                {changingPassword ? 'Changing...' : 'Change Password'}
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <BarChart3 className="h-7 w-7 text-gold" />
            <div>
              <h1 className="text-lg font-bold text-white leading-none">EverydayHoroscope Admin</h1>
              <p className="text-xs text-gray-400 mt-0.5">Monitoring \u00b7 Healing \u00b7 Operations</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button onClick={() => setShowPasswordModal(true)} variant="outline" size="sm" className="border-gray-600 text-gray-300 hover:bg-gray-700">
              <Settings className="h-4 w-4 mr-1.5" />Password
            </Button>
            <Button onClick={handleLogout} variant="outline" size="sm" className="border-gray-600 text-gray-300 hover:bg-gray-700">
              <LogOut className="h-4 w-4 mr-1.5" />Logout
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">

        {/* Stat cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          {statCards.map((stat, i) => {
            const Icon = stat.icon;
            return (
              <Card key={i} className="p-4 bg-gray-800 border-gray-700">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-gray-400 text-xs">{stat.label}</p>
                    <p className="text-xl font-bold text-white mt-1">{stat.value}</p>
                    {stat.change !== undefined && (
                      <p className="text-green-400 text-xs mt-1 flex items-center gap-0.5">
                        <ArrowUpRight className="h-3 w-3" />{stat.change} {stat.changeLabel}
                      </p>
                    )}
                  </div>
                  <div className={`${stat.bgColor} rounded-lg p-2`}>
                    <Icon className={`h-4 w-4 ${stat.color}`} />
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Tabs */}
        <div className="flex flex-wrap gap-2 mb-6">
          {tabs.map(({ id, label, icon: Icon }) => (
            <Button key={id} onClick={() => setActiveTab(id)} size="sm"
              className={activeTab === id ? 'bg-gold text-gray-900' : 'border-gray-600 text-gray-300 hover:bg-gray-700'}
              variant={activeTab === id ? 'default' : 'outline'}>
              <Icon className="h-3.5 w-3.5 mr-1.5" />{label}
            </Button>
          ))}
        </div>

        {/* OVERVIEW */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="p-6 bg-gray-800 border-gray-700">
              <h3 className="text-base font-semibold text-white mb-4 flex items-center gap-2"><Users className="h-4 w-4 text-blue-400" />Recent Users</h3>
              <div className="space-y-2">
                {users.slice(0, 5).map((u, i) => {
                  const s = getUserStatus(u);
                  return (
                    <div key={i} className="flex items-center justify-between py-2 border-b border-gray-700 last:border-0">
                      <div>
                        <p className="text-white text-sm font-medium">{u.name}</p>
                        <p className="text-gray-400 text-xs">{u.email}</p>
                        <MonoID id={u.user_id} label="User ID" />
                      </div>
                      <StatusBadge status={s.label.toLowerCase()} />
                    </div>
                  );
                })}
              </div>
            </Card>
            <Card className="p-6 bg-gray-800 border-gray-700">
              <h3 className="text-base font-semibold text-white mb-4 flex items-center gap-2"><CreditCard className="h-4 w-4 text-green-400" />Recent Payments</h3>
              <div className="space-y-2">
                {payments.slice(0, 5).map((p, i) => (
                  <div key={i} className="flex items-center justify-between py-2 border-b border-gray-700 last:border-0">
                    <div>
                      <p className="text-white text-sm font-medium">\u20b9{p.amount} \u2014 {p.report_type?.replace(/_/g,' ')}</p>
                      <p className="text-gray-400 text-xs">{p.user_email}</p>
                      <MonoID id={p.razorpay_order_id} label="Order ID" />
                    </div>
                    <StatusBadge status={p.status} />
                  </div>
                ))}
                {payments.length === 0 && <p className="text-gray-500 text-sm">No payments yet</p>}
              </div>
            </Card>
          </div>
        )}

        {/* SYSTEM HEALTH */}
        {activeTab === 'health' && (
          <div className="space-y-6">
            <Card className="p-6 bg-gray-800 border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base font-semibold text-white flex items-center gap-2"><Zap className="h-4 w-4 text-gold" />Horoscope Cache</h3>
                <div className="flex gap-2">
                  <Button onClick={fetchHealth} variant="outline" size="sm" className="border-gray-600 text-gray-300" disabled={healthLoading}>
                    <RefreshCw className={`h-3.5 w-3.5 mr-1.5 ${healthLoading ? 'animate-spin' : ''}`} />Refresh
                  </Button>
                  <Button onClick={triggerPrefetch} size="sm" className="bg-gold hover:bg-gold/90 text-gray-900" disabled={prefetchLoading}>
                    <Zap className="h-3.5 w-3.5 mr-1.5" />{prefetchLoading ? 'Running...' : 'Trigger Prefetch'}
                  </Button>
                </div>
              </div>
              {healthData?.prefetch ? (
                <div className="grid grid-cols-3 gap-4">
                  {['daily','weekly','monthly'].map(type => {
                    const d = healthData.prefetch[type];
                    const pct = Math.round((d.cached / d.total) * 100);
                    const full = d.cached === d.total;
                    return (
                      <div key={type} className={`p-4 rounded-lg border ${full ? 'border-green-500/30 bg-green-500/5' : 'border-yellow-500/30 bg-yellow-500/5'}`}>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-white capitalize font-medium">{type}</span>
                          {full ? <CheckCircle className="h-4 w-4 text-green-400" /> : <AlertTriangle className="h-4 w-4 text-yellow-400" />}
                        </div>
                        <p className="text-2xl font-bold text-white">{d.cached}/{d.total}</p>
                        <div className="mt-2 h-1.5 bg-gray-700 rounded-full overflow-hidden">
                          <div className={`h-full rounded-full transition-all ${full ? 'bg-green-400' : 'bg-yellow-400'}`} style={{ width: `${pct}%` }} />
                        </div>
                        <p className="text-xs text-gray-400 mt-1">For {d.date}</p>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Button onClick={fetchHealth} className="bg-gold hover:bg-gold/90 text-gray-900">
                    <Activity className="h-4 w-4 mr-2" />Load Health Data
                  </Button>
                </div>
              )}
            </Card>

            {/* Stuck Payments */}
            <Card className="p-6 bg-gray-800 border-gray-700">
              <h3 className="text-base font-semibold text-white mb-1 flex items-center gap-2"><AlertTriangle className="h-4 w-4 text-yellow-400" />Stuck Payments</h3>
              <p className="text-xs text-gray-400 mb-4">Payments in &quot;created&quot; status for &gt;1 hour</p>
              {(() => {
                const stale = payments.filter(p => p.status === 'created' && Date.now() - new Date(p.created_at).getTime() > 60 * 60 * 1000);
                return stale.length === 0 ? (
                  <div className="flex items-center gap-2 text-green-400">
                    <CheckCircle className="h-4 w-4" /><span className="text-sm">All clear \u2014 no stuck payments</span>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p className="text-yellow-400 text-sm font-medium">{stale.length} stuck payment{stale.length > 1 ? 's' : ''} found</p>
                    {stale.map((p, i) => (
                      <div key={i} className="p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg text-sm">
                        <p className="text-white">{p.user_email} \u2014 \u20b9{p.amount} ({p.report_type?.replace(/_/g,' ')})</p>
                        <div className="flex items-center gap-3 mt-1">
                          <span className="text-gray-400 text-xs font-mono">{p.razorpay_order_id}</span>
                          <button onClick={() => copyToClipboard(p.razorpay_order_id, 'Order ID')} className="text-gold text-xs hover:underline">Copy</button>
                        </div>
                        <p className="text-gray-500 text-xs mt-1">{new Date(p.created_at).toLocaleString()}</p>
                      </div>
                    ))}
                  </div>
                );
              })()}
            </Card>
          </div>
        )}

        {/* USERS */}
        {activeTab === 'users' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-semibold text-white">Users ({filteredUsers.length})</h3>
              <div className="flex items-center gap-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                  <input type="text" placeholder="Name / email / ID..." value={userSearch} onChange={e => setUserSearch(e.target.value)}
                    className="bg-gray-700 border border-gray-600 text-white rounded-md pl-8 pr-3 py-1.5 text-sm w-52 focus:outline-none focus:ring-1 focus:ring-gold" />
                </div>
                <Button onClick={fetchDashboardData} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                  <RefreshCw className="h-3.5 w-3.5" />
                </Button>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-400 border-b border-gray-700 text-xs uppercase tracking-wider">
                    <th className="pb-3 pr-3">Name</th>
                    <th className="pb-3 pr-3">Email</th>
                    <th className="pb-3 pr-3">User ID</th>
                    <th className="pb-3 pr-3">Auth</th>
                    <th className="pb-3 pr-3">Joined</th>
                    <th className="pb-3 pr-3">Status</th>
                    <th className="pb-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user, i) => {
                    const status = getUserStatus(user);
                    return (
                      <tr key={i} className="border-b border-gray-700/50 hover:bg-gray-700/20">
                        <td className="py-3 pr-3 text-white font-medium">{user.name}</td>
                        <td className="py-3 pr-3">
                          <div className="flex items-center gap-1 group">
                            <span className="text-gray-400 text-xs">{user.email}</span>
                            <button onClick={() => copyToClipboard(user.email, 'Email')} className="opacity-0 group-hover:opacity-100 text-gold p-0.5">
                              <Copy className="h-3 w-3" />
                            </button>
                          </div>
                        </td>
                        <td className="py-3 pr-3"><MonoID id={user.user_id} label="User ID" /></td>
                        <td className="py-3 pr-3">
                          <span className={`px-2 py-0.5 rounded text-xs ${user.google_id ? 'bg-blue-500/20 text-blue-400' : 'bg-gray-600/20 text-gray-400'}`}>
                            {user.google_id ? 'Google' : 'Email'}
                          </span>
                        </td>
                        <td className="py-3 pr-3 text-gray-400 text-xs">{new Date(user.created_at).toLocaleDateString()}</td>
                        <td className="py-3 pr-3"><StatusBadge status={status.label.toLowerCase()} /></td>
                        <td className="py-3">
                          <div className="flex items-center gap-1">
                            {!user.is_restricted
                              ? <button onClick={() => handleUserAction(user.user_id,'restrict')} disabled={!!actionLoading} title="Restrict" className="p-1.5 rounded bg-yellow-500/10 text-yellow-400 hover:bg-yellow-500/20 disabled:opacity-50"><ShieldOff className="h-3.5 w-3.5" /></button>
                              : <button onClick={() => handleUserAction(user.user_id,'unrestrict')} disabled={!!actionLoading} title="Unrestrict" className="p-1.5 rounded bg-green-500/10 text-green-400 hover:bg-green-500/20 disabled:opacity-50"><ShieldCheck className="h-3.5 w-3.5" /></button>}
                            {!user.is_suspended
                              ? <button onClick={() => handleUserAction(user.user_id,'suspend')} disabled={!!actionLoading} title="Suspend" className="p-1.5 rounded bg-orange-500/10 text-orange-400 hover:bg-orange-500/20 disabled:opacity-50"><Ban className="h-3.5 w-3.5" /></button>
                              : <button onClick={() => handleUserAction(user.user_id,'unsuspend')} disabled={!!actionLoading} title="Unsuspend" className="p-1.5 rounded bg-green-500/10 text-green-400 hover:bg-green-500/20 disabled:opacity-50"><ShieldCheck className="h-3.5 w-3.5" /></button>}
                            <button onClick={() => handleDeleteUser(user.user_id, user.name)} disabled={!!actionLoading} title="Delete" className="p-1.5 rounded bg-red-500/10 text-red-400 hover:bg-red-500/20 disabled:opacity-50"><Trash2 className="h-3.5 w-3.5" /></button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              {filteredUsers.length === 0 && <p className="text-gray-500 text-center py-8">No users found</p>}
            </div>
          </Card>
        )}

        {/* REPORTS */}
        {activeTab === 'reports' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-semibold text-white">Reports Tracker ({filteredReports.length})</h3>
              <div className="flex items-center gap-2 flex-wrap">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                  <input type="text" placeholder="Search by ID..." value={reportSearch} onChange={e => setReportSearch(e.target.value)}
                    className="bg-gray-700 border border-gray-600 text-white rounded-md pl-8 pr-3 py-1.5 text-sm w-44 focus:outline-none focus:ring-1 focus:ring-gold" />
                </div>
                <select value={reportFilter} onChange={e => setReportFilter(e.target.value)}
                  className="bg-gray-700 border border-gray-600 text-white rounded-md px-3 py-1.5 text-sm focus:outline-none">
                  <option value="all">All Types</option>
                  <option value="birth">Birth Chart</option>
                  <option value="kundali">Kundali Milan</option>
                </select>
                <Button onClick={fetchReports} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                  <RefreshCw className="h-3.5 w-3.5" />
                </Button>
              </div>
            </div>
            {filteredReports.length === 0 ? (
              <div className="text-center py-12">
                <FileText className="h-10 w-10 text-gray-600 mx-auto mb-3" />
                <p className="text-gray-500 mb-3">No reports yet, or click Refresh to load</p>
                <Button onClick={fetchReports} className="bg-gold hover:bg-gold/90 text-gray-900" size="sm">
                  <RefreshCw className="h-3.5 w-3.5 mr-1.5" />Load Reports
                </Button>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left text-gray-400 border-b border-gray-700 text-xs uppercase tracking-wider">
                      <th className="pb-3 pr-3">Type</th>
                      <th className="pb-3 pr-3">Report ID</th>
                      <th className="pb-3 pr-3">Profile / Person IDs</th>
                      <th className="pb-3 pr-3">Generated</th>
                      <th className="pb-3">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredReports.map((r, i) => {
                      const Icon = r.icon;
                      return (
                        <tr key={i} className="border-b border-gray-700/50 hover:bg-gray-700/20">
                          <td className="py-3 pr-3">
                            <span className={`flex items-center gap-1.5 text-xs font-medium ${r.color}`}>
                              <Icon className="h-3.5 w-3.5" />{r.type}
                            </span>
                          </td>
                          <td className="py-3 pr-3"><MonoID id={r.id} label="Report ID" /></td>
                          <td className="py-3 pr-3">
                            {r.profile_id && <MonoID id={r.profile_id} label="Profile ID" />}
                            {r.person1_id && (
                              <div className="space-y-0.5">
                                <div className="text-gray-500 text-xs">P1: <MonoID id={r.person1_id} label="Person 1 ID" /></div>
                                <div className="text-gray-500 text-xs">P2: <MonoID id={r.person2_id} label="Person 2 ID" /></div>
                              </div>
                            )}
                          </td>
                          <td className="py-3 pr-3 text-gray-400 text-xs">
                            {r.generated_at ? new Date(r.generated_at).toLocaleString() : '\u2014'}
                          </td>
                          <td className="py-3"><StatusBadge status="generated" /></td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </Card>
        )}

        {/* PAYMENTS */}
        {activeTab === 'payments' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-semibold text-white">Payments ({filteredPayments.length})</h3>
                <p className="text-xs text-gray-400 mt-0.5">Revenue: <span className="text-green-400 font-semibold">\u20b9{(stats?.total_revenue||0).toLocaleString()}</span></p>
              </div>
              <div className="flex gap-2">
                <select value={paymentFilter} onChange={e => setPaymentFilter(e.target.value)}
                  className="bg-gray-700 border border-gray-600 text-white rounded-md px-3 py-1.5 text-sm focus:outline-none">
                  <option value="all">All Status</option>
                  <option value="completed">Completed</option>
                  <option value="created">Created (Pending)</option>
                  <option value="failed">Failed</option>
                </select>
                <Button onClick={fetchDashboardData} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                  <RefreshCw className="h-3.5 w-3.5" />
                </Button>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-400 border-b border-gray-700 text-xs uppercase tracking-wider">
                    <th className="pb-3 pr-3">User</th>
                    <th className="pb-3 pr-3">Report Type</th>
                    <th className="pb-3 pr-3">Amount</th>
                    <th className="pb-3 pr-3">Order ID</th>
                    <th className="pb-3 pr-3">Status</th>
                    <th className="pb-3">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPayments.map((p, i) => (
                    <tr key={i} className="border-b border-gray-700/50 hover:bg-gray-700/20">
                      <td className="py-3 pr-3 text-gray-400 text-xs">{p.user_email}</td>
                      <td className="py-3 pr-3 text-white capitalize">{p.report_type?.replace(/_/g,' ')}</td>
                      <td className="py-3 pr-3 text-white font-medium">\u20b9{p.amount}</td>
                      <td className="py-3 pr-3"><MonoID id={p.razorpay_order_id} label="Order ID" /></td>
                      <td className="py-3 pr-3"><StatusBadge status={p.status} /></td>
                      <td className="py-3 text-gray-400 text-xs">{new Date(p.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {filteredPayments.length === 0 && <p className="text-gray-500 text-center py-8">No payments found</p>}
            </div>
            {/* Explain Created status */}
            <div className="mt-4 pt-4 border-t border-gray-700 text-xs text-gray-500">
              <span className="inline-flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-yellow-400 inline-block" />Created = payment order initiated, awaiting Razorpay confirmation</span>
              <span className="ml-4 inline-flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-400 inline-block" />Completed = payment verified, report access granted</span>
            </div>
          </Card>
        )}

        {/* CONTACTS */}
        {activeTab === 'contacts' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-semibold text-white flex items-center gap-2">
                <MessageSquare className="h-4 w-4 text-gold" />Messages ({contacts.length})
              </h3>
              <Button onClick={fetchContacts} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                <RefreshCw className="h-3.5 w-3.5 mr-1.5" />Refresh
              </Button>
            </div>
            <div className="space-y-3">
              {contacts.map((msg, i) => (
                <div key={i} className="p-4 bg-gray-700/50 rounded-lg border border-gray-600">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="text-white font-medium">{msg.name}</p>
                      <p className="text-gray-400 text-sm">{msg.email}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-gray-500 text-xs">{new Date(msg.created_at).toLocaleString()}</p>
                      {/* ← FIX: in-app reply button instead of mailto */}
                      <button
                        onClick={() => setReplyMsg(msg)}
                        className="text-gold text-xs hover:underline flex items-center justify-end gap-1 mt-1"
                      >
                        <Mail className="h-3 w-3" />Reply
                      </button>
                    </div>
                  </div>
                  {msg.subject && <p className="text-gold text-sm font-medium mb-1">{msg.subject}</p>}
                  <p className="text-gray-300 text-sm leading-relaxed">{msg.message}</p>
                </div>
              ))}
              {contacts.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                  <MessageSquare className="h-10 w-10 mx-auto mb-3 opacity-30" />
                  <p>No messages yet</p>
                </div>
              )}
            </div>
          </Card>
        )}

        {/* BLOG */}
        {activeTab === 'blog' && <AdminBlogManager getAuthHeaders={getAuthHeaders} />}

        {/* NOTIFICATIONS */}
        {activeTab === 'notifications' && (
          <div className="space-y-6">
            {/* Sub-nav */}
            <div className="flex flex-wrap gap-2">
              {[
                { id: 'subscribers', label: 'Subscribers',  icon: Users },
                { id: 'compose',     label: 'Compose',      icon: Send },
                { id: 'scheduled',   label: 'Scheduled',    icon: CalendarClock },
                { id: 'history',     label: 'History',      icon: History },
                { id: 'social',      label: 'Social Media', icon: Globe },
              ].map(({ id, label, icon: Icon }) => (
                <Button key={id} onClick={() => setNotifTab(id)} size="sm"
                  className={notifTab === id ? 'bg-gold/20 text-gold border border-gold/40' : 'border-gray-600 text-gray-400 hover:bg-gray-700'}
                  variant="outline">
                  <Icon className="h-3.5 w-3.5 mr-1.5" />{label}
                </Button>
              ))}
            </div>

            {/* SUBSCRIBERS */}
            {notifTab === 'subscribers' && (
              <div className="space-y-4">
                {/* Add form */}
                <Card className="p-5 bg-gray-800 border-gray-700">
                  <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
                    <PlusCircle className="h-4 w-4 text-gold" />Add Subscriber
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                    <div>
                      <Label className="text-gray-400 text-xs mb-1 block">Name *</Label>
                      <Input value={subForm.name} onChange={e => setSubForm(p => ({ ...p, name: e.target.value }))}
                        placeholder="Full name" className="bg-gray-700 border-gray-600 text-white text-sm" />
                    </div>
                    <div>
                      <Label className="text-gray-400 text-xs mb-1 block flex items-center gap-1"><Mail className="h-3 w-3" />Email</Label>
                      <Input value={subForm.email} onChange={e => setSubForm(p => ({ ...p, email: e.target.value }))}
                        placeholder="user@example.com" type="email" className="bg-gray-700 border-gray-600 text-white text-sm" />
                    </div>
                    <div>
                      <Label className="text-gray-400 text-xs mb-1 block flex items-center gap-1"><Phone className="h-3 w-3" />Phone (WhatsApp)</Label>
                      <Input value={subForm.phone} onChange={e => setSubForm(p => ({ ...p, phone: e.target.value }))}
                        placeholder="+919876543210" className="bg-gray-700 border-gray-600 text-white text-sm" />
                    </div>
                    <div>
                      <Label className="text-gray-400 text-xs mb-1 block flex items-center gap-1"><Tag className="h-3 w-3" />Tags (comma-separated)</Label>
                      <Input value={subForm.tags} onChange={e => setSubForm(p => ({ ...p, tags: e.target.value }))}
                        placeholder="premium, panchang" className="bg-gray-700 border-gray-600 text-white text-sm" />
                    </div>
                  </div>
                  <Button onClick={handleAddSubscriber} size="sm" className="mt-3 bg-gold hover:bg-gold/90 text-gray-900">
                    <PlusCircle className="h-3.5 w-3.5 mr-1.5" />Add Subscriber
                  </Button>
                </Card>

                {/* Subscriber list */}
                <Card className="p-5 bg-gray-800 border-gray-700">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                      <Users className="h-4 w-4 text-blue-400" />All Subscribers
                      <span className="text-xs text-gray-400 font-normal">({subscribers.length})</span>
                    </h3>
                    <div className="flex gap-2">
                      <div className="relative">
                        <Search className="h-3.5 w-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
                        <Input value={subSearch} onChange={e => setSubSearch(e.target.value)}
                          placeholder="Search..." className="bg-gray-700 border-gray-600 text-white text-sm pl-8 w-40" />
                      </div>
                      <Button onClick={fetchSubscribers} variant="outline" size="sm" className="border-gray-600 text-gray-300" disabled={subLoading}>
                        <RefreshCw className={`h-3.5 w-3.5 ${subLoading ? 'animate-spin' : ''}`} />
                      </Button>
                    </div>
                  </div>
                  <div className="space-y-2 max-h-[480px] overflow-y-auto">
                    {subscribers
                      .filter(s => !subSearch || s.name?.toLowerCase().includes(subSearch.toLowerCase()) || s.email?.includes(subSearch) || s.phone?.includes(subSearch))
                      .map(sub => (
                        <div key={sub.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
                          {editingSub?.id === sub.id ? (
                            <div className="flex flex-1 gap-2 mr-2 flex-wrap">
                              <Input value={editingSub.name} onChange={e => setEditingSub(p => ({ ...p, name: e.target.value }))}
                                className="bg-gray-600 border-gray-500 text-white text-xs h-8 w-28" />
                              <Input value={editingSub.email || ''} onChange={e => setEditingSub(p => ({ ...p, email: e.target.value }))}
                                className="bg-gray-600 border-gray-500 text-white text-xs h-8 w-36" placeholder="email" />
                              <Input value={editingSub.phone || ''} onChange={e => setEditingSub(p => ({ ...p, phone: e.target.value }))}
                                className="bg-gray-600 border-gray-500 text-white text-xs h-8 w-32" placeholder="phone" />
                              <Input value={(editingSub.tags || []).join(', ')} onChange={e => setEditingSub(p => ({ ...p, tags: e.target.value.split(',').map(t => t.trim()).filter(Boolean) }))}
                                className="bg-gray-600 border-gray-500 text-white text-xs h-8 w-32" placeholder="tags" />
                              <Button size="sm" className="h-8 bg-gold/20 text-gold border border-gold/30 text-xs"
                                onClick={() => handleUpdateSubscriber(sub.id, { name: editingSub.name, email: editingSub.email, phone: editingSub.phone, tags: editingSub.tags })}>
                                Save
                              </Button>
                              <Button size="sm" variant="outline" className="h-8 border-gray-600 text-gray-400 text-xs" onClick={() => setEditingSub(null)}>Cancel</Button>
                            </div>
                          ) : (
                            <div className="flex items-center gap-3 flex-1">
                              <div className={`w-2 h-2 rounded-full flex-shrink-0 ${sub.active ? 'bg-green-400' : 'bg-gray-500'}`} />
                              <div>
                                <p className="text-white text-sm font-medium">{sub.name}</p>
                                <div className="flex items-center gap-3 text-xs text-gray-400 mt-0.5">
                                  {sub.email && <span className="flex items-center gap-1"><Mail className="h-3 w-3" />{sub.email}</span>}
                                  {sub.phone && <span className="flex items-center gap-1"><Phone className="h-3 w-3" />{sub.phone}</span>}
                                </div>
                                {sub.tags?.length > 0 && (
                                  <div className="flex gap-1 mt-1">
                                    {sub.tags.map(t => <span key={t} className="px-1.5 py-0.5 bg-gold/10 text-gold text-xs rounded">{t}</span>)}
                                  </div>
                                )}
                              </div>
                            </div>
                          )}
                          {editingSub?.id !== sub.id && (
                            <div className="flex gap-1.5 ml-2">
                              <Button size="sm" variant="outline" className="h-7 px-2 border-gray-600 text-gray-400 text-xs"
                                onClick={() => setEditingSub({ ...sub })}>Edit</Button>
                              <Button size="sm" variant="outline" className="h-7 px-2 border-red-800/50 text-red-400 text-xs hover:bg-red-900/20"
                                onClick={() => handleDeleteSubscriber(sub.id, sub.name)}>
                                <Trash2 className="h-3 w-3" />
                              </Button>
                            </div>
                          )}
                        </div>
                      ))}
                    {subscribers.length === 0 && !subLoading && <p className="text-gray-500 text-sm text-center py-6">No subscribers yet</p>}
                  </div>
                </Card>
              </div>
            )}

            {/* COMPOSE */}
            {notifTab === 'compose' && (
              <Card className="p-6 bg-gray-800 border-gray-700">
                <h3 className="text-sm font-semibold text-white mb-5 flex items-center gap-2">
                  <Send className="h-4 w-4 text-gold" />Compose Notification
                </h3>
                <div className="space-y-4 max-w-2xl">
                  <div>
                    <Label className="text-gray-300 text-xs mb-1 block">Subject / Title</Label>
                    <Input value={notifForm.subject} onChange={e => setNotifForm(p => ({ ...p, subject: e.target.value }))}
                      placeholder="e.g. Today's Panchang — 27 March 2026" className="bg-gray-700 border-gray-600 text-white" />
                  </div>
                  <div>
                    <Label className="text-gray-300 text-xs mb-1 block">Message Body (HTML supported)</Label>
                    <textarea value={notifForm.body} onChange={e => setNotifForm(p => ({ ...p, body: e.target.value }))}
                      rows={8} placeholder="<p>Hello {{name}},</p><p>Today's Tithi is...</p>"
                      className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white text-sm resize-y focus:outline-none focus:ring-1 focus:ring-gold font-mono" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label className="text-gray-300 text-xs mb-2 block">Channels</Label>
                      <div className="space-y-2">
                        {[
                          { id: 'email',    label: 'Email (Resend)', icon: Mail,  available: true },
                          { id: 'whatsapp', label: 'WhatsApp',       icon: Phone, available: false },
                        ].map(({ id, label, icon: Icon, available }) => (
                          <label key={id} className={`flex items-center gap-2 cursor-pointer ${!available ? 'opacity-40' : ''}`}>
                            <input type="checkbox" checked={notifForm.channels.includes(id)} disabled={!available}
                              onChange={e => setNotifForm(p => ({
                                ...p,
                                channels: e.target.checked ? [...p.channels, id] : p.channels.filter(c => c !== id)
                              }))}
                              className="rounded border-gray-600" />
                            <Icon className="h-3.5 w-3.5 text-gray-400" />
                            <span className="text-gray-300 text-sm">{label}</span>
                            {available
                              ? <Wifi className="h-3 w-3 text-green-400" />
                              : <span className="text-xs text-gray-500 ml-1">— coming soon</span>}
                          </label>
                        ))}
                      </div>
                    </div>
                    <div>
                      <Label className="text-gray-300 text-xs mb-2 block">Audience</Label>
                      <div className="space-y-2">
                        {[
                          { id: 'all',    label: 'All active subscribers' },
                          { id: 'tagged', label: 'Filter by tag' },
                        ].map(({ id, label }) => (
                          <label key={id} className="flex items-center gap-2 cursor-pointer">
                            <input type="radio" name="audience" value={id} checked={notifForm.audience === id}
                              onChange={() => setNotifForm(p => ({ ...p, audience: id }))} />
                            <span className="text-gray-300 text-sm">{label}</span>
                          </label>
                        ))}
                      </div>
                      {notifForm.audience === 'tagged' && (
                        <Input value={notifForm.tags} onChange={e => setNotifForm(p => ({ ...p, tags: e.target.value }))}
                          placeholder="premium, panchang" className="bg-gray-700 border-gray-600 text-white text-sm mt-2" />
                      )}
                    </div>
                  </div>
                  <div>
                    <Label className="text-gray-300 text-xs mb-1 block flex items-center gap-1">
                      <Clock className="h-3 w-3" />Schedule Date &amp; Time (leave blank to send now)
                    </Label>
                    <Input type="datetime-local" value={notifForm.scheduled_at}
                      onChange={e => setNotifForm(p => ({ ...p, scheduled_at: e.target.value }))}
                      className="bg-gray-700 border-gray-600 text-white" />
                  </div>
                  {notifResult && (
                    <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg text-sm text-green-400">
                      ✓ Sent to {notifResult.sent} subscriber{notifResult.sent !== 1 ? 's' : ''}
                      {notifResult.failed > 0 && <span className="text-red-400 ml-2">· {notifResult.failed} failed</span>}
                    </div>
                  )}
                  <div className="flex gap-3 pt-2">
                    <Button onClick={() => handleSendNotification(false)} disabled={notifSending}
                      className="bg-gold hover:bg-gold/90 text-gray-900">
                      <Send className="h-3.5 w-3.5 mr-1.5" />{notifSending ? 'Sending...' : 'Send Now'}
                    </Button>
                    <Button onClick={() => handleSendNotification(true)} disabled={notifSending} variant="outline"
                      className="border-gray-600 text-gray-300 hover:bg-gray-700">
                      <CalendarClock className="h-3.5 w-3.5 mr-1.5" />Schedule
                    </Button>
                  </div>
                </div>
              </Card>
            )}

            {/* SCHEDULED */}
            {notifTab === 'scheduled' && (
              <Card className="p-5 bg-gray-800 border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                    <CalendarClock className="h-4 w-4 text-gold" />Scheduled Notifications ({scheduled.length})
                  </h3>
                  <Button onClick={fetchScheduled} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                    <RefreshCw className="h-3.5 w-3.5" />
                  </Button>
                </div>
                {scheduled.length === 0
                  ? <p className="text-gray-500 text-sm text-center py-8">No pending scheduled notifications</p>
                  : <div className="space-y-3">
                    {scheduled.map(n => (
                      <div key={n.id} className="p-4 bg-gray-700/50 rounded-lg flex items-start justify-between gap-3">
                        <div>
                          <p className="text-white text-sm font-medium">{n.subject}</p>
                          <div className="flex items-center gap-3 mt-1 text-xs text-gray-400">
                            <span className="flex items-center gap-1"><Clock className="h-3 w-3" />{new Date(n.scheduled_at).toLocaleString('en-IN')}</span>
                            <span className="flex items-center gap-1"><Users className="h-3 w-3" />{n.audience}</span>
                            <span>{n.channels.join(', ')}</span>
                          </div>
                        </div>
                        <Button onClick={() => handleCancelScheduled(n.id)} size="sm" variant="outline"
                          className="border-red-800/50 text-red-400 hover:bg-red-900/20 text-xs flex-shrink-0">
                          <X className="h-3 w-3 mr-1" />Cancel
                        </Button>
                      </div>
                    ))}
                  </div>
                }
              </Card>
            )}

            {/* HISTORY */}
            {notifTab === 'history' && (
              <Card className="p-5 bg-gray-800 border-gray-700">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                    <History className="h-4 w-4 text-gold" />Send History ({notifLogs.length})
                  </h3>
                  <Button onClick={fetchNotifLogs} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                    <RefreshCw className="h-3.5 w-3.5" />
                  </Button>
                </div>
                {notifLogs.length === 0
                  ? <p className="text-gray-500 text-sm text-center py-8">No notification history yet</p>
                  : <div className="space-y-2 max-h-[500px] overflow-y-auto">
                    {notifLogs.map(log => (
                      <div key={log.id} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
                        <div className="flex items-center gap-3">
                          {log.status === 'sent'
                            ? <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                            : <AlertTriangle className="h-4 w-4 text-red-400 flex-shrink-0" />}
                          <div>
                            <p className="text-white text-sm">{log.recipient_name}
                              <span className="text-gray-400 ml-2 text-xs">{log.recipient_email || log.recipient_phone || '—'}</span>
                            </p>
                            <p className="text-gray-400 text-xs">{log.subject} · {log.channel}
                              {log.error && <span className="text-red-400 ml-2">· {log.error}</span>}
                            </p>
                          </div>
                        </div>
                        <span className="text-gray-500 text-xs flex-shrink-0">{new Date(log.sent_at).toLocaleString('en-IN')}</span>
                      </div>
                    ))}
                  </div>
                }
              </Card>
            )}

            {/* SOCIAL MEDIA */}
            {notifTab === 'social' && (
              <div className="space-y-4">
                {/* Compose */}
                <Card className="p-5 bg-gray-800 border-gray-700">
                  <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
                    <Globe className="h-4 w-4 text-gold" />Post to Social Media
                  </h3>

                  {/* Channels */}
                  <div className="mb-4">
                    <Label className="text-gray-400 text-xs mb-2 block">Channels</Label>
                    <div className="flex flex-wrap gap-3">
                      {[
                        { id: 'facebook',  label: 'Facebook',  available: true },
                        { id: 'instagram', label: 'Instagram', available: false },
                        { id: 'x',         label: 'X (Twitter)', available: false },
                        { id: 'youtube',   label: 'YouTube',   available: false },
                      ].map(({ id, label, available }) => (
                        <label key={id} className={`flex items-center gap-2 text-sm cursor-pointer ${!available ? 'opacity-50' : ''}`}>
                          <input type="checkbox" disabled={!available}
                            checked={socialForm.channels.includes(id)}
                            onChange={e => setSocialForm(p => ({
                              ...p,
                              channels: e.target.checked ? [...p.channels, id] : p.channels.filter(c => c !== id)
                            }))}
                            className="accent-yellow-500"
                          />
                          <span className="text-gray-300">{label}</span>
                          {!available && <span className="text-xs text-gray-500">— coming soon</span>}
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Message */}
                  <div className="mb-3">
                    <Label className="text-gray-400 text-xs mb-1 block">Caption / Message</Label>
                    <textarea
                      value={socialForm.message}
                      onChange={e => setSocialForm(p => ({ ...p, message: e.target.value }))}
                      placeholder="Write your post caption here... Use {{date}}, {{tithi}}, etc. for dynamic content."
                      rows={5}
                      className="w-full bg-gray-700 border border-gray-600 text-white text-sm rounded-md p-3 resize-y focus:outline-none focus:ring-1 focus:ring-yellow-500"
                    />
                    <p className="text-gray-500 text-xs mt-1">{socialForm.message.length} characters</p>
                  </div>

                  {/* Image URL */}
                  <div className="mb-4">
                    <Label className="text-gray-400 text-xs mb-1 block flex items-center gap-1">
                      <Image className="h-3 w-3" />Image URL (optional — leave blank for text-only post)
                    </Label>
                    <Input
                      value={socialForm.image_url}
                      onChange={e => setSocialForm(p => ({ ...p, image_url: e.target.value }))}
                      placeholder="https://example.com/image.jpg"
                      className="bg-gray-700 border-gray-600 text-white text-sm"
                    />
                  </div>

                  <Button onClick={handleSocialPost} disabled={socialPosting}
                    className="bg-gold hover:bg-gold/90 text-gray-900 font-semibold">
                    <Globe className="h-4 w-4 mr-2" />
                    {socialPosting ? 'Posting…' : 'Post Now'}
                  </Button>

                  {/* Results */}
                  {socialResults && (
                    <div className="mt-4 space-y-2">
                      {socialResults.map(r => (
                        <div key={r.channel} className={`flex items-center gap-3 p-3 rounded-lg ${r.success ? 'bg-green-900/30 border border-green-700/40' : 'bg-red-900/30 border border-red-700/40'}`}>
                          {r.success
                            ? <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                            : <AlertTriangle className="h-4 w-4 text-red-400 flex-shrink-0" />}
                          <div>
                            <p className="text-white text-sm capitalize font-medium">{r.channel}</p>
                            {r.success
                              ? <p className="text-green-400 text-xs">Posted · ID: {r.post_id}</p>
                              : <p className="text-red-400 text-xs">{r.error}</p>}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </Card>

                {/* Social Post History */}
                <Card className="p-5 bg-gray-800 border-gray-700">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                      <History className="h-4 w-4 text-gold" />Post History ({socialLogs.length})
                    </h3>
                    <Button onClick={fetchSocialLogs} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                      <RefreshCw className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                  {socialLogs.length === 0
                    ? <p className="text-gray-500 text-sm text-center py-8">No posts yet</p>
                    : <div className="space-y-2 max-h-[400px] overflow-y-auto">
                      {socialLogs.map((log, i) => (
                        <div key={i} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
                          <div className="flex items-center gap-3">
                            {log.success
                              ? <CheckCircle className="h-4 w-4 text-green-400 flex-shrink-0" />
                              : <AlertTriangle className="h-4 w-4 text-red-400 flex-shrink-0" />}
                            <div>
                              <p className="text-white text-sm capitalize">{log.channel}
                                {log.post_id && <span className="text-gray-400 text-xs ml-2">· {log.post_id}</span>}
                              </p>
                              <p className="text-gray-400 text-xs">{log.message_preview}
                                {log.error && <span className="text-red-400 ml-2">· {log.error}</span>}
                              </p>
                            </div>
                          </div>
                          <span className="text-gray-500 text-xs flex-shrink-0">{new Date(log.posted_at).toLocaleString('en-IN')}</span>
                        </div>
                      ))}
                    </div>
                  }
                </Card>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
