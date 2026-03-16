import React from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import { AdminAuthProvider } from './context/AdminAuthContext';
import { ThemeToggle } from './components/ThemeToggle';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthCallback } from './components/AuthCallback';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Home } from './pages/Home';
import { DailyHoroscope } from './pages/DailyHoroscope';
import { WeeklyHoroscope } from './pages/WeeklyHoroscope';
import { MonthlyHoroscope } from './pages/MonthlyHoroscope';
import { BirthChartPage } from './pages/BirthChartPage';
import { KundaliMilanPage } from './pages/KundaliMilanPage';
import { BlogList } from './pages/BlogList';
import { BlogPost } from './pages/BlogPost';
import { AdminLogin } from './pages/admin/AdminLogin';
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { AdminBlogManager } from './pages/admin/AdminBlogManager';
import { AboutUs } from './pages/AboutUs';
import { ContactUs } from './pages/ContactUs';
import { PolicyPage } from './pages/PolicyPage';
import { ResetPassword } from './pages/ResetPassword';
import { AccountSettings } from './pages/AccountSettings';
import { Toaster } from './components/ui/sonner';
import { CookieConsent } from './components/CookieConsent';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AdminAuthProvider>
          <div className="App min-h-screen">
            <ThemeToggle />
            <Toaster position="top-center" richColors />
            <BrowserRouter>
              <CookieConsent />
              <Routes>
                {/* Auth Routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/auth/callback" element={<AuthCallback />} />

                {/* Public Routes */}
                <Route path="/" element={<Home />} />
                <Route path="/horoscope/daily" element={<DailyHoroscope />} />
                <Route path="/horoscope/weekly" element={<WeeklyHoroscope />} />
                <Route path="/horoscope/monthly" element={<MonthlyHoroscope />} />

                {/* Blog Routes */}
                <Route path="/blog" element={<BlogList />} />
                <Route path="/blog/:slug" element={<BlogPost />} />

                {/* Password Reset */}
                <Route path="/reset-password" element={<ResetPassword />} />

                {/* Company Pages */}
                <Route path="/about" element={<AboutUs />} />
                <Route path="/contact" element={<ContactUs />} />

                {/* Policy Pages */}
                <Route path="/terms" element={<PolicyPage type="terms" />} />
                <Route path="/privacy" element={<PolicyPage type="privacy" />} />
                <Route path="/subscription-terms" element={<PolicyPage type="subscription-terms" />} />
                <Route path="/refund-policy" element={<PolicyPage type="refund-policy" />} />
                <Route path="/cookie-policy" element={<PolicyPage type="cookie-policy" />} />

                {/* Protected Routes */}
                <Route path="/account" element={<ProtectedRoute><AccountSettings /></ProtectedRoute>} />
                <Route path="/birth-chart" element={<ProtectedRoute><BirthChartPage /></ProtectedRoute>} />
                <Route path="/kundali-milan" element={<ProtectedRoute><KundaliMilanPage /></ProtectedRoute>} />

                {/* Admin Routes */}
                <Route path="/admin" element={<Navigate to="/admin/login" replace />} />
                <Route path="/admin/login" element={<AdminLogin />} />
                <Route path="/admin/dashboard" element={<AdminDashboard />} />
                <Route path="/admin/blog" element={<AdminBlogManager />} />

                {/* Fallback */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </BrowserRouter>
          </div>
        </AdminAuthProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
