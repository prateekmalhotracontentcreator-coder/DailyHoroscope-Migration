import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Crown, Check, Sparkles } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const PaymentModal = ({ isOpen, onClose, reportType, reportId, onSuccess }) => {
  const [email, setEmail] = useState('');
  const [paymentOption, setPaymentOption] = useState('per_report');
  const [processing, setProcessing] = useState(false);

  const pricing = {
    birth_chart: { price: 9.99, title: 'Birth Chart Report' },
    kundali_milan: { price: 14.99, title: 'Kundali Milan Report' },
    premium_monthly: { price: 19.99, title: 'Premium Monthly Subscription' }
  };

  const currentPrice = paymentOption === 'premium_monthly' 
    ? pricing.premium_monthly.price 
    : pricing[reportType]?.price || 9.99;

  const handlePayment = async () => {
    if (!email) {
      toast.error('Please enter your email');
      return;
    }

    setProcessing(true);
    
    try {
      // Create payment intent
      const intentResponse = await axios.post(`${API}/payment/create-intent`, {
        report_type: paymentOption === 'premium_monthly' ? 'premium_monthly' : reportType,
        report_id: reportId,
        user_email: email
      });

      // In real implementation, you'd use Stripe Elements here
      // For demo, we'll simulate successful payment
      const paymentIntentId = 'pi_test_' + Date.now();
      
      // Confirm payment
      await axios.post(`${API}/payment/confirm`, null, {
        params: {
          payment_intent_id: paymentIntentId,
          user_email: email,
          report_type: paymentOption === 'premium_monthly' ? 'premium_monthly' : reportType,
          report_id: reportId
        }
      });

      toast.success('Payment successful! You now have premium access.');
      localStorage.setItem('user_email', email);
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Payment error:', error);
      toast.error('Payment failed. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <div className="flex items-center space-x-2 mb-2">
            <Crown className="h-6 w-6 text-gold" />
            <DialogTitle className="text-2xl font-playfair">Unlock Premium Access</DialogTitle>
          </div>
          <DialogDescription>
            Get full detailed analysis with comprehensive insights
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          <div>
            <Label htmlFor="email" className="text-base font-semibold mb-2 block">
              Email Address
            </Label>
            <Input
              id="email"
              type="email"
              data-testid="payment-email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="h-12 text-base"
            />
          </div>

          <div>
            <Label className="text-base font-semibold mb-3 block">Choose Payment Option</Label>
            <RadioGroup value={paymentOption} onValueChange={setPaymentOption}>
              <div className="flex items-center space-x-3 p-4 border border-border rounded-sm hover:border-gold transition-colors cursor-pointer">
                <RadioGroupItem value="per_report" id="per_report" />
                <Label htmlFor="per_report" className="flex-1 cursor-pointer">
                  <div className="font-semibold">This Report Only</div>
                  <div className="text-sm text-muted-foreground">
                    ${pricing[reportType]?.price} one-time
                  </div>
                </Label>
              </div>

              <div className="flex items-center space-x-3 p-4 border-2 border-gold rounded-sm bg-gold/5 cursor-pointer relative">
                <RadioGroupItem value="premium_monthly" id="premium_monthly" />
                <Label htmlFor="premium_monthly" className="flex-1 cursor-pointer">
                  <div className="flex items-center space-x-2">
                    <span className="font-semibold">Premium Monthly</span>
                    <span className="text-xs bg-gold text-primary-foreground px-2 py-0.5 rounded-full font-semibold">BEST VALUE</span>
                  </div>
                  <div className="text-sm text-muted-foreground mb-2">
                    $19.99/month - Unlimited reports
                  </div>
                  <div className="flex items-start space-x-2 text-xs text-foreground/80">
                    <Check className="h-3 w-3 text-gold mt-0.5 flex-shrink-0" />
                    <span>Unlimited Birth Charts & Kundali Milan</span>
                  </div>
                  <div className="flex items-start space-x-2 text-xs text-foreground/80">
                    <Check className="h-3 w-3 text-gold mt-0.5 flex-shrink-0" />
                    <span>PDF downloads & sharing</span>
                  </div>
                </Label>
              </div>
            </RadioGroup>
          </div>

          <div className="bg-muted p-4 rounded-sm">
            <div className="flex justify-between items-center mb-2">
              <span className="font-semibold">Total:</span>
              <span className="text-2xl font-playfair font-bold text-gold">${currentPrice}</span>
            </div>
            {paymentOption === 'premium_monthly' && (
              <p className="text-xs text-muted-foreground">Cancel anytime. No hidden fees.</p>
            )}
          </div>

          <Button
            data-testid="complete-payment"
            onClick={handlePayment}
            disabled={processing}
            className="w-full h-12 text-base font-semibold bg-gold hover:bg-gold-hover text-primary-foreground"
          >
            {processing ? (
              <span className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5 animate-pulse" />
                <span>Processing...</span>
              </span>
            ) : (
              `Complete Payment - $${currentPrice}`
            )}
          </Button>

          <p className="text-xs text-center text-muted-foreground">
            Secure payment powered by Stripe • 30-day money-back guarantee
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
};