import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Sparkles, Mail, Lock, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showForgot, setShowForgot] = useState(false);
  const [forgotEmail, setForgotEmail] = useState('');
  const [forgotLoading, setForgotLoading] = useState(false);
  const [forgotSent, setForgotSent] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const from = location.state?.from?.pathname || '/';

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');
    try {
      await login(email, password);
      toast.success('Welcome back!');
      navigate(from, { replace: true });
    } catch (error) {
      const detail = error.response?.data?.detail || 'Login failed. Please try again.';
      setErrorMsg(detail);
      if (error.response?.status === 429) {
        toast.error(detail, { duration: 6000 });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;
    const redirectUrl = window.location.origin + '/auth/callback';
    const scope = 'openid email profile';
    window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${encodeURIComponent(redirectUrl)}&response_type=code&scope=${encodeURIComponent(scope)}&access_type=offline`;
  };

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    setForgotLoading(true);
    try {
      await axios.post(`${API}/auth/forgot-password`, { email: forgotEmail });
      setForgotSent(true);
      toast.success('Reset instructions sent!');
    } catch (error) {
      toast.error('Something went wrong. Please try again.');
    } finally {
      setForgotLoading(false);
    }
  };

  if (showForgot) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4 py-12">
        <Card className="w-full max-w-md p-8 border-2 border-gold/30">
          <div className="text-center mb-8">
            <Sparkles className="h-10 w-10 text-gold mx-auto mb-4" />
            <h1 className="text-3xl font-playfair font-semibold mb-2">Reset Password</h1>
            <p className="text-muted-foreground text-sm">Enter your email and we'll send you a reset link</p>
          </div>

          {forgotSent ? (
            <div className="text-center space-y-4">
              <div className="p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
                <p className="text-sm text-green-600 dark:text-green-400">
                  If an account exists for <strong>{forgotEmail}</strong>, a reset link has been sent.
                </p>
              </div>
              <p className="text-xs text-muted-foreground">Check your inbox and follow the link to reset your password.</p>
              <Button onClick={() => { setShowForgot(false); setForgotSent(false); }} variant="outline" className="w-full">
                Back to Login
              </Button>
            </div>
          ) : (
            <form onSubmit={handleForgotPassword} className="space-y-4">
              <div>
                <Label htmlFor="forgot-email">Email Address</Label>
                <div className="relative mt-1">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                  <Input
                    id="forgot-email"
                    type="email"
                    value={forgotEmail}
                    onChange={e => setForgotEmail(e.target.value)}
                    placeholder="your@email.com"
                    className="h-12 pl-10"
                    required
                  />
                </div>
              </div>
              <Button type="submit" disabled={forgotLoading} className="w-full h-12 bg-gold hover:bg-gold/90 text-primary-foreground">
                {forgotLoading ? 'Sending...' : 'Send Reset Link'}
              </Button>
              <Button type="button" variant="ghost" onClick={() => setShowForgot(false)} className="w-full">
                Back to Login
              </Button>
            </form>
          )}
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md p-8 border-2 border-gold/30">
        <div className="text-center mb-8">
          <Sparkles className="h-10 w-10 text-gold mx-auto mb-4" />
          <h1 className="text-4xl font-playfair font-semibold mb-2">Welcome Back</h1>
          <p className="text-muted-foreground">Sign in to access your cosmic insights</p>
        </div>

        {errorMsg && (
          <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start space-x-2">
            <AlertCircle className="h-4 w-4 text-red-500 mt-0.5 shrink-0" />
            <p className="text-sm text-red-600 dark:text-red-400">{errorMsg}</p>
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <Label htmlFor="email" className="text-base font-semibold mb-2 block">Email</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input id="email" type="email" data-testid="login-email" value={email} onChange={e => setEmail(e.target.value)} placeholder="your@email.com" className="h-12 text-base pl-10" required />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <Label htmlFor="password" className="text-base font-semibold">Password</Label>
              <button type="button" onClick={() => setShowForgot(true)} className="text-xs text-gold hover:underline">
                Forgot password?
              </button>
            </div>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input id="password" type="password" data-testid="login-password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Enter your password" className="h-12 text-base pl-10" required />
            </div>
          </div>

          <Button type="submit" data-testid="login-submit" disabled={loading} className="w-full h-12 text-base font-semibold bg-primary hover:bg-gold hover:text-primary-foreground">
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
        </form>

        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-border"></div></div>
          <div className="relative flex justify-center text-sm"><span className="px-4 bg-card text-muted-foreground">Or continue with</span></div>
        </div>

        <Button data-testid="google-login" onClick={handleGoogleLogin} variant="outline" className="w-full h-12 text-base font-semibold border-gold hover:bg-gold hover:text-primary-foreground">
          <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
            <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Sign in with Google
        </Button>

        <p className="mt-6 text-center text-sm text-muted-foreground">
          Don't have an account?{' '}
          <Link to="/register" className="text-gold hover:underline font-semibold">Sign up</Link>
        </p>
      </Card>
    </div>
  );
};
