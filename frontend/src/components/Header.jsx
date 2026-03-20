import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { UserAccountMenu } from './UserAccountMenu';
import { Button } from './ui/button';
import { Sparkles, LogIn, Home, Star, FileText, User } from 'lucide-react';

export const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, loading } = useAuth();

  const isActive = (path) => location.pathname === path || location.pathname.startsWith(path + '/');

  return (
    <>
      {/* ── Top header bar ── */}
      <div className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div
              className="flex items-center space-x-3 cursor-pointer"
              onClick={() => navigate(user ? '/home' : '/')}
              data-testid="header-logo"
            >
              <Sparkles className="h-8 w-8 text-gold" />
              <h1 className="text-2xl font-playfair font-semibold">Everyday Horoscope</h1>
            </div>

            <div className="flex items-center space-x-4">
              {loading ? (
                <div className="h-10 w-10 rounded-full bg-muted animate-pulse" />
              ) : user ? (
                <UserAccountMenu />
              ) : (
                <Button
                  data-testid="header-login-btn"
                  onClick={() => navigate('/login')}
                  className="bg-gold hover:bg-gold/90 text-primary-foreground"
                >
                  <LogIn className="h-4 w-4 mr-2" />
                  Sign In
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* ── Bottom mobile nav bar (logged-in users only) ── */}
      {user && (
        <div className="fixed bottom-0 left-0 right-0 z-50 sm:hidden bg-card/95 backdrop-blur-sm border-t border-border pb-safe">
          <div className="grid grid-cols-4 h-16">
            {[
              { icon: Home,     label: 'Home',     path: '/home' },
              { icon: Star,     label: 'Horoscope', path: '/horoscope/daily' },
              { icon: FileText, label: 'Reports',   path: '/my-reports' },
              { icon: User,     label: 'Account',   path: '/account' },
            ].map(({ icon: Icon, label, path }) => {
              const active = isActive(path);
              return (
                <button
                  key={path}
                  onClick={() => navigate(path)}
                  className={`flex flex-col items-center justify-center gap-1 text-xs font-medium transition-colors ${
                    active ? 'text-gold' : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Icon className={`h-5 w-5 ${active ? 'text-gold' : ''}`} />
                  <span className={active ? 'text-gold' : ''}>{label}</span>
                  {active && <span className="absolute bottom-0 w-8 h-0.5 bg-gold rounded-full" />}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </>
  );
};
