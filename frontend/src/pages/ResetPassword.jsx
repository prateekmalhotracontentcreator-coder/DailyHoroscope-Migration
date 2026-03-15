import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Sparkles, Lock, CheckCircle, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const ResetPassword = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [token]);

  const handleReset = async (e) => {
    e.preventDefault();
    setError('');
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }
    setLoading(true);
    try {
      await axios.post(`${API}/auth/reset-password`, { token, new_password: password });
      setSuccess(true);
      toast.success('Password reset successfully!');
    } catch (error) {
      setError(error.response?.data?.detail || 'Reset failed. The link may have expired.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md p-8 border-2 border-gold/30">
        <div className="text-center mb-8">
          <Sparkles className="h-10 w-10 text-gold mx-auto mb-4" />
          <h1 className="text-3xl font-playfair font-semibold mb-2">Set New Password</h1>
          <p className="text-muted-foreground text-sm">Choose a strong password for your account</p>
        </div>

        {success ? (
          <div className="text-center space-y-4">
            <CheckCircle className="h-12 w-12 text-green-500 mx-auto" />
            <p className="text-green-600 dark:text-green-400 font-medium">Password reset successfully!</p>
            <Button onClick={() => navigate('/login')} className="w-full bg-gold hover:bg-gold/90 text-primary-foreground">
              Back to Login
            </Button>
          </div>
        ) : (
          <form onSubmit={handleReset} className="space-y-4">
            {error && (
              <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-start space-x-2">
                <AlertCircle className="h-4 w-4 text-red-500 mt-0.5 shrink-0" />
                <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
              </div>
            )}
            <div>
              <Label htmlFor="password">New Password</Label>
              <div className="relative mt-1">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <Input id="password" type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Minimum 6 characters" className="h-12 pl-10" required minLength={6} />
              </div>
            </div>
            <div>
              <Label htmlFor="confirm">Confirm New Password</Label>
              <div className="relative mt-1">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <Input id="confirm" type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} placeholder="Repeat your password" className="h-12 pl-10" required />
              </div>
            </div>
            <Button type="submit" disabled={loading} className="w-full h-12 bg-gold hover:bg-gold/90 text-primary-foreground font-semibold">
              {loading ? 'Resetting...' : 'Reset Password'}
            </Button>
          </form>
        )}
      </Card>
    </div>
  );
};
