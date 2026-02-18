import React from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
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
import { Toaster } from './components/ui/sonner';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <div className="App min-h-screen">
          <ThemeToggle />
          <Toaster position="top-center" richColors />
          <BrowserRouter>
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/auth/callback" element={<AuthCallback />} />
              
              {/* Protected Routes */}
              <Route path="/" element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              } />
              
              <Route path="/horoscope/daily" element={
                <ProtectedRoute>
                  <DailyHoroscope />
                </ProtectedRoute>
              } />
              
              <Route path="/horoscope/weekly" element={
                <ProtectedRoute>
                  <WeeklyHoroscope />
                </ProtectedRoute>
              } />
              
              <Route path="/horoscope/monthly" element={
                <ProtectedRoute>
                  <MonthlyHoroscope />
                </ProtectedRoute>
              } />
              
              <Route path="/birth-chart" element={
                <ProtectedRoute>
                  <BirthChartPage />
                </ProtectedRoute>
              } />
              
              <Route path="/kundali-milan" element={
                <ProtectedRoute>
                  <KundaliMilanPage />
                </ProtectedRoute>
              } />
              
              {/* Fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </BrowserRouter>
        </div>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
