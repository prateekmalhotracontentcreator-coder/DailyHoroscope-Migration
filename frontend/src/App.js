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
const PremiumReportsLanding = lazy(() => import('./pages/reports/PremiumReportsLanding'));
const KarmicDebtLandingPage = lazy(() => import('./pages/reports/landing/KarmicDebtLandingPage'));
const CareerBlueprintLandingPage = lazy(() => import('./pages/reports/landing/CareerBlueprintLandingPage'));
const ShadowSelfLandingPage = lazy(() => import('./pages/reports/landing/ShadowSelfLandingPage'));
const RetrogradeSurvivalLandingPage = lazy(() => import('./pages/reports/landing/RetrogradeSurvivalLandingPage'));
const LifeCyclesLandingPage = lazy(() => import('./pages/reports/landing/LifeCyclesLandingPage'));
const WealthBlueprintLandingPage = lazy(() => import('./pages/reports/landing/WealthBlueprintLandingPage'));
const RomanceCreativeLandingPage = lazy(() => import('./pages/reports/landing/RomanceCreativeLandingPage'));
const VitalityHealthLandingPage = lazy(() => import('./pages/reports/landing/VitalityHealthLandingPage'));
const PartnershipWindowLandingPage = lazy(() => import('./pages/reports/landing/PartnershipWindowLandingPage'));
const DharmaPurposeLandingPage = lazy(() => import('./pages/reports/landing/DharmaPurposeLandingPage'));
const GainsNetworkLandingPage = lazy(() => import('./pages/reports/landing/GainsNetworkLandingPage'));
const EncounterWindowLandingPage = lazy(() => import('./pages/reports/landing/EncounterWindowLandingPage'));
const LoveWeatherLandingPage = lazy(() => import('./pages/reports/landing/LoveWeatherLandingPage'));
const LunarCycleWellnessLandingPage = lazy(() => import('./pages/reports/landing/LunarCycleWellnessLandingPage'));
const DateNightLandingPage = lazy(() => import('./pages/reports/landing/DateNightLandingPage'));
const IntimacyVitalityLandingPage = lazy(() => import('./pages/reports/landing/IntimacyVitalityLandingPage'));
const VenusRetrogradeLandingPage = lazy(() => import('./pages/reports/landing/VenusRetrogradeLandingPage'));
const SoulmateLandingPage = lazy(() => import('./pages/reports/landing/SoulmateLandingPage'));
const SoulConnectionLandingPage = lazy(() => import('./pages/reports/landing/SoulConnectionLandingPage'));
const LovePage = lazy(() => import('./pages/reports/LovePage'));
const LoveReportsPage = lazy(() => import('./pages/reports/LoveReportsPage'));
const LiveSaiBabaArtiPage = lazy(() => import('./pages/live/LiveSaiBabaArtiPage'));
const RitualEnginePage = lazy(() => import('./pages/rewards/RitualEnginePage'));
const ComingSoonPage = lazy(() => import('./pages/system/ComingSoonPage').then(m => ({ default: m.ComingSoonPage })));
const CareersPage = lazy(() => import('./pages/content/CareersPage').then(m => ({ default: m.CareersPage })));
const PanchangPage = lazy(() => import('./pages/panchang/PanchangPage').then(m => ({ default: m.PanchangPage })));
const CityPanchangPage = lazy(() => import('./pages/panchang/CityPanchangPage').then(m => ({ default: m.CityPanchangPage })));
const ChoghadiyaPage = lazy(() => import('./pages/panchang/ChoghadiyaPage').then(m => ({ default: m.ChoghadiyaPage })));
const NumerologyPage = lazy(() => import('./pages/numerology/NumerologyPage').then(m => ({ default: m.NumerologyPage })));
const NumerologyReportPage = lazy(() => import('./pages/numerology/NumerologyReportPage'));
const PalmistryPage = lazy(() => import('./pages/palmistry/PalmistryPage').then(m => ({ default: m.PalmistryPage })));
const TarotPage = lazy(() => import('./pages/tarot/TarotPage').then(m => ({ default: m.TarotPage })));
const TarotLanding = lazy(() => import('./pages/tarot/TarotLanding'));
const TarotHistoryPage = lazy(() => import('./pages/tarot/TarotHistoryPage'));
const TarotSeoHubPage = lazy(() => import('./pages/tarot-seo/TarotSeoHubPage'));
const TarotSpreadPage = lazy(() => import('./pages/tarot-seo/TarotSpreadPage'));
const TarotCardPage = lazy(() => import('./pages/tarot-seo/TarotCardPage'));
const TarotIntentionPage = lazy(() => import('./pages/tarot-seo/TarotIntentionPage'));
const HoroscopeSignPage = lazy(() => import('./pages/horoscope/HoroscopeSignPage').then(m => ({ default: m.HoroscopeSignPage })));
const RemedyPage = lazy(() => import('./pages/remedies/RemedyPage').then(m => ({ default: m.RemedyPage })));
const KundaliPage = lazy(() => import('./pages/kundali/KundaliPage'));
const LuminaPage = lazy(() => import('./pages/lumina/LuminaPage'));
const LongevityReportPage = lazy(() => import('./pages/reports/LongevityReportPage'));
const LongevityLanding = lazy(() => import('./pages/reports/LongevityLanding'));
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
// Strategist routes temporarily un-wired for diagnostic study -- maintenance page active
const StrategistMaintenancePage = lazy(() => import('./pages/strategist/StrategistMaintenancePage'));
// eslint-disable-next-line no-unused-vars
const TheStrategistLandingPage = lazy(() => import('./pages/strategist/TheStrategistLandingPage'));
// eslint-disable-next-line no-unused-vars
const StrategistPage = lazy(() => import('./pages/strategist/StrategistPage'));
// eslint-disable-next-line no-unused-vars
const StrategistExecutivePage = lazy(() => import('./pages/strategist/StrategistExecutivePage'));
// eslint-disable-next-line no-unused-vars
const StrategistMissionsPage = lazy(() => import('./pages/strategist/StrategistMissionsPage'));
// eslint-disable-next-line no-unused-vars
const StrategistReportPage = lazy(() => import('./pages/strategist/StrategistReportPage'));
// eslint-disable-next-line no-unused-vars
const StrategistSurrogatePage = lazy(() => import('./pages/strategist/StrategistSurrogatePage'));
const KrishnaOraclePage = lazy(() => import('./pages/kp/KrishnaOraclePage'));
const AskQuestionPage = lazy(() => import('./pages/kp/AskQuestionPage'));
const PunyaRewardsPage = lazy(() => import('./pages/rewards/PunyaRewardsPage'));
const AuspiciousPage = lazy(() => import('./pages/auspicious/AuspiciousPage'));
// eslint-disable-next-line no-unused-vars
const StrategistActionPlanPage = lazy(() => import('./pages/strategist/StrategistActionPlanPage'));
const FestivalsHubPage = lazy(() => import('./pages/festivals/FestivalsHubPage').then(m => ({ default: m.FestivalsHubPage })));
const FestivalPage = lazy(() => import('./pages/festivals/FestivalPage').then(m => ({ default: m.FestivalPage })));
const IndianCalendarPage = lazy(() => import('./pages/calendar/IndianCalendarPage').then(m => ({ default: m.IndianCalendarPage })));
const HoraTodayPage = lazy(() => import('./pages/hora/HoraTodayPage').then(m => ({ default: m.HoraTodayPage })));
const RashiCalculatorPage = lazy(() => import('./pages/calculators/RashiCalculatorPage').then(m => ({ default: m.RashiCalculatorPage })));
const NakshatraCalculatorPage = lazy(() => import('./pages/calculators/NakshatraCalculatorPage').then(m => ({ default: m.NakshatraCalculatorPage })));
const NameCompatibilityPage = lazy(() => import('./pages/calculators/NameCompatibilityPage').then(m => ({ default: m.NameCompatibilityPage })));
const CompatibilityPage = lazy(() => import('./pages/kundali/CompatibilityPage').then(m => ({ default: m.CompatibilityPage })));
const LoveCalculatorPage = lazy(() => import('./pages/calculators/LoveCalculatorPage').then(m => ({ default: m.LoveCalculatorPage })));
const RemedyHubPage = lazy(() => import('./pages/remedies/RemedyHubPage').then(m => ({ default: m.RemedyHubPage })));
const DevotionalDatePage = lazy(() => import('./pages/devotional/DevotionalDatePage').then(m => ({ default: m.DevotionalDatePage })));
const MarriageMuhuratPage = lazy(() => import('./pages/muhurat/MarriageMuhuratPage').then(m => ({ default: m.MarriageMuhuratPage })));
const CelebrityHubPage = lazy(() => import('./pages/celebrity/CelebrityHubPage').then(m => ({ default: m.CelebrityHubPage })));
const CelebrityChartPage = lazy(() => import('./pages/celebrity/CelebrityChartPage').then(m => ({ default: m.CelebrityChartPage })));
const AngelNumbersHubPage = lazy(() => import('./pages/angel-numbers/AngelNumbersHubPage').then(m => ({ default: m.AngelNumbersHubPage })));
const AngelNumberPage = lazy(() => import('./pages/angel-numbers/AngelNumberPage').then(m => ({ default: m.AngelNumberPage })));
const ZibuHubPage = lazy(() => import('./pages/seo/ZibuHubPage').then(m => ({ default: m.ZibuHubPage })));
const ZibuSymbolPage = lazy(() => import('./pages/seo/ZibuSymbolPage').then(m => ({ default: m.ZibuSymbolPage })));
const FaithHubPage = lazy(() => import('./pages/faith-seo/FaithHubPage').then(m => ({ default: m.FaithHubPage })));
const FaithCollectionsHubPage = lazy(() => import('./pages/faith-seo/FaithCollectionsHubPage').then(m => ({ default: m.FaithCollectionsHubPage })));
const FaithCollectionPage = lazy(() => import('./pages/faith-seo/FaithCollectionPage').then(m => ({ default: m.FaithCollectionPage })));
const FaithGitaHubPage = lazy(() => import('./pages/faith-seo/FaithGitaHubPage').then(m => ({ default: m.FaithGitaHubPage })));
const FaithGitaRecitationPage = lazy(() => import('./pages/faith-seo/FaithGitaRecitationPage').then(m => ({ default: m.FaithGitaRecitationPage })));
const FaithGitaChapterPage = lazy(() => import('./pages/faith-seo/FaithGitaChapterPage').then(m => ({ default: m.FaithGitaChapterPage })));
const GitaVersePage = lazy(() => import('./pages/faith-seo/GitaVersePage').then(m => ({ default: m.GitaVersePage })));
const FaithBibleHubPage = lazy(() => import('./pages/faith-seo/FaithBibleHubPage').then(m => ({ default: m.FaithBibleHubPage })));
const FaithBibleTopicPage = lazy(() => import('./pages/faith-seo/FaithBibleTopicPage').then(m => ({ default: m.FaithBibleTopicPage })));
const BibleTopicPage = lazy(() => import('./pages/faith-seo/BibleTopicPage').then(m => ({ default: m.BibleTopicPage })));
const FaithTransitHubPage = lazy(() => import('./pages/faith-seo/FaithTransitHubPage').then(m => ({ default: m.FaithTransitHubPage })));
const FaithDailyHubPage = lazy(() => import('./pages/faith-seo/FaithDailyHubPage').then(m => ({ default: m.FaithDailyHubPage })));
const FaithDailySignPage = lazy(() => import('./pages/faith-seo/FaithDailySignPage').then(m => ({ default: m.FaithDailySignPage })));
const TransitScripturePage = lazy(() => import('./pages/faith-seo/TransitScripturePage').then(m => ({ default: m.TransitScripturePage })));
const DailyScripturePage = lazy(() => import('./pages/faith-seo/DailyScripturePage').then(m => ({ default: m.DailyScripturePage })));
const KundaliReportsCategoryPage = lazy(() => import('./pages/reports/category/KundaliReportsPage').then(m => ({ default: m.KundaliReportsPage })));
const NumerologyReportsCategoryPage = lazy(() => import('./pages/reports/category/NumerologyReportsPage').then(m => ({ default: m.NumerologyReportsPage })));
const LoveReportsCategoryPage = lazy(() => import('./pages/reports/category/LoveReportsPage').then(m => ({ default: m.LoveReportsPage })));
const CareerReportsCategoryPage = lazy(() => import('./pages/reports/category/CareerReportsPage').then(m => ({ default: m.CareerReportsPage })));
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
                  <Route path="/horoscope/:sign/tomorrow" element={<HoroscopeSignPage period="tomorrow" />} />
                  <Route path="/horoscope/:sign/weekly" element={<HoroscopeSignPage period="weekly" />} />
                  <Route path="/horoscope/:sign/monthly" element={<HoroscopeSignPage period="monthly" />} />
                  <Route path="/rashi-calculator" element={<RashiCalculatorPage />} />
                  <Route path="/nakshatra-calculator" element={<NakshatraCalculatorPage />} />
                  <Route path="/compatibility/name" element={<NameCompatibilityPage />} />
                  <Route path="/compatibility/:signPair" element={<CompatibilityPage />} />
                  <Route path="/love-calculator" element={<LoveCalculatorPage />} />
                  <Route path="/angel-numbers" element={<AngelNumbersHubPage />} />
                  <Route path="/angel-numbers/:number" element={<AngelNumberPage />} />
                  <Route path="/zibu" element={<ZibuHubPage />} />
                  <Route path="/zibu/:symbolSlug" element={<ZibuSymbolPage />} />
                  <Route path="/faith" element={<FaithHubPage />} />
                  <Route path="/faith/pathways" element={<FaithCollectionsHubPage />} />
                  <Route path="/faith/pathways/:collectionSlug" element={<FaithCollectionPage />} />
                  <Route path="/faith/gita" element={<FaithGitaHubPage />} />
                  <Route path="/faith/gita/recitation" element={<FaithGitaRecitationPage />} />
                  <Route path="/faith/gita/chapter/:chapter" element={<FaithGitaChapterPage />} />
                  <Route path="/faith/gita/:chapterVerse/:situationSlug" element={<GitaVersePage />} />
                  <Route path="/faith/bible" element={<FaithBibleHubPage />} />
                  <Route path="/faith/bible/topic/:topicSlug" element={<FaithBibleTopicPage />} />
                  <Route path="/faith/bible/:topicSlug/:transitionSlug" element={<BibleTopicPage />} />
                  <Route path="/faith/transit" element={<FaithTransitHubPage />} />
                  <Route path="/faith/transit/:transitSlug/:tradition" element={<TransitScripturePage />} />
                  <Route path="/faith/daily" element={<FaithDailyHubPage />} />
                  <Route path="/faith/daily/:sign/:month" element={<DailyScripturePage />} />
                  <Route path="/faith/daily/:sign" element={<FaithDailySignPage />} />
                  <Route path="/ekadashi" element={<DevotionalDatePage type="ekadashi" />} />
                  <Route path="/amavasya" element={<DevotionalDatePage type="amavasya" />} />
                  <Route path="/purnima" element={<DevotionalDatePage type="purnima" />} />
                  <Route path="/muhurat/marriage" element={<MarriageMuhuratPage />} />
                  <Route path="/celebrity-horoscopes" element={<CelebrityHubPage />} />
                  <Route path="/celebrity-horoscopes/:slug" element={<CelebrityChartPage />} />
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
                  <Route path="/premium-reports" element={<PremiumReportsLanding />} />
                  <Route path="/individual-reports" element={<PremiumReportsLanding />} />
                  <Route path="/karmic-debt-report" element={<KarmicDebtLandingPage />} />
                  <Route path="/career-blueprint-report" element={<CareerBlueprintLandingPage />} />
                  <Route path="/shadow-self-report" element={<ShadowSelfLandingPage />} />
                  <Route path="/retrograde-survival-report" element={<RetrogradeSurvivalLandingPage />} />
                  <Route path="/life-cycles-report" element={<LifeCyclesLandingPage />} />
                  <Route path="/wealth-blueprint-report" element={<WealthBlueprintLandingPage />} />
                  <Route path="/romance-creative-report" element={<RomanceCreativeLandingPage />} />
                  <Route path="/vitality-health-report" element={<VitalityHealthLandingPage />} />
                  <Route path="/partnership-window-report" element={<PartnershipWindowLandingPage />} />
                  <Route path="/dharma-purpose-report" element={<DharmaPurposeLandingPage />} />
                  <Route path="/gains-network-report" element={<GainsNetworkLandingPage />} />
                  <Route path="/encounter-window-report" element={<EncounterWindowLandingPage />} />
                  <Route path="/love-weather-report" element={<LoveWeatherLandingPage />} />
                  <Route path="/lunar-cycle-wellness" element={<LunarCycleWellnessLandingPage />} />
                  <Route path="/date-night-report" element={<DateNightLandingPage />} />
                  <Route path="/intimacy-vitality-report" element={<IntimacyVitalityLandingPage />} />
                  <Route path="/venus-retrograde-report" element={<VenusRetrogradeLandingPage />} />
                  <Route path="/soulmate-timing-report" element={<SoulmateLandingPage />} />
                  <Route path="/soul-connection-report" element={<SoulConnectionLandingPage />} />
                  <Route path="/reports/kundali" element={<KundaliReportsCategoryPage />} />
                  <Route path="/reports/numerology" element={<NumerologyReportsCategoryPage />} />
                  <Route path="/reports/love" element={<LoveReportsCategoryPage />} />
                  <Route path="/reports/career" element={<CareerReportsCategoryPage />} />
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
                  <Route path="/festivals/holi" element={<FestivalPage slug="holi" />} />
                  <Route path="/festivals/diwali" element={<FestivalPage slug="diwali" />} />
                  <Route path="/festivals/karwa-chauth" element={<FestivalPage slug="karwa-chauth" />} />
                  <Route path="/festivals" element={<FestivalsHubPage />} />
                  <Route path="/calendar" element={<IndianCalendarPage />} />
                  <Route path="/calendar/:year/:month" element={<IndianCalendarPage />} />
                  <Route path="/hora" element={<HoraTodayPage />} />
                  <Route path="/choghadiya/:citySlug/:period" element={<ChoghadiyaPage />} />
                  <Route path="/panchang" element={<PanchangLandingPage />} />
                  <Route path="/panchang/:citySlug/:date" element={<CityPanchangPage />} />
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
                  <Route path="/the-tarot" element={<TarotLanding />} />
                  <Route path="/tarot/history" element={<PremiumRoute feature="Tarot History" description="Your saved tarot reading history is a Premium feature. Upgrade to review all your past readings."><TarotHistoryPage /></PremiumRoute>} />
                  <Route path="/tarot/spreads" element={<TarotSeoHubPage />} />
                  <Route path="/tarot/spread/:spreadSlug" element={<TarotSpreadPage />} />
                  <Route path="/tarot/card/:cardSlug" element={<TarotCardPage />} />
                  <Route path="/tarot/for/:intentionSlug" element={<TarotIntentionPage />} />
                  <Route path="/remedies" element={<RemedyPage />} />
                  <Route path="/remedies/:dosha" element={<RemedyHubPage />} />
                  {/* /kundali = free public entry point for Vedic Kundali */}
                  <Route path="/kundali" element={<KundaliPage />} />
                  <Route path="/kundali/view/:chartId" element={<KundaliPage />} />
                  <Route path="/lagna-kundali" element={<PremiumRoute feature="Lagna Kundali" description="Your full Vedic birth chart workspace -- D1 through all divisional charts -- is a Premium feature. Upgrade to unlock."><KundaliPage /></PremiumRoute>} />
                  <Route path="/lagna-kundali/chart/:chartId" element={<PremiumRoute feature="Lagna Kundali" description="Your full Vedic birth chart workspace is a Premium feature. Upgrade to unlock."><KundaliPage /></PremiumRoute>} />

                  {/* Lumina -- Spiritual companion module */}
                  <Route path="/lumina" element={<LuminaPage />} />

                  {/* Ayur Jyotish -- Longevity & Health Report */}
                  <Route path="/longevity" element={<LongevityReportPage />} />
                  <Route path="/longevity-report" element={<LongevityReportPage />} />
                  <Route path="/longevity/report/:reportId" element={<ProtectedRoute><LongevityReportPage /></ProtectedRoute>} />
                  <Route path="/the-longevity-report" element={<LongevityLanding />} />

                  {/* Arc Angel -- 12 Areas of Life */}
                  <Route path="/arc-angel" element={<ProtectedRoute><ArcAngelPage /></ProtectedRoute>} />

                  {/* Questionnaire -- personalise readings */}
                  <Route path="/questionnaire" element={<ProtectedRoute><QuestionnairePage /></ProtectedRoute>} />

                  {/* Coming soon */}
                  <Route path="/ask-question" element={<AskQuestionPage />} />

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

                  {/* The Strategist -- UN-WIRED for diagnostic study 2026-05-29 */}
                  {/* All routes serve maintenance page until diagnostic is complete  */}
                  <Route path="/the-strategist" element={<StrategistMaintenancePage />} />
                  <Route path="/strategist" element={<StrategistMaintenancePage />} />
                  <Route path="/strategist/war-room" element={<ProtectedRoute><StrategistMaintenancePage /></ProtectedRoute>} />
                  <Route path="/strategist/executive" element={<ProtectedRoute><StrategistMaintenancePage /></ProtectedRoute>} />
                  <Route path="/strategist/missions" element={<ProtectedRoute><StrategistMaintenancePage /></ProtectedRoute>} />
                  <Route path="/strategist/report" element={<ProtectedRoute><StrategistMaintenancePage /></ProtectedRoute>} />
                  <Route path="/strategist/surrogate" element={<ProtectedRoute><StrategistMaintenancePage /></ProtectedRoute>} />
                  <Route path="/strategist/action-plan" element={<ProtectedRoute><StrategistMaintenancePage /></ProtectedRoute>} />
                  <Route path="/krishna-prashnavali" element={<KrishnaOraclePage />} />

                  {/* Punya Rewards -- loyalty & gamification (all logged-in users) */}
                  <Route path="/punya-rewards" element={<ProtectedRoute><PunyaRewardsPage /></ProtectedRoute>} />

                  {/* Auspicious Day Calculator -- dual-system Vedic + Chinese Tong Shu */}
                  <Route path="/auspicious-calculator" element={<AuspiciousPage />} />

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
