import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Button } from './ui/button';
import { Crown, User, LogOut, CreditCard, Check, X } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const UserAccountMenu = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      checkSubscription();
    }
  }, [user]);

  const checkSubscription = async () => {
    try {
      // Check if user has active subscription
      const response = await axios.get(`${API}/premium/check`, {
        params: {
          user_email: user.email,
          report_type: 'premium_monthly',
          report_id: 'subscription'
        }
      });
      
      if (response.data.has_premium_access) {
        setSubscription({
          active: true,
          type: 'Premium Monthly',
          amount: '₹1,599/month'
        });
      }
    } catch (error) {
      console.error('Error checking subscription:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      toast.success('Logged out successfully');
      navigate('/login');
    } catch (error) {
      toast.error('Logout failed');
    }
  };

  if (!user) return null;

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const isPremium = subscription?.active;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          className="relative h-12 w-12 rounded-full border-2 border-gold/50 hover:border-gold transition-colors"
          data-testid="user-account-menu"
        >
          <Avatar className="h-10 w-10">
            <AvatarImage src={user.picture} alt={user.name} />
            <AvatarFallback className="bg-gold text-primary-foreground font-semibold">
              {getInitials(user.name)}
            </AvatarFallback>
          </Avatar>
          {isPremium && (
            <div className="absolute -top-1 -right-1 bg-gold rounded-full p-1">
              <Crown className="h-3 w-3 text-primary-foreground" />
            </div>
          )}
        </Button>
      </DropdownMenuTrigger>
      
      <DropdownMenuContent className="w-80" align="end" forceMount>
        {/* User Info */}
        <DropdownMenuLabel className="font-normal">
          <div className="flex items-start space-x-3 py-2">
            <Avatar className="h-14 w-14">
              <AvatarImage src={user.picture} alt={user.name} />
              <AvatarFallback className="bg-gold text-primary-foreground font-semibold text-lg">
                {getInitials(user.name)}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 space-y-1">
              <p className="text-base font-semibold leading-none">{user.name}</p>
              <p className="text-xs text-muted-foreground">{user.email}</p>
              {isPremium && (
                <div className="inline-flex items-center space-x-1 bg-gold/20 text-gold px-2 py-1 rounded-full text-xs font-semibold mt-2">
                  <Crown className="h-3 w-3" />
                  <span>Premium Member</span>
                </div>
              )}
            </div>
          </div>
        </DropdownMenuLabel>
        
        <DropdownMenuSeparator />
        
        {/* Plan Details */}
        <div className="px-2 py-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-semibold">Current Plan</span>
            {isPremium ? (
              <span className="text-xs bg-gold text-primary-foreground px-2 py-1 rounded-full font-semibold">
                {subscription.type}
              </span>
            ) : (
              <span className="text-xs bg-muted text-muted-foreground px-2 py-1 rounded-full font-semibold">
                Free
              </span>
            )}
          </div>
          
          {isPremium ? (
            <div className="space-y-2 text-xs">
              <div className="flex items-center text-green-600 dark:text-green-400">
                <Check className="h-4 w-4 mr-2" />
                <span>Unlimited Birth Charts</span>
              </div>
              <div className="flex items-center text-green-600 dark:text-green-400">
                <Check className="h-4 w-4 mr-2" />
                <span>Unlimited Kundali Milan</span>
              </div>
              <div className="flex items-center text-green-600 dark:text-green-400">
                <Check className="h-4 w-4 mr-2" />
                <span>PDF Downloads</span>
              </div>
              <div className="flex items-center text-green-600 dark:text-green-400">
                <Check className="h-4 w-4 mr-2" />
                <span>Social Sharing</span>
              </div>
              <div className="pt-2 border-t border-border">
                <p className="text-muted-foreground">
                  Billed {subscription.amount}
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-2 text-xs">
              <div className="flex items-center text-green-600 dark:text-green-400">
                <Check className="h-4 w-4 mr-2" />
                <span>Daily/Weekly/Monthly Horoscopes</span>
              </div>
              <div className="flex items-center text-green-600 dark:text-green-400">
                <Check className="h-4 w-4 mr-2" />
                <span>Basic Birth Chart Preview</span>
              </div>
              <div className="flex items-center text-muted-foreground">
                <X className="h-4 w-4 mr-2" />
                <span>Full Birth Chart Analysis</span>
              </div>
              <div className="flex items-center text-muted-foreground">
                <X className="h-4 w-4 mr-2" />
                <span>Kundali Milan Analysis</span>
              </div>
              <div className="flex items-center text-muted-foreground">
                <X className="h-4 w-4 mr-2" />
                <span>PDF Downloads</span>
              </div>
            </div>
          )}
        </div>
        
        <DropdownMenuSeparator />
        
        {/* Actions */}
        {!isPremium && (
          <>
            <DropdownMenuItem
              className="cursor-pointer text-gold hover:text-gold hover:bg-gold/10"
              onClick={() => {
                navigate('/home');
              }}
            >
              <Crown className="mr-2 h-4 w-4" />
              <span className="font-semibold">Upgrade to Premium</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
          </>
        )}
        
        <DropdownMenuItem className="cursor-pointer" onClick={() => navigate('/account')}>
          <User className="mr-2 h-4 w-4" />
          <span>Account Settings</span>
        </DropdownMenuItem>
        
        <DropdownMenuItem className="cursor-pointer" onClick={() => navigate('/account?tab=payments')}>
          <CreditCard className="mr-2 h-4 w-4" />
          <span>Payment History</span>
        </DropdownMenuItem>
        
        <DropdownMenuSeparator />
        
        <DropdownMenuItem
          className="cursor-pointer text-red-600 dark:text-red-400 focus:text-red-600 dark:focus:text-red-400"
          onClick={handleLogout}
          data-testid="logout-menu-item"
        >
          <LogOut className="mr-2 h-4 w-4" />
          <span>Log out</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};