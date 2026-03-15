import React, { useState } from 'react';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { Mail, MessageSquare, Clock, Sparkles } from 'lucide-react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';

export const ContactUs = () => {
  const [formData, setFormData] = useState({ name: '', email: '', subject: '', message: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    // Opens mailto with form data pre-filled
    const mailtoLink = `mailto:prateekmalhotra.contentcreator@gmail.com?subject=${encodeURIComponent(formData.subject || 'Contact from Everyday Horoscope')}&body=${encodeURIComponent(`Name: ${formData.name}\nEmail: ${formData.email}\n\n${formData.message}`)}`;
    window.location.href = mailtoLink;
    toast.success('Opening your email client...');
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      <main className="flex-1 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <Sparkles className="h-12 w-12 text-gold mx-auto mb-4" />
          <h1 className="text-4xl font-playfair font-bold mb-4">Contact Us</h1>
          <p className="text-xl text-muted-foreground">We'd love to hear from you</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Info */}
          <div className="space-y-6">
            <Card className="p-6">
              <div className="flex items-center space-x-3 mb-3">
                <Mail className="h-5 w-5 text-gold" />
                <h3 className="font-semibold">Email Us</h3>
              </div>
              <a href="mailto:prateekmalhotra.contentcreator@gmail.com" className="text-gold hover:underline text-sm">
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

          {/* Form */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-6">Send a Message</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label>Name</Label>
                <Input value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} placeholder="Your name" required className="mt-1" />
              </div>
              <div>
                <Label>Email</Label>
                <Input type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} placeholder="your@email.com" required className="mt-1" />
              </div>
              <div>
                <Label>Subject</Label>
                <Input value={formData.subject} onChange={e => setFormData({...formData, subject: e.target.value})} placeholder="How can we help?" className="mt-1" />
              </div>
              <div>
                <Label>Message</Label>
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
                {loading ? 'Opening...' : 'Send Message'}
              </Button>
            </form>
          </Card>
        </div>
      </main>
      <Footer />
    </div>
  );
};
