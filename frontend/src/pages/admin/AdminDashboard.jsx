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
  Search, RefreshCw, MessageSquare, Mail
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';
import { AdminBlogManager } from './AdminBlogManager';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const AdminDashboard = () => {
  const navigate = useNavigate();
  const { logout, getAuthHeaders, isAuthenticated, loading: authLoading } = useAdminAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [users, setUsers] = useState([]);
  const [payments, setPayments] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [userSearch, setUserSearch] = useState('');
  const [actionLoading, setActionLoading] = useState(null);

  // Password change state
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showCurrentPwd, setShowCurrentPwd] = useState(false);
  const [showNewPwd, setShowNewPwd] = useState(false);
  const [changingPassword, setChangingPassword] = useState(false);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) navigate('/admin/login');
  }, [isAuthenticated, authLoading, navigate]);

  useEffect(() => {
    if (isAuthenticated) fetchDashboardData();
  }, [isAuthenticated]);

  const fetchDashboardData = async () => {
    try {
      const headers = getAuthHeaders();
      const [statsRes, usersRes, paymentsRes] = await Promise.all([
        axios.get(`${API}/admin/dashboard`, { headers }),
        axios.get(`${API}/admin/users?limit=100`, { headers }),
        axios.get(`${API}/admin/payments?limit=50`, { headers }),
      ]);
      setStats(statsRes.data);
      setUsers(usersRes.data.users);
      setPayments(paymentsRes.data.payments);
    } catch (error) {
      if (error.response?.status === 401) navigate('/admin/login');
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const fetchContacts = async () => {
    try {
      const headers = getAuthHeaders();
      const res = await axios.get(`${API}/admin/contacts`, { headers });
      setContacts(res.data.messages || []);
    } catch (error) {
      toast.error('Failed to load contact messages');
    }
  };

  useEffect(() => {
    if (activeTab === 'contacts') fetchContacts();
  }, [activeTab]);

  const handleUserAction = async (userId, action) => {
    setActionLoading(userId + action);
    try {
      const headers = getAuthHeaders();
      await axios.post(`${API}/admin/user/${userId}/action`, { action }, { headers });
      toast.success(`User ${action}ed successfully`);
      fetchDashboardData();
    } catch (error) {
      toast.error(error.response?.data?.detail || `Failed to ${action} user`);
    } finally {
      setActionLoading(null);
    }
  };

  const handleDeleteUser = async (userId, userName) => {
    if (!window.confirm(`Are you sure you want to permanently delete ${userName}? This cannot be undone.`)) return;
    setActionLoading(userId + 'delete');
    try {
      const headers = getAuthHeaders();
      await axios.delete(`${API}/admin/user/${userId}`, { headers });
      toast.success('User deleted successfully');
      fetchDashboardData();
    } catch (error) {
      toast.error('Failed to delete user');
    } finally {
      setActionLoading(null);
    }
  };

  const handleLogout = async () => { await logout(); navigate('/admin/login'); };

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) { toast.error('Passwords do not match'); return; }
    if (newPassword.length < 8) { toast.error('Password must be at least 8 characters'); return; }
    setChangingPassword(true);
    try {
      const headers = getAuthHeaders();
      await axios.post(`${API}/admin/change-password`, {
        current_password: currentPassword, new_password: newPassword
      }, { headers });
      toast.success('Password changed successfully');
      setShowPasswordModal(false);
      setCurrentPassword(''); setNewPassword(''); setConfirmPassword('');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to change password');
    } finally {
      setChangingPassword(false);
    }
  };

  const getUserStatus = (user) => {
    if (user.is_deleted) return { label: 'Deleted', color: 'bg-red-500/20 text-red-400' };
    if (user.is_suspended) return { label: 'Suspended', color: 'bg-orange-500/20 text-orange-400' };
    if (user.is_restricted) return { label: 'Restricted', color: 'bg-yellow-500/20 text-yellow-400' };
    if (user.locked_until) {
      const locked = new Date(user.locked_until);
      if (locked > new Date()) return { label: 'Locked', color: 'bg-purple-500/20 text-purple-400' };
    }
    return { label: 'Active', color: 'bg-green-500/20 text-green-400' };
  };

  const filteredUsers = users.filter(u =>
    u.name?.toLowerCase().includes(userSearch.toLowerCase()) ||
    u.email?.toLowerCase().includes(userSearch.toLowerCase())
  );

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-gold text-xl">Loading...</div>
      </div>
    );
  }

  const statCards = [
    { label: 'Total Users', value: stats?.total_users || 0, icon: Users, color: 'text-blue-400', bgColor: 'bg-blue-400/10', change: stats?.users_today, changeLabel: 'today' },
    { label: 'Total Revenue', value: `₹${(stats?.total_revenue || 0).toLocaleString()}`, icon: IndianRupee, color: 'text-green-400', bgColor: 'bg-green-400/10', change: stats?.payments_today, changeLabel: 'payments today' },
    { label: 'Birth Charts', value: stats?.total_birth_charts || 0, icon: FileText, color: 'text-purple-400', bgColor: 'bg-purple-400/10' },
    { label: 'Kundali Milans', value: stats?.total_kundali_milans || 0, icon: Crown, color: 'text-pink-400', bgColor: 'bg-pink-400/10' },
    { label: 'Active Subscriptions', value: stats?.active_subscriptions || 0, icon: TrendingUp, color: 'text-gold', bgColor: 'bg-gold/10' },
    { label: 'Total Payments', value: stats?.total_payments || 0, icon: CreditCard, color: 'text-cyan-400', bgColor: 'bg-cyan-400/10' },
  ];

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3 },
    { id: 'users', label: 'Users', icon: Users },
    { id: 'payments', label: 'Payments', icon: CreditCard },
    { id: 'contacts', label: 'Messages', icon: MessageSquare },
    { id: 'blog', label: 'Blog', icon: BookOpen },
  ];

  return (
    <div className="min-h-screen bg-gray-900">

      {/* Password Modal */}
      {showPasswordModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md p-6 bg-gray-800 border-gray-700 mx-4">
            <div className="flex items-center space-x-2 mb-6">
              <Lock className="h-5 w-5 text-gold" />
              <h2 className="text-xl font-bold text-white">Change Password</h2>
            </div>
            <div className="space-y-4">
              <div>
                <Label className="text-gray-300">Current Password</Label>
                <div className="relative">
                  <Input type={showCurrentPwd ? "text" : "password"} value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} className="bg-gray-700 border-gray-600 text-white pr-10" placeholder="Current password" />
                  <button type="button" onClick={() => setShowCurrentPwd(!showCurrentPwd)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                    {showCurrentPwd ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>
              <div>
                <Label className="text-gray-300">New Password</Label>
                <div className="relative">
                  <Input type={showNewPwd ? "text" : "password"} value={newPassword} onChange={e => setNewPassword(e.target.value)} className="bg-gray-700 border-gray-600 text-white pr-10" placeholder="Min 8 characters" />
                  <button type="button" onClick={() => setShowNewPwd(!showNewPwd)} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                    {showNewPwd ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>
              <div>
                <Label className="text-gray-300">Confirm New Password</Label>
                <Input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} className="bg-gray-700 border-gray-600 text-white" placeholder="Confirm new password" />
              </div>
            </div>
            <div className="flex space-x-3 mt-6">
              <Button onClick={() => setShowPasswordModal(false)} variant="outline" className="flex-1 border-gray-600 text-gray-300">Cancel</Button>
              <Button onClick={handleChangePassword} className="flex-1 bg-gold hover:bg-gold/90 text-gray-900" disabled={changingPassword}>
                {changingPassword ? 'Changing...' : 'Change Password'}
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <BarChart3 className="h-8 w-8 text-gold" />
            <h1 className="text-xl font-bold text-white">Admin Dashboard</h1>
          </div>
          <div className="flex items-center space-x-3">
            <Button onClick={() => setShowPasswordModal(true)} variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-700">
              <Settings className="h-4 w-4 mr-2" />Change Password
            </Button>
            <Button onClick={handleLogout} variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-700">
              <LogOut className="h-4 w-4 mr-2" />Logout
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {statCards.map((stat, i) => {
            const Icon = stat.icon;
            return (
              <Card key={i} className="p-6 bg-gray-800 border-gray-700">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">{stat.label}</p>
                    <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                    {stat.change !== undefined && (
                      <div className="flex items-center mt-2 text-sm">
                        <ArrowUpRight className="h-4 w-4 text-green-400 mr-1" />
                        <span className="text-green-400">{stat.change}</span>
                        <span className="text-gray-500 ml-1">{stat.changeLabel}</span>
                      </div>
                    )}
                  </div>
                  <div className={`${stat.bgColor} rounded-lg p-3`}>
                    <Icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Tabs */}
        <div className="flex flex-wrap gap-2 mb-6">
          {tabs.map(({ id, label, icon: Icon }) => (
            <Button key={id} variant={activeTab === id ? 'default' : 'outline'}
              onClick={() => setActiveTab(id)}
              className={activeTab === id ? 'bg-gold text-gray-900' : 'border-gray-600 text-gray-300 hover:bg-gray-700'}
            >
              <Icon className="h-4 w-4 mr-2" />{label}
            </Button>
          ))}
        </div>

        {/* OVERVIEW TAB */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="p-6 bg-gray-800 border-gray-700">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <Users className="h-5 w-5 mr-2 text-blue-400" />Recent Users
              </h3>
              <div className="space-y-3">
                {users.slice(0, 5).map((user, i) => {
                  const status = getUserStatus(user);
                  return (
                    <div key={i} className="flex items-center justify-between py-2 border-b border-gray-700 last:border-0">
                      <div>
                        <p className="text-white font-medium">{user.name}</p>
                        <p className="text-gray-400 text-sm">{user.email}</p>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs ${status.color}`}>{status.label}</span>
                    </div>
                  );
                })}
                {users.length === 0 && <p className="text-gray-500 text-center py-4">No users yet</p>}
              </div>
            </Card>
            <Card className="p-6 bg-gray-800 border-gray-700">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <CreditCard className="h-5 w-5 mr-2 text-green-400" />Recent Payments
              </h3>
              <div className="space-y-3">
                {payments.slice(0, 5).map((payment, i) => (
                  <div key={i} className="flex items-center justify-between py-2 border-b border-gray-700 last:border-0">
                    <div>
                      <p className="text-white font-medium">₹{payment.amount}</p>
                      <p className="text-gray-400 text-sm">{payment.report_type?.replace(/_/g, ' ')}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${payment.status === 'completed' ? 'bg-green-500/20 text-green-400' : payment.status === 'created' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'}`}>
                      {payment.status}
                    </span>
                  </div>
                ))}
                {payments.length === 0 && <p className="text-gray-500 text-center py-4">No payments yet</p>}
              </div>
            </Card>
          </div>
        )}

        {/* USERS TAB */}
        {activeTab === 'users' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">User Management</h3>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search users..."
                    value={userSearch}
                    onChange={e => setUserSearch(e.target.value)}
                    className="bg-gray-700 border border-gray-600 text-white rounded-md pl-9 pr-3 py-2 text-sm w-48 focus:outline-none focus:ring-1 focus:ring-gold"
                  />
                </div>
                <Button onClick={fetchDashboardData} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                  <RefreshCw className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-400 border-b border-gray-700">
                    <th className="pb-3 pr-3">Name</th>
                    <th className="pb-3 pr-3">Email</th>
                    <th className="pb-3 pr-3">Auth</th>
                    <th className="pb-3 pr-3">Joined</th>
                    <th className="pb-3 pr-3">Status</th>
                    <th className="pb-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user, i) => {
                    const status = getUserStatus(user);
                    const isLoading = (action) => actionLoading === user.user_id + action;
                    return (
                      <tr key={i} className="border-b border-gray-700/50 hover:bg-gray-700/20">
                        <td className="py-3 pr-3 text-white font-medium">{user.name}</td>
                        <td className="py-3 pr-3 text-gray-400">{user.email}</td>
                        <td className="py-3 pr-3">
                          <span className={`px-2 py-0.5 rounded text-xs ${user.google_id ? 'bg-blue-500/20 text-blue-400' : 'bg-gray-600/20 text-gray-400'}`}>
                            {user.google_id ? 'Google' : 'Email'}
                          </span>
                        </td>
                        <td className="py-3 pr-3 text-gray-400">
                          {new Date(user.created_at).toLocaleDateString()}
                        </td>
                        <td className="py-3 pr-3">
                          <span className={`px-2 py-0.5 rounded text-xs ${status.color}`}>{status.label}</span>
                        </td>
                        <td className="py-3">
                          <div className="flex items-center gap-1">
                            {!user.is_restricted ? (
                              <button
                                onClick={() => handleUserAction(user.user_id, 'restrict')}
                                disabled={!!actionLoading}
                                title="Restrict user"
                                className="p-1.5 rounded bg-yellow-500/10 text-yellow-400 hover:bg-yellow-500/20 disabled:opacity-50"
                              >
                                <ShieldOff className="h-3.5 w-3.5" />
                              </button>
                            ) : (
                              <button
                                onClick={() => handleUserAction(user.user_id, 'unrestrict')}
                                disabled={!!actionLoading}
                                title="Remove restriction"
                                className="p-1.5 rounded bg-green-500/10 text-green-400 hover:bg-green-500/20 disabled:opacity-50"
                              >
                                <ShieldCheck className="h-3.5 w-3.5" />
                              </button>
                            )}
                            {!user.is_suspended ? (
                              <button
                                onClick={() => handleUserAction(user.user_id, 'suspend')}
                                disabled={!!actionLoading}
                                title="Suspend user"
                                className="p-1.5 rounded bg-orange-500/10 text-orange-400 hover:bg-orange-500/20 disabled:opacity-50"
                              >
                                <Ban className="h-3.5 w-3.5" />
                              </button>
                            ) : (
                              <button
                                onClick={() => handleUserAction(user.user_id, 'unsuspend')}
                                disabled={!!actionLoading}
                                title="Unsuspend user"
                                className="p-1.5 rounded bg-green-500/10 text-green-400 hover:bg-green-500/20 disabled:opacity-50"
                              >
                                <ShieldCheck className="h-3.5 w-3.5" />
                              </button>
                            )}
                            <button
                              onClick={() => handleDeleteUser(user.user_id, user.name)}
                              disabled={!!actionLoading}
                              title="Delete user"
                              className="p-1.5 rounded bg-red-500/10 text-red-400 hover:bg-red-500/20 disabled:opacity-50"
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              {filteredUsers.length === 0 && (
                <p className="text-gray-500 text-center py-8">No users found</p>
              )}
            </div>

            {/* Legend */}
            <div className="mt-4 pt-4 border-t border-gray-700 flex flex-wrap gap-4 text-xs text-gray-400">
              <span className="flex items-center gap-1"><ShieldOff className="h-3 w-3 text-yellow-400" /> Restrict — limits access to premium features</span>
              <span className="flex items-center gap-1"><Ban className="h-3 w-3 text-orange-400" /> Suspend — blocks all access for 24hrs</span>
              <span className="flex items-center gap-1"><Trash2 className="h-3 w-3 text-red-400" /> Delete — permanent, cannot be undone</span>
            </div>
          </Card>
        )}

        {/* PAYMENTS TAB */}
        {activeTab === 'payments' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">All Payments</h3>
              <div className="text-sm text-gray-400">
                Total Revenue: <span className="text-green-400 font-semibold">₹{(stats?.total_revenue || 0).toLocaleString()}</span>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-gray-400 border-b border-gray-700">
                    <th className="pb-3 pr-4">User</th>
                    <th className="pb-3 pr-4">Report Type</th>
                    <th className="pb-3 pr-4">Amount</th>
                    <th className="pb-3 pr-4">Razorpay Order ID</th>
                    <th className="pb-3 pr-4">Status</th>
                    <th className="pb-3">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {payments.map((payment, i) => (
                    <tr key={i} className="border-b border-gray-700/50">
                      <td className="py-3 pr-4 text-gray-400">{payment.user_email}</td>
                      <td className="py-3 pr-4 text-white capitalize">{payment.report_type?.replace(/_/g, ' ')}</td>
                      <td className="py-3 pr-4 text-white font-medium">₹{payment.amount}</td>
                      <td className="py-3 pr-4 text-gray-500 text-xs font-mono">{payment.razorpay_order_id}</td>
                      <td className="py-3 pr-4">
                        <span className={`px-2 py-1 rounded text-xs ${payment.status === 'completed' ? 'bg-green-500/20 text-green-400' : payment.status === 'created' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'}`}>
                          {payment.status}
                        </span>
                      </td>
                      <td className="py-3 text-gray-400">{new Date(payment.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {payments.length === 0 && <p className="text-gray-500 text-center py-8">No payments yet</p>}
            </div>
          </Card>
        )}

        {/* CONTACTS TAB */}
        {activeTab === 'contacts' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                <MessageSquare className="h-5 w-5 text-gold" />Contact Messages
              </h3>
              <Button onClick={fetchContacts} variant="outline" size="sm" className="border-gray-600 text-gray-300">
                <RefreshCw className="h-4 w-4 mr-2" />Refresh
              </Button>
            </div>
            <div className="space-y-4">
              {contacts.map((msg, i) => (
                <div key={i} className="p-4 bg-gray-700/50 rounded-lg border border-gray-600">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <p className="text-white font-medium">{msg.name}</p>
                      <p className="text-gray-400 text-sm">{msg.email}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-gray-500 text-xs">{new Date(msg.created_at).toLocaleString()}</p>
                      <a href={`mailto:${msg.email}?subject=Re: ${msg.subject}`}
                        className="text-gold text-xs hover:underline flex items-center justify-end gap-1 mt-1">
                        <Mail className="h-3 w-3" />Reply
                      </a>
                    </div>
                  </div>
                  {msg.subject && <p className="text-gold text-sm font-medium mb-1">{msg.subject}</p>}
                  <p className="text-gray-300 text-sm leading-relaxed">{msg.message}</p>
                </div>
              ))}
              {contacts.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                  <MessageSquare className="h-12 w-12 mx-auto mb-3 opacity-30" />
                  <p>No contact messages yet</p>
                </div>
              )}
            </div>
          </Card>
        )}

        {/* BLOG TAB */}
        {activeTab === 'blog' && <AdminBlogManager getAuthHeaders={getAuthHeaders} />}
      </div>
    </div>
  );
};
