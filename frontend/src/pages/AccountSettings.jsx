import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

import { Footer } from '../components/Footer';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { toast } from 'sonner';
import axios from 'axios';
import {
  User,
  Lock,
  CreditCard,
  Cookie,
  ChevronRight,
  Sparkles,
  Crown,
  CheckCircle,
  XCircle,
  Eye,
  EyeOff,
  Save,
  ArrowLeft,
  Shield,
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SECTIONS = ['profile', 'security', 'payments', 'privacy'];

const ZODIAC_SIGNS = [
  { id: 'aries',       name: 'Aries',       symbol: '\u2648', dates: 'Mar 21 – Apr 19' },
  { id: 'taurus',      name: 'Taurus',      symbol: '\u2649', dates: 'Apr 20 – May 20' },
  { id: 'gemini',      name: 'Gemini',      symbol: '\u264a', dates: 'May 21 – Jun 20' },
  { id: 'cancer',      name: 'Cancer',      symbol: '\u264b', dates: 'Jun 21 – Jul 22' },
  { id: 'leo',         name: 'Leo',         symbol: '\u264c', dates: 'Jul 23 – Aug 22' },
  { id: 'virgo',       name: 'Virgo',       symbol: '\u264d', dates: 'Aug 23 – Sep 22' },
  { id: 'libra',       name: 'Libra',       symbol: '\u264e', dates: 'Sep 23 – Oct 22' },
  { id: 'scorpio',     name: 'Scorpio',     symbol: '\u264f', dates: 'Oct 23 – Nov 21' },
  { id: 'sagittarius', name: 'Sagittarius', symbol: '\u2650', dates: 'Nov 22 – Dec 21' },
  { id: 'capricorn',   name: 'Capricorn',   symbol: '\u2651', dates: 'Dec 22 – Jan 19' },
  { id: 'aquarius',    name: 'Aquarius',    symbol: '\u2652', dates: 'Jan 20 – Feb 18' },
  { id: 'pisces',      name: 'Pisces',      symbol: '\u2653', dates: 'Feb 19 – Mar 20' },
];

export const AccountSettings = () => {
  const { user, checkAuth } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [activeSection, setActiveSection] = useState(() => {
    const params = new URLSearchParams(location.search);
    const tab = params.get('tab');
    return SECTIONS.includes(tab) ? tab : 'profile';
  });

  // Profile state
  const [name, setName] = useState('');
  const [zodiacSign, setZodiacSign] = useState('');
  const [savingProfile, setSavingProfile] = useState(false);

  // Password state
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showCurrent, setShowCurrent] = useState(false);
  const [showNew, setShowNew] = useState(false);
  const [savingPassword, setSavingPassword] = useState(false);

  // Payments state
  const [payments, setPayments] = useState([]);
  const [loadingPayments, setLoadingPayments] = useState(false);

  // Cookie prefs state
  const [cookiePrefs, setCookiePrefs] = useState({
    analytics: true,
    personalization: true,
    marketing: false,
  });

  const isOAuthUser = user && !user.password_hash && user.picture;

  useEffect(() => {
    if (user) setName(user.name || '');
  }, [user]);

  useEffect(() => {
    // Load saved zodiac sign from localStorage
    const saved = localStorage.getItem('selected-sign');
    if (saved) setZodiacSign(saved);
  }, []);

  useEffect(() => {
    if (activeSection === 'payments') fetchPayments();
  }, [activeSection]);

  useEffect(() => {
    const saved = localStorage.getItem('cookie-prefs');
    if (saved) {
      try { setCookiePrefs(JSON.parse(saved)); } catch (e) {}
    }
  }, []);

  const fetchPayments = async () => {
    setLoadingPayments(true);
    try {
      const res = await axios.get(`${API}/auth/my-payments`, { withCredentials: true });
      setPayments(res.data.payments || []);
    } catch (err) {
      toast.error('Could not load payment history');
    } finally {
      setLoadingPayments(false);
    }
  };

  const handleSaveProfile = async () => {
    if (!name.trim() || name.trim().length < 2) {
      toast.error('Name must be at least 2 characters');
      return;
    }
    setSavingProfile(true);
    try {
      await axios.put(`${API}/auth/profile`, { name: name.trim() }, { withCredentials: true });
      await checkAuth();
      // Save zodiac sign to localStorage
      if (zodiacSign) {
        localStorage.setItem('selected-sign', zodiacSign);
      } else {
        localStorage.removeItem('selected-sign');
      }
      toast.success('Profile updated successfully');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to update profile');
    } finally {
      setSavingProfile(false);
    }
  };

  const handleChangePassword = async () => {
    if (!currentPassword || !newPassword || !confirmPassword) {
      toast.error('Please fill in all password fields');
      return;
    }
    if (newPassword !== confirmPassword) {
      toast.error('New passwords do not match');
      return;
    }
    if (newPassword.length < 8) {
      toast.error('New password must be at least 8 characters');
      return;
    }
    if (newPassword === currentPassword) {
      toast.error('New password must be different from current password');
      return;
    }
    setSavingPassword(true);
    try {
      await axios.put(
        `${API}/auth/change-password`,
        { current_password: currentPassword, new_password: newPassword },
        { withCredentials: true }
      );
      toast.success('Password changed successfully');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to change password');
    } finally {
      setSavingPassword(false);
    }
  };

  const handleSaveCookies = () => {
    localStorage.setItem('cookie-prefs', JSON.stringify(cookiePrefs));
    toast.success('Cookie preferences saved');
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '\u2014';
    try {
      return new Date(dateStr).toLocaleDateString('en-IN', {
        day: 'numeric', month: 'short', year: 'numeric'
      });
    } catch { return '\u2014'; }
  };

  const formatAmount = (amount) => {
    if (!amount) return '\u2014';
    return `\u20b9${Number(amount).toLocaleString('en-IN')}`;
  };

  const reportTypeLabel = (type) => {
    const map = {
      birth_chart: 'Birth Chart Analysis',
      kundali_milan: 'Kundali Milan',
      brihat_kundli: 'Brihat Kundli Pro',
      premium_monthly: 'Premium Subscription',
    };
    return map[type] || type;
  };

  const profileDirty = name.trim() !== (user?.name || '') || zodiacSign !== (localStorage.getItem('selected-sign') || '');

  const navItems = [
    { id: 'profile',  label: 'Profile',          icon: User },
    { id: 'security', label: 'Security',          icon: Lock },
    { id: 'payments', label: 'Payment History',   icon: CreditCard },
    { id: 'privacy',  label: 'Privacy & Cookies', icon: Cookie },
  ];

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Sparkles className="h-10 w-10 text-gold animate-pulse" />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10 pb-24 lg:pb-10">
        {/* Page header */}
        <div className="mb-8 flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1 text-sm"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </button>
          <div>
            <h1 className="text-3xl font-playfair font-semibold">Account Settings</h1>
            <p className="text-sm text-muted-foreground mt-1">Manage your profile, security, and preferences</p>
          </div>
        </div>

        <div className="flex flex-col md:flex-row gap-6">
          {/* Sidebar nav */}
          <aside className="w-full md:w-56 flex-shrink-0">
            <Card className="p-2 border border-border">
              {/* User pill */}
              <div className="flex items-center gap-3 px-3 py-3 mb-2 border-b border-border">
                <div className="h-9 w-9 rounded-full bg-gold flex items-center justify-center text-sm font-bold text-primary-foreground flex-shrink-0">
                  {user.name?.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)}
                </div>
                <div className="overflow-hidden">
                  <p className="text-sm font-semibold truncate">{user.name}</p>
                  <p className="text-xs text-muted-foreground truncate">{user.email}</p>
                </div>
              </div>
              {navItems.map(({ id, label, icon: Icon }) => (
                <button
                  key={id}
                  onClick={() => setActiveSection(id)}
                  className={`w-full flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                    activeSection === id
                      ? 'bg-gold/15 text-gold font-semibold'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  }`}
                >
                  <span className="flex items-center gap-2.5">
                    <Icon className="h-4 w-4" />
                    {label}
                  </span>
                  <ChevronRight className="h-3.5 w-3.5 opacity-50" />
                </button>
              ))}
            </Card>
          </aside>

          {/* Main content */}
          <div className="flex-1 min-w-0">

            {/* ── PROFILE ── */}
            {activeSection === 'profile' && (
              <Card className="p-6 border border-border">
                <div className="flex items-center gap-2 mb-6">
                  <User className="h-5 w-5 text-gold" />
                  <h2 className="text-xl font-playfair font-semibold">Profile Information</h2>
                </div>

                <div className="space-y-5">
                  {/* Avatar */}
                  <div className="flex items-center gap-4">
                    <div className="h-16 w-16 rounded-full bg-gold flex items-center justify-center text-xl font-bold text-primary-foreground">
                      {user.name?.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)}
                    </div>
                    <div>
                      <p className="text-sm font-medium">{user.name}</p>
                      <p className="text-xs text-muted-foreground">{user.email}</p>
                      {user.picture && (
                        <span className="inline-flex items-center gap-1 text-xs text-blue-500 mt-1">
                          <Shield className="h-3 w-3" /> Google account
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Name field */}
                  <div>
                    <label className="block text-sm font-medium mb-1.5">Display Name</label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                      placeholder="Your name"
                    />
                  </div>

                  {/* Email (read-only) */}
                  <div>
                    <label className="block text-sm font-medium mb-1.5">
                      Email Address
                      <span className="ml-2 text-xs text-muted-foreground font-normal">(cannot be changed)</span>
                    </label>
                    <input
                      type="email"
                      value={user.email}
                      disabled
                      className="w-full px-3 py-2.5 rounded-lg border border-border bg-muted text-sm text-muted-foreground cursor-not-allowed"
                    />
                  </div>

                  {/* Zodiac Sign */}
                  <div>
                    <label className="block text-sm font-medium mb-1.5">
                      Your Zodiac Sign
                      <span className="ml-2 text-xs text-muted-foreground font-normal">(personalises your horoscope experience)</span>
                    </label>
                    <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                      {ZODIAC_SIGNS.map((sign) => (
                        <button
                          key={sign.id}
                          type="button"
                          onClick={() => setZodiacSign(sign.id)}
                          className={`flex flex-col items-center gap-1 p-2.5 rounded-lg border text-xs transition-all ${
                            zodiacSign === sign.id
                              ? 'border-gold bg-gold/10 text-gold font-semibold'
                              : 'border-border text-muted-foreground hover:border-gold/40 hover:bg-muted/40'
                          }`}
                        >
                          <span className="text-lg leading-none">{sign.symbol}</span>
                          <span>{sign.name}</span>
                          <span className="text-xs opacity-60 hidden sm:block">{sign.dates}</span>
                        </button>
                      ))}
                    </div>
                    {zodiacSign && (
                      <button
                        type="button"
                        onClick={() => setZodiacSign('')}
                        className="mt-2 text-xs text-muted-foreground hover:text-foreground underline underline-offset-2"
                      >
                        Clear selection
                      </button>
                    )}
                  </div>

                  <Button
                    onClick={handleSaveProfile}
                    disabled={savingProfile || !profileDirty}
                    className="bg-gold hover:bg-gold/90 text-primary-foreground gap-2"
                  >
                    <Save className="h-4 w-4" />
                    {savingProfile ? 'Saving...' : 'Save Changes'}
                  </Button>
                </div>
              </Card>
            )}

            {/* ── SECURITY ── */}
            {activeSection === 'security' && (
              <Card className="p-6 border border-border">
                <div className="flex items-center gap-2 mb-6">
                  <Lock className="h-5 w-5 text-gold" />
                  <h2 className="text-xl font-playfair font-semibold">Security</h2>
                </div>

                {isOAuthUser ? (
                  <div className="flex items-start gap-3 p-4 rounded-lg bg-blue-500/10 border border-blue-500/20">
                    <Shield className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Google Sign-In Account</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        Your account is secured by Google. Password management is handled through your Google account settings.
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-5">
                    <p className="text-sm text-muted-foreground">
                      Choose a strong password you don't use elsewhere. Minimum 8 characters.
                    </p>

                    <div>
                      <label className="block text-sm font-medium mb-1.5">Current Password</label>
                      <div className="relative">
                        <input
                          type={showCurrent ? 'text' : 'password'}
                          value={currentPassword}
                          onChange={(e) => setCurrentPassword(e.target.value)}
                          className="w-full px-3 py-2.5 pr-10 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                          placeholder="Enter current password"
                        />
                        <button
                          type="button"
                          onClick={() => setShowCurrent(!showCurrent)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                        >
                          {showCurrent ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-1.5">New Password</label>
                      <div className="relative">
                        <input
                          type={showNew ? 'text' : 'password'}
                          value={newPassword}
                          onChange={(e) => setNewPassword(e.target.value)}
                          className="w-full px-3 py-2.5 pr-10 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all"
                          placeholder="Enter new password"
                        />
                        <button
                          type="button"
                          onClick={() => setShowNew(!showNew)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                        >
                          {showNew ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </button>
                      </div>
                      {newPassword && (
                        <div className="mt-1.5 flex gap-1">
                          {[1, 2, 3, 4].map((i) => (
                            <div
                              key={i}
                              className={`h-1 flex-1 rounded-full transition-all ${
                                newPassword.length >= i * 3
                                  ? i <= 1 ? 'bg-red-500' : i <= 2 ? 'bg-amber-500' : i <= 3 ? 'bg-blue-500' : 'bg-green-500'
                                  : 'bg-muted'
                              }`}
                            />
                          ))}
                        </div>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-1.5">Confirm New Password</label>
                      <input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className={`w-full px-3 py-2.5 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 focus:border-gold transition-all ${
                          confirmPassword && confirmPassword !== newPassword ? 'border-red-500' : 'border-border'
                        }`}
                        placeholder="Confirm new password"
                      />
                      {confirmPassword && confirmPassword !== newPassword && (
                        <p className="text-xs text-red-500 mt-1">Passwords do not match</p>
                      )}
                    </div>

                    <Button
                      onClick={handleChangePassword}
                      disabled={savingPassword || !currentPassword || !newPassword || !confirmPassword}
                      className="bg-gold hover:bg-gold/90 text-primary-foreground gap-2"
                    >
                      <Lock className="h-4 w-4" />
                      {savingPassword ? 'Updating...' : 'Update Password'}
                    </Button>
                  </div>
                )}
              </Card>
            )}

            {/* ── PAYMENTS ── */}
            {activeSection === 'payments' && (
              <Card className="p-6 border border-border">
                <div className="flex items-center gap-2 mb-6">
                  <CreditCard className="h-5 w-5 text-gold" />
                  <h2 className="text-xl font-playfair font-semibold">Payment History</h2>
                </div>

                {loadingPayments ? (
                  <div className="flex items-center justify-center py-12">
                    <Sparkles className="h-8 w-8 text-gold animate-pulse" />
                  </div>
                ) : payments.length === 0 ? (
                  <div className="text-center py-12">
                    <CreditCard className="h-10 w-10 text-muted-foreground mx-auto mb-3 opacity-40" />
                    <p className="text-sm text-muted-foreground">No payments yet</p>
                    <p className="text-xs text-muted-foreground mt-1">Your purchases will appear here</p>
                    <Button
                      onClick={() => navigate('/birth-chart')}
                      className="mt-4 bg-gold hover:bg-gold/90 text-primary-foreground gap-2 text-sm"
                    >
                      <Crown className="h-4 w-4" />
                      Explore Premium Reports
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {payments.map((payment, idx) => (
                      <div
                        key={payment.id || idx}
                        className="flex items-center justify-between p-4 rounded-lg border border-border hover:border-gold/30 transition-all"
                      >
                        <div className="flex items-center gap-3">
                          <div className={`h-8 w-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                            payment.status === 'completed' ? 'bg-green-500/10' : 'bg-amber-500/10'
                          }`}>
                            {payment.status === 'completed'
                              ? <CheckCircle className="h-4 w-4 text-green-500" />
                              : <XCircle className="h-4 w-4 text-amber-500" />
                            }
                          </div>
                          <div>
                            <p className="text-sm font-medium">{reportTypeLabel(payment.report_type)}</p>
                            <p className="text-xs text-muted-foreground">{formatDate(payment.created_at)}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-semibold">{formatAmount(payment.amount)}</p>
                          <span className={`text-xs px-2 py-0.5 rounded-full ${
                            payment.status === 'completed'
                              ? 'bg-green-500/10 text-green-600 dark:text-green-400'
                              : 'bg-amber-500/10 text-amber-600 dark:text-amber-400'
                          }`}>
                            {payment.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </Card>
            )}

            {/* ── PRIVACY & COOKIES ── */}
            {activeSection === 'privacy' && (
              <Card className="p-6 border border-border">
                <div className="flex items-center gap-2 mb-6">
                  <Cookie className="h-5 w-5 text-gold" />
                  <h2 className="text-xl font-playfair font-semibold">Privacy & Cookie Preferences</h2>
                </div>

                <p className="text-sm text-muted-foreground mb-6">
                  Control how we use cookies on your device. Strictly necessary cookies cannot be disabled as they are required for the platform to function.
                </p>

                <div className="space-y-4">
                  {[
                    { key: null,             label: 'Strictly Necessary',       description: 'Required for authentication, security, and core platform functionality.', alwaysOn: true },
                    { key: 'analytics',      label: 'Performance & Analytics',  description: 'Help us understand how you use the platform so we can improve it.' },
                    { key: 'personalization',label: 'Personalization',           description: 'Enable tailored astrological insights and content recommendations.' },
                    { key: 'marketing',      label: 'Marketing & Attribution',  description: 'Track referral sources and measure campaign effectiveness.' },
                  ].map(({ key, label, description, alwaysOn }) => (
                    <div key={key || 'necessary'} className="flex items-start justify-between gap-4 p-4 rounded-lg border border-border">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-medium">{label}</span>
                          {alwaysOn && (
                            <span className="text-xs bg-green-500/10 text-green-600 dark:text-green-400 px-2 py-0.5 rounded-full">Always on</span>
                          )}
                        </div>
                        <p className="text-xs text-muted-foreground">{description}</p>
                      </div>
                      <div className="flex-shrink-0 mt-0.5">
                        {alwaysOn ? (
                          <div className="w-10 h-5 bg-green-500 rounded-full opacity-60 cursor-not-allowed" />
                        ) : (
                          <button
                            onClick={() => setCookiePrefs(p => ({ ...p, [key]: !p[key] }))}
                            className={`w-10 h-5 rounded-full transition-all duration-200 relative ${
                              cookiePrefs[key] ? 'bg-gold' : 'bg-muted border border-border'
                            }`}
                          >
                            <span className={`absolute top-0.5 h-4 w-4 rounded-full bg-white shadow transition-all duration-200 ${
                              cookiePrefs[key] ? 'left-5' : 'left-0.5'
                            }`} />
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-6 flex items-center gap-3">
                  <Button onClick={handleSaveCookies} className="bg-gold hover:bg-gold/90 text-primary-foreground gap-2">
                    <Save className="h-4 w-4" />
                    Save Preferences
                  </Button>
                  <a href="/cookie-policy" className="text-sm text-muted-foreground hover:text-gold underline underline-offset-2 transition-colors">
                    Cookie Policy
                  </a>
                </div>
              </Card>
            )}

          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};
