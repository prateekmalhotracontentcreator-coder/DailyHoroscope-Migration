import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { SEO } from '../components/SEO';
import { KundaliMilanForm } from '../components/KundaliMilanForm';
import { KundaliMilanDisplay } from '../components/KundaliMilanDisplay';
import { ArrowLeft } from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const KundaliMilanPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [kundaliMilan, setKundaliMilan] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleKundaliMilanSubmit = async (data) => {
    setLoading(true);
    try {
      const profile1Response = await axios.post(`${API}/profile/birth`, data.person1);
      const profile2Response = await axios.post(`${API}/profile/birth`, data.person2);

      const person1 = profile1Response.data;
      const person2 = profile2Response.data;

      const milanResponse = await axios.post(`${API}/kundali-milan/generate`, {
        person1_id: person1.id,
        person2_id: person2.id
      });

      setKundaliMilan({
        report: milanResponse.data,
        person1,
        person2
      });

      toast.success('Kundali Milan report generated!');
    } catch (error) {
      console.error('Error generating Kundali Milan:', error);
      toast.error('Failed to generate compatibility report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <SEO
        title="Kundali Milan — Marriage Compatibility Analysis"
        description="Check marriage compatibility with Kundali Milan. Get your Guna Milan score, Mangal Dosha analysis, and relationship compatibility report based on Vedic astrology."
        url="https://everydayhoroscope.in/kundali-milan"
      />
      <div className="max-w-5xl mx-auto">
        <Button
          data-testid="back-to-home"
          onClick={() => navigate('/')}
          variant="ghost"
          className="mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Home
        </Button>

        <h1 className="text-4xl font-playfair font-semibold mb-8 text-center">Kundali Milan</h1>
        <p className="text-center text-muted-foreground mb-8">Marriage Compatibility Analysis</p>

        <div className="space-y-6">
          {!kundaliMilan ? (
            <KundaliMilanForm
              onSubmit={handleKundaliMilanSubmit}
              isLoading={loading}
            />
          ) : (
            <>
              <KundaliMilanDisplay
                report={kundaliMilan.report}
                person1={kundaliMilan.person1}
                person2={kundaliMilan.person2}
                isLoading={loading}
              />
              <Button
                data-testid="new-kundali-milan"
                onClick={() => setKundaliMilan(null)}
                variant="outline"
                className="w-full h-12 text-base font-semibold border-gold hover:bg-gold hover:text-primary-foreground transition-all duration-300"
              >
                Check Another Compatibility
              </Button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
