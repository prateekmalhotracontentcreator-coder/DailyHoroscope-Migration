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

// Critical path -- loaded synchronously (first-paint routes)
import { Login } from './pages/account/Login';
import { Register } from './pages/account/Register';
import { Home } from './pages/home/Home';
import { Landing } from './pages/home/Landing';
import { DailyHoroscope } from './pages/horoscope/DailyHoroscope';
import { DailyHoroscopeSign } from './pages/horoscope/DailyHoroscopeSign';
import { WeeklyHoroscope } from './pages/horoscope/WeeklyHoroscope';
import { MonthlyHoroscope } from './pages/horoscope/MonthlyHoroscope';
import { BirthChartPage } from './pages/kundali/BirthChartPage';
import { KundaliMilanPage } from './pages/kundali/KundaliMilanPage';
import { AdminLogin } from './pages/admin/AdminLogin';
import { PanchangLangPage } from './pages/panchang/PanchangLangPage';
import PanchangLandingPage from './pages/panchang/PanchangLandingPage';

// Lazy-loaded -- split into separate chunks, loaded on demand
const BrihatKundliPage = lazy(() => import('./pages/kundali/BrihatKundliPage').then(m => ({ default: m.BrihatKundliPage })));
const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboard').then(m => ({ default: m.AdminDashboard })));
const LibraryConsolePage = lazy(() => import('./pages/admin/LibraryConsolePage').then(m => ({ default: m.LibraryConsolePage })));
const AdminBlogManager = lazy(() => import('./pages/admin/AdminBlogManager').then(m => ({ default: m.AdminBlogManager })));
const PricingPage = lazy(() => import('./pages/system/PricingPage').then(m => ({ default: m.PricingPage })));
const BlogList = lazy(() => import('./pages/content/BlogList').then(m => ({ default: m.BlogList })));
const BlogPost = lazy(() => import('./pages/content/BlogPost').then(m => ({ default: m.BlogPost })));
const AboutUs = lazy(() => import('./pages/home/AboutUs').then(m => ({ default: m.AboutUs })));
const ContactUs = lazy(() => import('./pages/content/ContactUs').then(m => ({ default: m.ContactUs })));
const PolicyPage = lazy(() => import('./pages/system/PolicyPage').then(m => ({ default: m.PolicyPage })));
const ResetPassword = lazy(() => import('./pages/account/ResetPassword').then(m => ({ default: m.ResetPassword })));
const AccountSettings = lazy(() => import('./pages/account/AccountSettings').then(m => ({ default: m.AccountSettings })));
const MyReportsPage = lazy(() => import('./pages/reports/MyReportsPage').then(m => ({ default: m.MyReportsPage })));
const IndividualReportsPage = lazy(() => import('./pages/reports/IndividualReportsPage'));
const LovePage = lazy(() => import('./pages/reports/LovePage'));
const LoveReportsPage = lazy(() => import('./pages/reports/LoveReportsPage'));
const LiveSaiBabaArtiPage = lazy(() => import('./pages/live/LiveSaiBabaArtiPage'));
const RitualEnginePage = lazy(() => import('./pages/rewards/RitualEnginePage'));
const ComingSoonPage = lazy(() => import('./pages/system/ComingSoonPage').then(m => ({ default: m.ComingSoonPage })));
const CareersPage = lazy(() => import('./pages/content/CareersPage').then(m => ({ default: m.CareersPage })));
const PanchangPage = lazy(() => import('./pages/panchang/PanchangPage').then(m => ({ default: m.PanchangPage })));
const NumerologyPage = lazy(() => import('./pages/numerology/NumerologyPage').then(m => ({ default: m.NumerologyPage })));
const NumerologyReportPage = lazy(() => import('./pages/numerology/NumerologyReportPage'));
const PalmistryPage = lazy(() => import('./pages/palmistry/PalmistryPage').then(m => ({ default: m.PalmistryPage })));
const TarotPage = lazy(() => import('./pages/tarot/TarotPage').then(m => ({ default: m.TarotPage })));
const TarotHistoryPage = lazy(() => import('./pages/tarot/TarotHistoryPage'));
const RemedyPage = lazy(() => import('./pages/remedies/RemedyPage').then(m => ({ default: m.RemedyPage })));
const KundaliPage = lazy(() => import('./pages/kundali/KundaliPage'));
const LuminaPage = lazy(() => import('./pages/lumina/LuminaPage'));
const LongevityReportPage = lazy(() => import('./pages/reports/LongevityReportPage'));
const ArcAngelPage = lazy(() => import('./pages/arc-angel/ArcAngelPage'));
const QuestionnairePage = lazy(() => import('./pages/account/QuestionnairePage'));
const LKRemediesPage       = lazy(() => import('./pages/lk/LKRemediesPage'));
const LalKitabLandingPage  = lazy(() => import('./pages/lk/LalKitabLandingPage'));
const DanaRemediesPage     = lazy(() => import('./pages/remedies/DanaRemediesPage'));
const GemstoneRemediesPage = lazy(() => import('./pages/remedies/GemstoneRemediesPage'));
const CrystalRemediesPage  = lazy(() => import('./pages/remedies/CrystalRemediesPage'));
const ChakraRemediesPage   = lazy(() => import('./pages/remedies/ChakraRemediesPage'));
const MantraRemediesPage   = lazy(() => import('./pages/remedies/MantraRemediesPage'));
const LKOnboardPage = lazy(() => import('./pages/lk/LKOnboardPage'));
const LKReportPage = lazy(() => import('./pages/lk/LKReportPage'));
const LKTrackerPage = lazy(() => import('./pages/lk/LKTrackerPage'));
const LKDebtAuditPage = lazy(() => import('./pages/lk/LKDebtAuditPage'));
const LKBrowsePage = lazy(() => import('./pages/lk/LKBrowsePage'));
const TheStrategistLandingPage = lazy(() => import('./pages/strategist/TheStrategistLandingPage'));
const StrategistPage = lazy(() => import('./pages/strategist/StrategistPage'));
const StrategistMissionsPage = lazy(() => import('./pages/strategist/StrategistMissionsPage'));
const StrategistReportPage = lazy(() => import('./pages/strategist/StrategistReportPage'));
const StrategistSurrogatePage = lazy(() => import('./pages/strategist/StrategistSurrogatePage'));
const KrishnaOraclePage = lazy(() => import('./pages/kp/KrishnaOraclePage'));
const PunyaRewardsPage = lazy(() => import('./pages/rewards/PunyaRewardsPage'));
const StrategistActionPlanPage = lazy(() => import('./pages/strategist/StrategistActionPlanPage'));
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
                  <Route path="/horoscope/daily/:sign" element={<DailyHoroscopeSign />} />
                  <Route path="/horoscope/weekly" element={<PremiumRoute feature="Weekly Horoscope" description="Full 7-day Vedic horoscope across all 12 signs is a Premium feature. Upgrade to unlock weekly predictions."><WeeklyHoroscope /></PremiumRoute>} />
                  <Route path="/horoscope/monthly" element={<PremiumRoute feature="Monthly Horoscope" description="Comprehensive monthly Vedic forecast across all 12 signs is a Premium feature. Upgrade for the full picture."><MonthlyHoroscope /></PremiumRoute>} />
                  <Route path="/live-sai-baba-arti" element={<LiveSaiBabaArtiPage />} />

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
                  <Route path="/birth-chart" element={<PremiumRoute feature="Birth Chart" description="Your Vedic birth chart analysis is a Premium feature. Upgrade to unlock your full chart with planetary positions, dashas, and yogas."><BirthChartPage /></PremiumRoute>} />
                  <Route path="/kundali-milan" element={<PremiumRoute feature="Kundali Milan" description="Kundali matching and compatibility scoring is a Premium feature. Upgrade to unlock full compatibility analysis."><KundaliMilanPage /></PremiumRoute>} />
                  <Route path="/brihat-kundli" element={<PremiumRoute feature="Brihat Kundli Pro" description="Comprehensive Vedic chart with all 16 divisional charts is a Premium feature. Upgrade to unlock the full Brihat Kundli."><BrihatKundliPage /></PremiumRoute>} />
                  <Route path="/my-reports" element={<PremiumRoute feature="My Reports" description="Your personalised Vedic reports are available to Premium members. Upgrade to access all your saved reports."><MyReportsPage /></PremiumRoute>} />
                  <Route path="/individual-reports" element={<PremiumRoute feature="Reports" description="Individual Vedic reports are a Premium feature. Upgrade to unlock your full report library."><IndividualReportsPage /></PremiumRoute>} />
                  <Route path="/reports" element={<PremiumRoute feature="Reports" description="Individual Vedic reports are a Premium feature. Upgrade to unlock your full report library."><IndividualReportsPage /></PremiumRoute>} />
                  <Route path="/love" element={<LovePage />} />
                  <Route path="/love-reports" element={<PremiumRoute feature="Love Reports" description="Your Vedic love compatibility reports are a Premium feature. Upgrade to unlock full relationship insights."><LoveReportsPage /></PremiumRoute>} />
                  <Route path="/ritual-engine" element={<PremiumRoute feature="Ritual Engine" description="Personalised Vedic ritual prescriptions are a Premium feature. Upgrade to unlock your ritual protocol."><RitualEnginePage /></PremiumRoute>} />

                  {/* Admin */}
                  <Route path="/admin" element={<Navigate to="/admin/login" replace />} />
                  <Route path="/admin/login" element={<AdminLogin />} />
                  <Route path="/admin/dashboard" element={<AdminDashboard />} />
                  <Route path="/admin/blog" element={<AdminBlogManager />} />
                  <Route path="/admin/library" element={<LibraryConsolePage />} />

                  {/* Panchang -- order matters: most specific first */}
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
                  <Route path="/numerology/report/:reportId" element={<PremiumRoute feature="Numerology Report" description="Your personalised numerology report is a Premium feature. Upgrade to unlock your full life number analysis."><NumerologyReportPage /></PremiumRoute>} />
                  <Route path="/palmistry" element={<PalmistryPage />} />
                  <Route path="/tarot" element={<TarotPage />} />
                  <Route path="/tarot/history" element={<PremiumRoute feature="Tarot History" description="Your saved tarot reading history is a Premium feature. Upgrade to review all your past readings."><TarotHistoryPage /></PremiumRoute>} />
                  <Route path="/remedies" element={<RemedyPage />} />
                  <Route path="/lagna-kundali" element={<PremiumRoute feature="Lagna Kundali" description="Your full Vedic birth chart workspace -- D1 through all divisional charts -- is a Premium feature. Upgrade to unlock."><KundaliPage /></PremiumRoute>} />
                  <Route path="/lagna-kundali/chart/:chartId" element={<PremiumRoute feature="Lagna Kundali" description="Your full Vedic birth chart workspace is a Premium feature. Upgrade to unlock."><KundaliPage /></PremiumRoute>} />

                  {/* Lumina -- Spiritual companion module */}
                  <Route path="/lumina" element={<LuminaPage />} />

                  {/* Ayur Jyotish -- Longevity & Health Report */}
                  <Route path="/longevity" element={<LongevityReportPage />} />

                  {/* Arc Angel -- 12 Areas of Life (Premium only) */}
                  <Route path="/arc-angel" element={<PremiumRoute><ArcAngelPage /></PremiumRoute>} />

                  {/* Questionnaire -- personalise readings (Premium only) */}
                  <Route path="/questionnaire" element={<PremiumRoute><QuestionnairePage /></PremiumRoute>} />

                  {/* Coming soon */}
                  <Route path="/ask-question" element={<ComingSoonPage title="Ask 1 Question" subtitle="KP Astrology-powered personalised answers" eta="Sprint 2" />} />

                  {/* Lal Kitab public SEO landing */}
                  <Route path="/lal-kitab-remedies" element={<LalKitabLandingPage />} />

                  {/* LK Standalone Remedies */}
                  <Route path="/lk-remedies"       element={<LKRemediesPage />} />
                  <Route path="/dana-remedies"     element={<DanaRemediesPage />} />
                  <Route path="/gemstone-remedies" element={<GemstoneRemediesPage />} />
                  <Route path="/crystal-therapy"   element={<CrystalRemediesPage />} />
                  <Route path="/chakra-healing"    element={<ChakraRemediesPage />} />
                  <Route path="/mantra-remedies"   element={<MantraRemediesPage />} />
                  <Route path="/lk-remedies/onboard" element={<ProtectedRoute><LKOnboardPage /></ProtectedRoute>} />
                  <Route path="/lk-remedies/report" element={<ProtectedRoute><LKReportPage /></ProtectedRoute>} />
                  <Route path="/lk-remedies/tracker" element={<ProtectedRoute><LKTrackerPage /></ProtectedRoute>} />
                  <Route path="/lk-remedies/debt-audit" element={<ProtectedRoute><LKDebtAuditPage /></ProtectedRoute>} />
                  <Route path="/lk-remedies/remedies" element={<LKBrowsePage />} />

                  {/* The Strategist */}
                  <Route path="/the-strategist" element={<TheStrategistLandingPage />} />
                  <Route path="/strategist" element={<StrategistPage />} />
                  <Route path="/strategist/missions" element={<ProtectedRoute><StrategistMissionsPage /></ProtectedRoute>} />
                  <Route path="/strategist/report" element={<ProtectedRoute><StrategistReportPage /></ProtectedRoute>} />
                  <Route path="/strategist/surrogate" element={<ProtectedRoute><StrategistSurrogatePage /></ProtectedRoute>} />
                  <Route path="/strategist/action-plan" element={<ProtectedRoute><StrategistActionPlanPage /></ProtectedRoute>} />
                  <Route path="/krishna-prashnavali" element={<KrishnaOraclePage />} />

                  {/* Punya Rewards -- loyalty & gamification (all logged-in users) */}
                  <Route path="/punya-rewards" element={<ProtectedRoute><PunyaRewardsPage /></ProtectedRoute>} />

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
