import React, { lazy, Suspense } from 'react';
import '@/App.css';
import './numerology.css';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import { AdminAuthProvider } from './context/AdminAuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { PremiumRoute } from './components/PremiumRoute';
import { AuthCallback } from './components/AuthCallback';
import { Toaster } from './components/ui/sonner';
import { CookieConsent } from './components/CookieConsent';
import { NavBar } from './components/NavBar';
import { ScrollToTop } from './components/ScrollToTop';

// Critical path — loaded synchronously (first-paint routes)
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Home } from './pages/Home';
import { Landing } from './pages/Landing';
import { DailyHoroscope } from './pages/DailyHoroscope';
import { WeeklyHoroscope } from './pages/WeeklyHoroscope';
import { MonthlyHoroscope } from './pages/MonthlyHoroscope';
import { BirthChartPage } from './pages/BirthChartPage';
import { KundaliMilanPage } from './pages/KundaliMilanPage';
import { AdminLogin } from './pages/admin/AdminLogin';
import { PanchangLangPage } from './pages/PanchangLangPage';
import PanchangLandingPage from './pages/PanchangLandingPage';

// Lazy-loaded — split into separate chunks, loaded on demand
const BrihatKundliPage = lazy(() => import('./pages/BrihatKundliPage').then(m => ({ default: m.BrihatKundliPage })));
const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboard').then(m => ({ default: m.AdminDashboard })));
const LibraryConsolePage = lazy(() => import('./pages/admin/LibraryConsolePage').then(m => ({ default: m.LibraryConsolePage })));
const AdminBlogManager = lazy(() => import('./pages/admin/AdminBlogManager').then(m => ({ default: m.AdminBlogManager })));
const PricingPage = lazy(() => import('./pages/PricingPage').then(m => ({ default: m.PricingPage })));
const BlogList = lazy(() => import('./pages/BlogList').then(m => ({ default: m.BlogList })));
const BlogPost = lazy(() => import('./pages/BlogPost').then(m => ({ default: m.BlogPost })));
const AboutUs = lazy(() => import('./pages/AboutUs').then(m => ({ default: m.AboutUs })));
const ContactUs = lazy(() => import('./pages/ContactUs').then(m => ({ default: m.ContactUs })));
const PolicyPage = lazy(() => import('./pages/PolicyPage').then(m => ({ default: m.PolicyPage })));
const ResetPassword = lazy(() => import('./pages/ResetPassword').then(m => ({ default: m.ResetPassword })));
const AccountSettings = lazy(() => import('./pages/AccountSettings').then(m => ({ default: m.AccountSettings })));
const MyReportsPage = lazy(() => import('./pages/MyReportsPage').then(m => ({ default: m.MyReportsPage })));
const IndividualReportsPage = lazy(() => import('./pages/IndividualReportsPage'));
const LovePage = lazy(() => import('./pages/LovePage'));
const LoveReportsPage = lazy(() => import('./pages/LoveReportsPage'));
const RitualEnginePage = lazy(() => import('./pages/RitualEnginePage'));
const ComingSoonPage = lazy(() => import('./pages/ComingSoonPage').then(m => ({ default: m.ComingSoonPage })));
const CareersPage = lazy(() => import('./pages/CareersPage').then(m => ({ default: m.CareersPage })));
const PanchangPage = lazy(() => import('./pages/PanchangPage').then(m => ({ default: m.PanchangPage })));
const NumerologyPage = lazy(() => import('./pages/NumerologyPage').then(m => ({ default: m.NumerologyPage })));
const NumerologyReportPage = lazy(() => import('./pages/NumerologyReportPage'));
const PalmistryPage = lazy(() => import('./pages/PalmistryPage').then(m => ({ default: m.PalmistryPage })));
const TarotPage = lazy(() => import('./pages/TarotPage').then(m => ({ default: m.TarotPage })));
const TarotHistoryPage = lazy(() => import('./pages/TarotHistoryPage'));
const RemedyPage = lazy(() => import('./pages/RemedyPage').then(m => ({ default: m.RemedyPage })));
const KundaliPage = lazy(() => import('./pages/KundaliPage'));
const LuminaPage = lazy(() => import('./pages/LuminaPage'));
const LongevityReportPage = lazy(() => import('./pages/LongevityReportPage'));
const ArcAngelPage = lazy(() => import('./pages/ArcAngelPage'));
const QuestionnairePage = lazy(() => import('./pages/QuestionnairePage'));
const LKRemediesPage = lazy(() => import('./pages/LKRemediesPage'));
const LKOnboardPage = lazy(() => import('./pages/LKOnboardPage'));
const LKReportPage = lazy(() => import('./pages/LKReportPage'));
const LKTrackerPage = lazy(() => import('./pages/LKTrackerPage'));
const LKDebtAuditPage = lazy(() => import('./pages/LKDebtAuditPage'));
const LKBrowsePage = lazy(() => import('./pages/LKBrowsePage'));
const StrategistPage = lazy(() => import('./pages/StrategistPage'));
const StrategistMissionsPage = lazy(() => import('./pages/StrategistMissionsPage'));
const StrategistReportPage = lazy(() => import('./pages/StrategistReportPage'));
const StrategistSurrogatePage = lazy(() => import('./pages/StrategistSurrogatePage'));
import './panchang.css';
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
                <Suspense fallback={<div />}>
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
                  <Route path="/individual-reports" element={<ProtectedRoute><IndividualReportsPage /></ProtectedRoute>} />
                  <Route path="/reports" element={<ProtectedRoute><IndividualReportsPage /></ProtectedRoute>} />
                  <Route path="/love" element={<LovePage />} />
                  <Route path="/love-reports" element={<ProtectedRoute><LoveReportsPage /></ProtectedRoute>} />
                  <Route path="/ritual-engine" element={<ProtectedRoute><RitualEnginePage /></ProtectedRoute>} />

                  {/* Admin */}
                  <Route path="/admin" element={<Navigate to="/admin/login" replace />} />
                  <Route path="/admin/login" element={<AdminLogin />} />
                  <Route path="/admin/dashboard" element={<AdminDashboard />} />
                  <Route path="/admin/blog" element={<AdminBlogManager />} />
                  <Route path="/admin/library" element={<LibraryConsolePage />} />

                  {/* Panchang — order matters: most specific first */}
                  <Route path="/panchang" element={<PanchangLandingPage />} />
                  <Route path="/panchang/calendar/:year/:month" element={<PanchangPage />} />
                  <Route path="/panchang/date/:dateValue" element={<PanchangPage />} />
                  {/* Language-specific Panchang pages + sub-views (must come before generic :type) */}
                  <Route path="/panchang/hindi/calendar/:year/:month" element={<PanchangLangPage lang="hindi" />} />
                  <Route path="/panchang/hindi/:type"      element={<PanchangLangPage lang="hindi" />} />
                  <Route path="/panchang/hindi"            element={<PanchangLangPage lang="hindi" />} />
                  <Route path="/panchang/tamil/calendar/:year/:month" element={<PanchangLangPage lang="tamil" />} />
                  <Route path="/panchang/tamil/:type"      element={<PanchangLangPage lang="tamil" />} />
                  <Route path="/panchang/tamil"            element={<PanchangLangPage lang="tamil" />} />
                  <Route path="/panchang/telugu/calendar/:year/:month" element={<PanchangLangPage lang="telugu" />} />
                  <Route path="/panchang/telugu/:type"     element={<PanchangLangPage lang="telugu" />} />
                  <Route path="/panchang/telugu"           element={<PanchangLangPage lang="telugu" />} />
                  <Route path="/panchang/malayalam/calendar/:year/:month" element={<PanchangLangPage lang="malayalam" />} />
                  <Route path="/panchang/malayalam/:type"  element={<PanchangLangPage lang="malayalam" />} />
                  <Route path="/panchang/malayalam"        element={<PanchangLangPage lang="malayalam" />} />
                  <Route path="/panchang/kannada/calendar/:year/:month" element={<PanchangLangPage lang="kannada" />} />
                  <Route path="/panchang/kannada/:type"    element={<PanchangLangPage lang="kannada" />} />
                  <Route path="/panchang/kannada"          element={<PanchangLangPage lang="kannada" />} />
                  <Route path="/panchang/:type" element={<PanchangPage />} />

                  {/* Phase 2 modules */}
                  <Route path="/numerology" element={<NumerologyPage />} />
                  <Route path="/numerology/report/:reportId" element={<ProtectedRoute><NumerologyReportPage /></ProtectedRoute>} />
                  <Route path="/palmistry" element={<PalmistryPage />} />
                  <Route path="/tarot" element={<TarotPage />} />
                  <Route path="/tarot/history" element={<ProtectedRoute><TarotHistoryPage /></ProtectedRoute>} />
                  <Route path="/remedies" element={<RemedyPage />} />
                  <Route path="/lagna-kundali" element={<ProtectedRoute><KundaliPage /></ProtectedRoute>} />
                  <Route path="/lagna-kundali/chart/:chartId" element={<ProtectedRoute><KundaliPage /></ProtectedRoute>} />

                  {/* Lumina — Spiritual companion module */}
                  <Route path="/lumina" element={<LuminaPage />} />

                  {/* Ayur Jyotish — Longevity & Health Report */}
                  <Route path="/longevity" element={<LongevityReportPage />} />

                  {/* Arc Angel — 12 Areas of Life (Premium only) */}
                  <Route path="/arc-angel" element={<PremiumRoute><ArcAngelPage /></PremiumRoute>} />

                  {/* Questionnaire — personalise readings (Premium only) */}
                  <Route path="/questionnaire" element={<PremiumRoute><QuestionnairePage /></PremiumRoute>} />

                  {/* Coming soon */}
                  <Route path="/ask-question" element={<ComingSoonPage title="Ask 1 Question" subtitle="KP Astrology-powered personalised answers" eta="Sprint 2" />} />

                  {/* LK Standalone Remedies */}
                  <Route path="/lk-remedies" element={<LKRemediesPage />} />
                  <Route path="/lk-remedies/onboard" element={<ProtectedRoute><LKOnboardPage /></ProtectedRoute>} />
                  <Route path="/lk-remedies/report" element={<ProtectedRoute><LKReportPage /></ProtectedRoute>} />
                  <Route path="/lk-remedies/tracker" element={<ProtectedRoute><LKTrackerPage /></ProtectedRoute>} />
                  <Route path="/lk-remedies/debt-audit" element={<ProtectedRoute><LKDebtAuditPage /></ProtectedRoute>} />
                  <Route path="/lk-remedies/remedies" element={<LKBrowsePage />} />

                  {/* The Strategist */}
                  <Route path="/strategist" element={<ProtectedRoute><StrategistPage /></ProtectedRoute>} />
                  <Route path="/strategist/missions" element={<ProtectedRoute><StrategistMissionsPage /></ProtectedRoute>} />
                  <Route path="/strategist/report" element={<ProtectedRoute><StrategistReportPage /></ProtectedRoute>} />
                  <Route path="/strategist/surrogate" element={<ProtectedRoute><StrategistSurrogatePage /></ProtectedRoute>} />

                  <Route path="/career-plus" element={<ComingSoonPage title="Career Plus" subtitle="Comprehensive career intelligence report" eta="Sprint 4" />} />
                  <Route path="/careers" element={<CareersPage />} />

                  {/* Fallback */}
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
                </Suspense>
              </KeepAliveWrapper>
            </BrowserRouter>
          </div>
        </AdminAuthProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
