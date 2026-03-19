import React, { useState, useEffect } from 'react';

import { Footer } from '../components/Footer';
import { Shield, FileText, RefreshCw, Cookie, ScrollText, ArrowLeft, Loader } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const policyMeta = {
  terms:                { icon: ScrollText, title: 'Terms of Service' },
  privacy:              { icon: Shield,     title: 'Privacy Policy' },
  'subscription-terms': { icon: FileText,   title: 'Subscription Terms' },
  'refund-policy':      { icon: RefreshCw,  title: 'Refund & Cancellation Policy' },
  'cookie-policy':      { icon: Cookie,     title: 'Cookie Policy' },
};

export const PolicyPage = ({ type }) => {
  const navigate = useNavigate();
  const [policy, setPolicy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const meta = policyMeta[type];

  useEffect(() => {
    const fetchPolicy = async () => {
      try {
        setLoading(true);
        const res = await axios.get(`${API}/policies/${type}`);
        setPolicy(res.data);
      } catch (err) {
        setError(true);
      } finally {
        setLoading(false);
      }
    };
    if (type) fetchPolicy();
  }, [type]);

  if (!meta) return null;
  const Icon = meta.icon;

  return (
    <div className="min-h-screen bg-background flex flex-col">

      <main className="flex-1 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <Button variant="ghost" onClick={() => navigate(-1)} className="mb-6">
          <ArrowLeft className="h-4 w-4 mr-2" />Back
        </Button>

        <div className="text-center mb-10">
          <Icon className="h-12 w-12 text-gold mx-auto mb-4" />
          <h1 className="text-4xl font-playfair font-bold mb-2">
            {policy?.title || meta.title}
          </h1>
          {policy && (
            <p className="text-sm text-muted-foreground">
              Effective Date: {policy.effective_date} · Last Updated: {policy.last_updated} · {policy.company}
            </p>
          )}
        </div>

        {loading && (
          <div className="flex items-center justify-center py-20">
            <Loader className="h-8 w-8 text-gold animate-spin" />
            <span className="ml-3 text-muted-foreground">Loading policy document...</span>
          </div>
        )}

        {error && (
          <div className="p-6 rounded-xl border border-border bg-card text-center">
            <p className="text-muted-foreground">Unable to load policy document. Please try again later.</p>
            <p className="text-sm text-muted-foreground mt-2">
              For immediate assistance, email us at{' '}
              <a href="mailto:prateekmalhotra.contentcreator@gmail.com" className="text-gold hover:underline">
                prateekmalhotra.contentcreator@gmail.com
              </a>
            </p>
          </div>
        )}

        {!loading && !error && policy && (
          <div className="space-y-1">
            {policy.sections.map((section, index) => (
              <div key={index}>
                {section.heading ? (
                  <div className="mt-6 mb-2">
                    <h2 className="text-base font-bold text-foreground border-l-4 border-gold pl-3 py-1">
                      {section.heading}
                    </h2>
                    {section.content && (
                      <p className="text-sm text-muted-foreground leading-relaxed mt-2 pl-3">
                        {section.content}
                      </p>
                    )}
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground leading-relaxed py-1">
                    {section.content}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}

        <div className="mt-12 p-4 rounded-xl border border-gold/20 bg-gold/5 text-center">
          <p className="text-xs text-muted-foreground">
            For questions about this policy, contact{' '}
            <a href="mailto:prateekmalhotra.contentcreator@gmail.com" className="text-gold hover:underline">
              prateekmalhotra.contentcreator@gmail.com
            </a>
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
};
