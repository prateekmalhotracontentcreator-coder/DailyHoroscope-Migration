import React, { useState } from 'react';
import { Header } from '../components/Header';
import { SEO } from '../components/SEO';
import { Footer } from '../components/Footer';
import { Mail, MessageSquare, Clock, Sparkles, CheckCircle } from 'lucide-react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const ContactUs = () => {
  const [formData, setFormData] = useState({ name: '', email: '', subject: '', message: '' });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`${API}/contact`, formData);
      setSubmitted(true);
      toast.success('Message sent successfully!');
    } catch (error) {
      toast.error('Failed to send message. Please try again or email us directly.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title="Contact Us — Everyday Horoscope"
        description="Get in touch with the Everyday Horoscope team. We're here to help with questions about your horoscope, reports, subscriptions, or anything else."
        url="https://everydayhoroscope.in/contact"
      />
      <Header />

      <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <Sparkles className="h-10 w-10 text-gold mx-auto mb-4" />
          <h1 className="text-4xl font-playfair font-bold mb-4">Contact Us</h1>
          <p className="text-xl text-muted-foreground">We'd love to hear from you</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Form first on mobile */}
          <Card className="p-6 md:order-2">
            {submitted ? (
              <div className="flex flex-col items-center justify-center h-full py-8 text-center space-y-4">
                <CheckCircle className="h-14 w-14 text-green-500" />
                <h3 className="text-xl font-semibold">Message Sent!</h3>
                <p className="text-muted-foreground text-sm">Thank you for reaching out. We'll get back to you within 2 business days.</p>
                <Button variant="outline" onClick={() => { setSubmitted(false); setFormData({ name: '', email: '', subject: '', message: '' }); }}>
                  Send Another Message
                </Button>
              </div>
            ) : (
              <>
                <h3 className="text-lg font-semibold mb-6">Send a Message</h3>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <Label>Name *</Label>
                    <Input value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} placeholder="Your name" required className="mt-1" />
                  </div>
                  <div>
                    <Label>Email *</Label>
                    <Input type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} placeholder="your@email.com" required className="mt-1" />
                  </div>
                  <div>
                    <Label>Subject</Label>
                    <Input value={formData.subject} onChange={e => setFormData({...formData, subject: e.target.value})} placeholder="How can we help?" className="mt-1" />
                  </div>
                  <div>
                    <Label>Message *</Label>
                    <textarea
                      value={formData.message}
                      onChange={e => setFormData({...formData, message: e.target.value})}
                      placeholder="Tell us more..."
                      required
                      className="w-full h-28 mt-1 px-3 py-2 bg-background border border-border rounded-md text-sm resize-none focus:outline-none focus:ring-1 focus:ring-gold"
                    />
                  </div>
                  <Button type="submit" disabled={loading} className="w-full bg-gold hover:bg-gold/90 text-primary-foreground">
                    <Mail className="h-4 w-4 mr-2" />
                    {loading ? 'Sending...' : 'Send Message'}
                  </Button>
                </form>
              </>
            )}
          </Card>

          {/* Info cards second on mobile, first on desktop */}
          <div className="space-y-6 md:order-1">
            <Card className="p-6">
              <div className="flex items-center space-x-3 mb-3">
                <Mail className="h-5 w-5 text-gold" />
                <h3 className="font-semibold">Email Us Directly</h3>
              </div>
              <a href="mailto:prateekmalhotra.contentcreator@gmail.com" className="text-gold hover:underline text-sm break-all">
                prateekmalhotra.contentcreator@gmail.com
              </a>
            </Card>
            <Card className="p-6">
              <div className="flex items-center space-x-3 mb-3">
                <Clock className="h-5 w-5 text-gold" />
                <h3 className="font-semibold">Response Time</h3>
              </div>
              <p className="text-sm text-muted-foreground">We typically respond within 2 business days.</p>
            </Card>
            <Card className="p-6">
              <div className="flex items-center space-x-3 mb-3">
                <MessageSquare className="h-5 w-5 text-gold" />
                <h3 className="font-semibold">What to include</h3>
              </div>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Your registered email address</li>
                <li>• Description of your query or issue</li>
                <li>• Order/payment ID (for billing queries)</li>
              </ul>
            </Card>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};
