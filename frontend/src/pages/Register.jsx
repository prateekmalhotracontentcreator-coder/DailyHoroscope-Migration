import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Sparkles, Mail, Lock, User } from 'lucide-react';
import { toast } from 'sonner';

export const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!agreedToTerms) {
      toast.error('Please accept the Terms of Service and Privacy Policy to continue.');
      return;
    }
    setLoading(true);
    try {
      await register(formData.email, formData.password, formData.name);
      toast.success('Account created successfully!');
      navigate('/', { replace: true });
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignup = () => {
    if (!agreedToTerms) {
      toast.error('Please accept the Terms of Service and Privacy Policy to continue.');
      return;
    }
    const redirectUrl = (process.env.REACT_APP_FRONTEND_URL || window.location.origin) + '/auth/callback';
    const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;
    const scope = 'openid email profile';
    window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${encodeURIComponent(redirectUrl)}&response_type=code&scope=${encodeURIComponent(scope)}&access_type=offline`;
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md p-8 border-2 border-gold/30">
        <div className="text-center mb-8">
          <Sparkles className="h-10 w-10 text-gold mx-auto mb-4" />
          <h1 className="text-4xl font-playfair font-semibold mb-2">Create Account</h1>
          <p className="text-muted-foreground">Start your astrological journey today</p>
        </div>

        <form onSubmit={handleRegister} className="space-y-6">
          <div>
            <Label htmlFor="name" className="text-base font-semibold mb-2 block">Full Name</Label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input id="name" name="name" data-testid="register-name" value={formData.name} onChange={handleChange} placeholder="Your full name" className="h-12 text-base pl-10" required />
            </div>
          </div>

          <div>
            <Label htmlFor="email" className="text-base font-semibold mb-2 block">Email</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input id="email" name="email" type="email" data-testid="register-email" value={formData.email} onChange={handleChange} placeholder="your@email.com" className="h-12 text-base pl-10" required />
            </div>
          </div>

          <div>
            <Label htmlFor="password" className="text-base font-semibold mb-2 block">Password</Label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input id="password" name="password" type="password" data-testid="register-password" value={formData.password} onChange={handleChange} placeholder="Create a password" className="h-12 text-base pl-10" required minLength={6} />
            </div>
            <p className="text-xs text-muted-foreground mt-1">Minimum 6 characters</p>
          </div>

          {/* T&C Checkbox */}
          <div className="flex items-start space-x-3 p-3 rounded-lg border border-border bg-muted/30">
            <input
              type="checkbox"
              id="terms"
              checked={agreedToTerms}
              onChange={e => setAgreedToTerms(e.target.checked)}
              className="mt-0.5 h-4 w-4 rounded border-gray-300 text-gold focus:ring-gold cursor-pointer"
            />
            <Label htmlFor="terms" className="text-sm font-normal text-muted-foreground cursor-pointer leading-relaxed">
              I have read and agree to the{' '}
              <Link to="/terms" target="_blank" className="text-gold hover:underline font-medium">Terms of Service</Link>
              {', '}
              <Link to="/privacy" target="_blank" className="text-gold hover:underline font-medium">Privacy Policy</Link>
              {', and '}
              <Link to="/subscription-terms" target="_blank" className="text-gold hover:underline font-medium">Subscription Terms</Link>.
              I understand this platform provides AI-generated astrological content for informational purposes only.
            </Label>
          </div>

          <Button
            type="submit"
            data-testid="register-submit"
            disabled={loading || !agreedToTerms}
            className="w-full h-12 text-base font-semibold bg-primary hover:bg-gold hover:text-primary-foreground disabled:opacity-50"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </Button>
        </form>

        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-border"></div></div>
          <div className="relative flex justify-center text-sm"><span className="px-4 bg-card text-muted-foreground">Or continue with</span></div>
        </div>

        <Button
          data-testid="google-signup"
          onClick={handleGoogleSignup}
          variant="outline"
          disabled={!agreedToTerms}
          className="w-full h-12 text-base font-semibold border-gold hover:bg-gold hover:text-primary-foreground disabled:opacity-50"
        >
          <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
            <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Sign up with Google
        </Button>

        <p className="mt-6 text-center text-sm text-muted-foreground">
          Already have an account?{' '}
          <Link to="/login" className="text-gold hover:underline font-semibold">Sign in</Link>
        </p>
      </Card>
    </div>
  );
};
