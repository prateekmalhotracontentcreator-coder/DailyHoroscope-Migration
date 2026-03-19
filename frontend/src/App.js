import React from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import { AdminAuthProvider } from './context/AdminAuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthCallback } from './components/AuthCallback';
import { ScrollToTop } from './components/ScrollToTop';
import { NavBar } from './components/NavBar';
import { Toaster } from './components/ui/sonner';
import { CookieConsent } from './components/CookieConsent';

// Existing pages
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
import { AboutUs } from './pages/AboutUs';
import { ContactUs } from './pages/ContactUs';
import { PolicyPage } from './pages/PolicyPage';
import { ResetPassword } from './pages/ResetPassword';
import { AccountSettings } from './pages/AccountSettings';
import { AdminLogin } from './pages/admin/AdminLogin';
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { AdminBlogManager } from './pages/admin/AdminBlogManager';

// New placeholder pages
import { PanchangPage } from './pages/PanchangPage';
import { NumerologyPage } from './pages/NumerologyPage';
import { TarotPage } from './pages/TarotPage';
import { PalmistryPage } from './pages/PalmistryPage';
import { RemedyPage } from './pages/RemedyPage';
import { ComingSoonPage } from './pages/ComingSoonPage';

// Layout wrapper — NavBar is shown on all non-landing, non-auth pages
const AppLayout = ({ children }) => (
  <div className="min-h-screen flex flex-col">
    <NavBar />
    <main className="flex-1">{children}</main>
  </div>
);

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AdminAuthProvider>
          <div className="App min-h-screen">
            <Toaster position="top-center" richColors />
            <BrowserRouter>
              <ScrollToTop />
              <CookieConsent />
              <Routes>
                {/* Landing — no NavBar */}
                <Route path="/" element={<Landing />} />

                {/* Auth — no NavBar */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/auth/callback" element={<AuthCallback />} />
                <Route path="/reset-password" element={<ResetPassword />} />

                {/* Admin — no NavBar */}
                <Route path="/admin" element={<Navigate to="/admin/login" replace />} />
                <Route path="/admin/login" element={<AdminLogin />} />
                <Route path="/admin/dashboard" element={<AdminDashboard />} />
                <Route path="/admin/blog" element={<AdminBlogManager />} />

                {/* All app pages — with NavBar */}
                <Route path="/home" element={<AppLayout><ProtectedRoute><Home /></ProtectedRoute></AppLayout>} />
                <Route path="/pricing" element={<AppLayout><PricingPage /></AppLayout>} />

                {/* Horoscope */}
                <Route path="/horoscope/daily"   element={<AppLayout><DailyHoroscope /></AppLayout>} />
                <Route path="/horoscope/weekly"  element={<AppLayout><WeeklyHoroscope /></AppLayout>} />
                <Route path="/horoscope/monthly" element={<AppLayout><MonthlyHoroscope /></AppLayout>} />

                {/* Panchang */}
                <Route path="/panchang/today"      element={<AppLayout><PanchangPage type="today" /></AppLayout>} />
                <Route path="/panchang/tomorrow"   element={<AppLayout><PanchangPage type="tomorrow" /></AppLayout>} />
                <Route path="/panchang/tithi"      element={<AppLayout><PanchangPage type="tithi" /></AppLayout>} />
                <Route path="/panchang/muhurat"    element={<AppLayout><PanchangPage type="muhurat" /></AppLayout>} />
                <Route path="/panchang/nakshatra"  element={<AppLayout><PanchangPage type="nakshatra" /></AppLayout>} />
                <Route path="/panchang/choghadiya" element={<AppLayout><PanchangPage type="choghadiya" /></AppLayout>} />
                <Route path="/panchang/rahukaal"   element={<AppLayout><PanchangPage type="rahukaal" /></AppLayout>} />

                {/* Reports — protected */}
                <Route path="/birth-chart"   element={<AppLayout><ProtectedRoute><BirthChartPage /></ProtectedRoute></AppLayout>} />
                <Route path="/kundali-milan" element={<AppLayout><ProtectedRoute><KundaliMilanPage /></ProtectedRoute></AppLayout>} />
                <Route path="/brihat-kundli" element={<AppLayout><ProtectedRoute><BrihatKundliPage /></ProtectedRoute></AppLayout>} />
                <Route path="/ask-question"  element={<AppLayout><ProtectedRoute><ComingSoonPage title="Ask 1 Question" subtitle="KP Astrology — Precise answers to your life questions" eta="Coming Soon" /></ProtectedRoute></AppLayout>} />
                <Route path="/love-report"   element={<AppLayout><ProtectedRoute><ComingSoonPage title="Love & Relationship Report" subtitle="Parashari + Jaimini compatibility analysis" eta="Coming Soon" /></ProtectedRoute></AppLayout>} />
                <Route path="/career-plus"   element={<AppLayout><ProtectedRoute><ComingSoonPage title="Career Plus Intelligence" subtitle="KP precision career timing and opportunity forecast" eta="Coming Soon" /></ProtectedRoute></AppLayout>} />

                {/* New feature pages */}
                <Route path="/numerology" element={<AppLayout><NumerologyPage /></AppLayout>} />
                <Route path="/palmistry"  element={<AppLayout><PalmistryPage /></AppLayout>} />
                <Route path="/tarot"      element={<AppLayout><TarotPage /></AppLayout>} />

                {/* Remedies */}
                <Route path="/remedies/gemstones"       element={<AppLayout><RemedyPage type="gemstones" /></AppLayout>} />
                <Route path="/remedies/mantras"         element={<AppLayout><RemedyPage type="mantras" /></AppLayout>} />
                <Route path="/remedies/yantras"         element={<AppLayout><RemedyPage type="yantras" /></AppLayout>} />
                <Route path="/remedies/feng-shui"       element={<AppLayout><RemedyPage type="feng-shui" /></AppLayout>} />
                <Route path="/remedies/crystal-therapy" element={<AppLayout><RemedyPage type="crystal-therapy" /></AppLayout>} />

                {/* Blog */}
                <Route path="/blog"      element={<AppLayout><BlogList /></AppLayout>} />
                <Route path="/blog/:slug" element={<AppLayout><BlogPost /></AppLayout>} />

                {/* Company */}
                <Route path="/about"   element={<AppLayout><AboutUs /></AppLayout>} />
                <Route path="/contact" element={<AppLayout><ContactUs /></AppLayout>} />

                {/* Policy */}
                <Route path="/terms"              element={<AppLayout><PolicyPage type="terms" /></AppLayout>} />
                <Route path="/privacy"            element={<AppLayout><PolicyPage type="privacy" /></AppLayout>} />
                <Route path="/subscription-terms" element={<AppLayout><PolicyPage type="subscription-terms" /></AppLayout>} />
                <Route path="/refund-policy"      element={<AppLayout><PolicyPage type="refund-policy" /></AppLayout>} />
                <Route path="/cookie-policy"      element={<AppLayout><PolicyPage type="cookie-policy" /></AppLayout>} />

                {/* Account */}
                <Route path="/account" element={<AppLayout><ProtectedRoute><AccountSettings /></ProtectedRoute></AppLayout>} />

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
