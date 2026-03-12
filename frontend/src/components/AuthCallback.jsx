import React, { useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { Sparkles } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const AuthCallback = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { checkAuth } = useAuth();
  const hasProcessed = useRef(false);

  useEffect(() => {
    if (hasProcessed.current) return;
    hasProcessed.current = true;

    const processAuth = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get('code');

      if (!code) {
        navigate('/login');
        return;
      }

      try {
        // Send code in request BODY to avoid URL encoding issues with '/' in code
        const response = await axios.post(
          `${API}/auth/oauth/callback`,
          { session_id: code },
          { withCredentials: true }
        );

        await checkAuth();
        navigate('/', { state: { user: response.data }, replace: true });
      } catch (error) {
        console.error('OAuth error:', error);
        navigate('/login', { state: { error: 'Authentication failed' } });
      }
    };

    processAuth();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <Sparkles className="h-16 w-16 text-gold mx-auto mb-4 animate-pulse" />
        <p className="text-xl font-playfair italic text-muted-foreground">Completing authentication...</p>
      </div>
    </div>
  );
};
