import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { UserAccountMenu } from './UserAccountMenu';
import { Button } from './ui/button';
import { Sparkles, LogIn } from 'lucide-react';

export const Header = () => {
  const navigate = useNavigate();
  const { user, loading } = useAuth();

  return (
    <div className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div 
            className="flex items-center space-x-3 cursor-pointer" 
            onClick={() => navigate('/')}
            data-testid="header-logo"
          >
            <Sparkles className="h-8 w-8 text-gold" />
            <h1 className="text-2xl font-playfair font-semibold">Cosmic Wisdom</h1>
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
  );
};
