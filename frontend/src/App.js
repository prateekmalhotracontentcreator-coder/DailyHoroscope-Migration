import React from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import { AdminAuthProvider } from './context/AdminAuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthCallback } from './components/AuthCallback';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Home } from './pages/Home';
import { Landing } from './pages/Landing';
import { DailyHoroscope } from './pages/DailyHoroscope';
import { WeeklyHoroscope } from './pages/WeeklyHoroscope';
import { MonthlyHoroscope } from './pages/MonthlyHoroscope';
import { BirthChartPage } from './pages/BirthChartPage';
import { KundaliMilanPage } from './pages/KundaliMilanPage';
import { BrihatKundliPage } from './pages/BrihatKundliPage';
import { PricingPage } from './pages/PricingPage';
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
import { MyReportsPage } from './pages/MyReportsPage';
import { Toaster } from './components/ui/sonner';
import { CookieConsent } from './components/CookieConsent';
import { NavBar } from './components/NavBar';
import { ScrollToTop } from './components/ScrollToTop';
import { ComingSoonPage } from './pages/ComingSoonPage';
import { PanchangPage } from './pages/PanchangPage';
import { NumerologyPage } from './pages/NumerologyPage';
import { PalmistryPage } from './pages/PalmistryPage';
import { TarotPage } from './pages/TarotPage';
import { RemedyPage } from './pages/RemedyPage';
import { useKeepAlive } from './hooks/useKeepAlive';

const NavBarWrapper = () => {
  const location = useLocation();
  if (location.pathname === '/') return null;
  return <NavBar />;
};

const KeepAliveWrapper = ({ children }) => {
  useKeepAlive();
  return children;
};

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AdminAuthProvider>
          <div className="App min-h-screen">
            <Toaster position="top-center" richColors />
            <BrowserRouter>
              <KeepAliveWrapper>
                <ScrollToTop />
                <NavBarWrapper />
                <CookieConsent />
                <Routes>
                  {/* Auth */}
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/auth/callback" element={<AuthCallback />} />

                  {/* Public */}
                  <Route path="/" element={<Landing />} />
                  <Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
                  <Route path="/pricing" element={<PricingPage />} />
                  <Route path="/horoscope/daily" element={<DailyHoroscope />} />
                  <Route path="/horoscope/weekly" element={<WeeklyHoroscope />} />
                  <Route path="/horoscope/monthly" element={<MonthlyHoroscope />} />

                  {/* Blog */}
                  <Route path="/blog" element={<BlogList />} />
                  <Route path="/blog/:slug" element={<BlogPost />} />

                  {/* Auth flows */}
                  <Route path="/reset-password" element={<ResetPassword />} />

                  {/* Company */}
                  <Route path="/about" element={<AboutUs />} />
                  <Route path="/contact" element={<ContactUs />} />

                  {/* Policies */}
                  <Route path="/terms" element={<PolicyPage type="terms" />} />
                  <Route path="/privacy" element={<PolicyPage type="privacy" />} />
                  <Route path="/subscription-terms" element={<PolicyPage type="subscription-terms" />} />
                  <Route path="/refund-policy" element={<PolicyPage type="refund-policy" />} />
                  <Route path="/cookie-policy" element={<PolicyPage type="cookie-policy" />} />

                  {/* Protected */}
                  <Route path="/account" element={<ProtectedRoute><AccountSettings /></ProtectedRoute>} />
                  <Route path="/birth-chart" element={<ProtectedRoute><BirthChartPage /></ProtectedRoute>} />
                  <Route path="/kundali-milan" element={<ProtectedRoute><KundaliMilanPage /></ProtectedRoute>} />
                  <Route path="/brihat-kundli" element={<ProtectedRoute><BrihatKundliPage /></ProtectedRoute>} />
                  <Route path="/my-reports" element={<ProtectedRoute><MyReportsPage /></ProtectedRoute>} />

                  {/* Admin */}
                  <Route path="/admin" element={<Navigate to="/admin/login" replace />} />
                  <Route path="/admin/login" element={<AdminLogin />} />
                  <Route path="/admin/dashboard" element={<AdminDashboard />} />
                  <Route path="/admin/blog" element={<AdminBlogManager />} />

                  {/* Panchang — calendar route MUST come before :type to avoid conflict */}
                  <Route path="/panchang/calendar/:year/:month" element={<PanchangPage />} />
                  <Route path="/panchang/:type" element={<PanchangPage />} />

                  {/* Phase 2 modules */}
                  <Route path="/numerology" element={<NumerologyPage />} />
                  <Route path="/palmistry" element={<PalmistryPage />} />
                  <Route path="/tarot" element={<TarotPage />} />
                  <Route path="/remedies" element={<RemedyPage />} />

                  {/* Coming soon */}
                  <Route path="/ask-question" element={<ComingSoonPage title="Ask 1 Question" subtitle="KP Astrology-powered personalised answers" eta="Sprint 2" />} />
                  <Route path="/love-report" element={<ComingSoonPage title="Love Report" subtitle="Deep compatibility and relationship analysis" eta="Sprint 3" />} />
                  <Route path="/career-plus" element={<ComingSoonPage title="Career Plus" subtitle="Comprehensive career intelligence report" eta="Sprint 4" />} />

                  {/* Fallback */}
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </KeepAliveWrapper>
            </BrowserRouter>
          </div>
        </AdminAuthProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
