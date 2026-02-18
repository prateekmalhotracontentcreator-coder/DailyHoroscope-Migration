import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdminAuth } from '../../context/AdminAuthContext';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import { 
  Users, CreditCard, FileText, TrendingUp, 
  LogOut, Crown, Calendar, IndianRupee,
  BarChart3, ArrowUpRight, ArrowDownRight, Settings, Lock, Eye, EyeOff, BookOpen
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
  
  // Password change state
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showCurrentPwd, setShowCurrentPwd] = useState(false);
  const [showNewPwd, setShowNewPwd] = useState(false);
  const [changingPassword, setChangingPassword] = useState(false);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate('/admin/login');
    }
  }, [isAuthenticated, authLoading, navigate]);

  useEffect(() => {
    if (isAuthenticated) {
      fetchDashboardData();
    }
  }, [isAuthenticated]);

  const fetchDashboardData = async () => {
    try {
      const headers = getAuthHeaders();
      
      const [statsRes, usersRes, paymentsRes] = await Promise.all([
        axios.get(`${API}/admin/dashboard`, { headers }),
        axios.get(`${API}/admin/users?limit=10`, { headers }),
        axios.get(`${API}/admin/payments?limit=10`, { headers })
      ]);
      
      setStats(statsRes.data);
      setUsers(usersRes.data.users);
      setPayments(paymentsRes.data.payments);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      if (error.response?.status === 401) {
        navigate('/admin/login');
      }
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/admin/login');
  };

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      toast.error('New passwords do not match');
      return;
    }
    if (newPassword.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }

    setChangingPassword(true);
    try {
      const headers = getAuthHeaders();
      await axios.post(`${API}/admin/change-password`, {
        current_password: currentPassword,
        new_password: newPassword
      }, { headers });
      
      toast.success('Password changed successfully');
      setShowPasswordModal(false);
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to change password');
    } finally {
      setChangingPassword(false);
    }
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-gold text-xl">Loading...</div>
      </div>
    );
  }

  const statCards = [
    { 
      label: 'Total Users', 
      value: stats?.total_users || 0, 
      icon: Users, 
      color: 'text-blue-400',
      bgColor: 'bg-blue-400/10',
      change: stats?.users_today || 0,
      changeLabel: 'today'
    },
    { 
      label: 'Total Revenue', 
      value: `₹${(stats?.total_revenue || 0).toLocaleString()}`, 
      icon: IndianRupee, 
      color: 'text-green-400',
      bgColor: 'bg-green-400/10',
      change: stats?.payments_today || 0,
      changeLabel: 'payments today'
    },
    { 
      label: 'Birth Charts', 
      value: stats?.total_birth_charts || 0, 
      icon: FileText, 
      color: 'text-purple-400',
      bgColor: 'bg-purple-400/10'
    },
    { 
      label: 'Kundali Milans', 
      value: stats?.total_kundali_milans || 0, 
      icon: Crown, 
      color: 'text-pink-400',
      bgColor: 'bg-pink-400/10'
    },
    { 
      label: 'Active Subscriptions', 
      value: stats?.active_subscriptions || 0, 
      icon: TrendingUp, 
      color: 'text-gold',
      bgColor: 'bg-gold/10'
    },
    { 
      label: 'Total Payments', 
      value: stats?.total_payments || 0, 
      icon: CreditCard, 
      color: 'text-cyan-400',
      bgColor: 'bg-cyan-400/10'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Password Change Modal */}
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
                  <Input
                    type={showCurrentPwd ? "text" : "password"}
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white pr-10"
                    placeholder="Enter current password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowCurrentPwd(!showCurrentPwd)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                  >
                    {showCurrentPwd ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>
              
              <div>
                <Label className="text-gray-300">New Password</Label>
                <div className="relative">
                  <Input
                    type={showNewPwd ? "text" : "password"}
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="bg-gray-700 border-gray-600 text-white pr-10"
                    placeholder="Enter new password (min 8 chars)"
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPwd(!showNewPwd)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                  >
                    {showNewPwd ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>
              
              <div>
                <Label className="text-gray-300">Confirm New Password</Label>
                <Input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="bg-gray-700 border-gray-600 text-white"
                  placeholder="Confirm new password"
                />
              </div>
            </div>
            
            <div className="flex space-x-3 mt-6">
              <Button
                onClick={() => setShowPasswordModal(false)}
                variant="outline"
                className="flex-1 border-gray-600 text-gray-300 hover:bg-gray-700"
              >
                Cancel
              </Button>
              <Button
                onClick={handleChangePassword}
                className="flex-1 bg-gold hover:bg-gold/90 text-gray-900"
                disabled={changingPassword}
              >
                {changingPassword ? 'Changing...' : 'Change Password'}
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <BarChart3 className="h-8 w-8 text-gold" />
              <h1 className="text-xl font-bold text-white">Admin Dashboard</h1>
            </div>
            <div className="flex items-center space-x-3">
              <Button
                onClick={() => setShowPasswordModal(true)}
                variant="outline"
                className="border-gray-600 text-gray-300 hover:bg-gray-700"
                data-testid="change-password-btn"
              >
                <Settings className="h-4 w-4 mr-2" />
                Change Password
              </Button>
              <Button
                onClick={handleLogout}
                variant="outline"
                className="border-gray-600 text-gray-300 hover:bg-gray-700"
                data-testid="admin-logout-btn"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {statCards.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <Card 
                key={index} 
                className="p-6 bg-gray-800 border-gray-700"
                data-testid={`stat-card-${stat.label.toLowerCase().replace(/\s/g, '-')}`}
              >
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
        <div className="flex space-x-4 mb-6">
          {['overview', 'users', 'payments'].map((tab) => (
            <Button
              key={tab}
              variant={activeTab === tab ? 'default' : 'outline'}
              onClick={() => setActiveTab(tab)}
              className={activeTab === tab 
                ? 'bg-gold text-gray-900' 
                : 'border-gray-600 text-gray-300 hover:bg-gray-700'
              }
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </Button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Recent Users */}
            <Card className="p-6 bg-gray-800 border-gray-700">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <Users className="h-5 w-5 mr-2 text-blue-400" />
                Recent Users
              </h3>
              <div className="space-y-3">
                {users.slice(0, 5).map((user, index) => (
                  <div key={index} className="flex items-center justify-between py-2 border-b border-gray-700 last:border-0">
                    <div>
                      <p className="text-white font-medium">{user.name}</p>
                      <p className="text-gray-400 text-sm">{user.email}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${
                      user.google_id ? 'bg-blue-500/20 text-blue-400' : 'bg-gray-600/20 text-gray-400'
                    }`}>
                      {user.google_id ? 'Google' : 'Email'}
                    </span>
                  </div>
                ))}
                {users.length === 0 && (
                  <p className="text-gray-500 text-center py-4">No users yet</p>
                )}
              </div>
            </Card>

            {/* Recent Payments */}
            <Card className="p-6 bg-gray-800 border-gray-700">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <CreditCard className="h-5 w-5 mr-2 text-green-400" />
                Recent Payments
              </h3>
              <div className="space-y-3">
                {payments.slice(0, 5).map((payment, index) => (
                  <div key={index} className="flex items-center justify-between py-2 border-b border-gray-700 last:border-0">
                    <div>
                      <p className="text-white font-medium">₹{payment.amount}</p>
                      <p className="text-gray-400 text-sm">{payment.report_type}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${
                      payment.status === 'completed' 
                        ? 'bg-green-500/20 text-green-400' 
                        : payment.status === 'created'
                        ? 'bg-yellow-500/20 text-yellow-400'
                        : 'bg-red-500/20 text-red-400'
                    }`}>
                      {payment.status}
                    </span>
                  </div>
                ))}
                {payments.length === 0 && (
                  <p className="text-gray-500 text-center py-4">No payments yet</p>
                )}
              </div>
            </Card>
          </div>
        )}

        {activeTab === 'users' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">All Users</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-gray-400 border-b border-gray-700">
                    <th className="pb-3 pr-4">Name</th>
                    <th className="pb-3 pr-4">Email</th>
                    <th className="pb-3 pr-4">Auth Type</th>
                    <th className="pb-3">Joined</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user, index) => (
                    <tr key={index} className="border-b border-gray-700/50">
                      <td className="py-3 pr-4 text-white">{user.name}</td>
                      <td className="py-3 pr-4 text-gray-400">{user.email}</td>
                      <td className="py-3 pr-4">
                        <span className={`px-2 py-1 rounded text-xs ${
                          user.google_id ? 'bg-blue-500/20 text-blue-400' : 'bg-gray-600/20 text-gray-400'
                        }`}>
                          {user.google_id ? 'Google' : 'Email'}
                        </span>
                      </td>
                      <td className="py-3 text-gray-400 text-sm">
                        {new Date(user.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}

        {activeTab === 'payments' && (
          <Card className="p-6 bg-gray-800 border-gray-700">
            <h3 className="text-lg font-semibold text-white mb-4">All Payments</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-gray-400 border-b border-gray-700">
                    <th className="pb-3 pr-4">User</th>
                    <th className="pb-3 pr-4">Type</th>
                    <th className="pb-3 pr-4">Amount</th>
                    <th className="pb-3 pr-4">Status</th>
                    <th className="pb-3">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {payments.map((payment, index) => (
                    <tr key={index} className="border-b border-gray-700/50">
                      <td className="py-3 pr-4 text-gray-400">{payment.user_email}</td>
                      <td className="py-3 pr-4 text-white capitalize">
                        {payment.report_type.replace('_', ' ')}
                      </td>
                      <td className="py-3 pr-4 text-white font-medium">₹{payment.amount}</td>
                      <td className="py-3 pr-4">
                        <span className={`px-2 py-1 rounded text-xs ${
                          payment.status === 'completed' 
                            ? 'bg-green-500/20 text-green-400' 
                            : payment.status === 'created'
                            ? 'bg-yellow-500/20 text-yellow-400'
                            : 'bg-red-500/20 text-red-400'
                        }`}>
                          {payment.status}
                        </span>
                      </td>
                      <td className="py-3 text-gray-400 text-sm">
                        {new Date(payment.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};
