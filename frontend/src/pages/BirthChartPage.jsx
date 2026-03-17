import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Sparkles, ArrowLeft } from 'lucide-react';
import { BirthDetailsForm } from '../components/BirthDetailsForm';
import { BirthChartDisplay } from '../components/BirthChartDisplay';
import axios from 'axios';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const BirthChartPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [birthProfile, setBirthProfile] = useState(null);
  const [birthChart, setBirthChart] = useState(null);
  const [loading, setLoading] = useState({ birthChart: false });
  const [profileLoading, setProfileLoading] = useState(true);

  useEffect(() => {
    loadBirthProfile();
  }, []);

  const loadBirthProfile = async () => {
    const savedProfileId = localStorage.getItem('birth-profile-id');
    if (!savedProfileId) {
      setProfileLoading(false);
      return;
    }
    try {
      const response = await axios.get(`${API}/profile/birth/${savedProfileId}`);
      setBirthProfile(response.data);
    } catch (error) {
      // Profile not found or stale ID — clear so form is usable
      console.error('Stale birth profile ID, clearing cache:', error);
      localStorage.removeItem('birth-profile-id');
      setBirthProfile(null);
    } finally {
      setProfileLoading(false);
    }
  };

  const handleResetProfile = () => {
    localStorage.removeItem('birth-profile-id');
    setBirthProfile(null);
  };

  const handleBirthDetailsSubmit = async (formData) => {
    setLoading({ birthChart: true });
    try {
      const profileResponse = await axios.post(`${API}/profile/birth`, formData);
      localStorage.setItem('birth-profile-id', profileResponse.data.id);
      const profile = profileResponse.data;
      setBirthProfile(profile);
      localStorage.setItem('birth-profile-id', profile.id);
      
      toast.success('Birth details saved successfully!');
      
      const chartResponse = await axios.post(`${API}/birthchart/generate`, {
        profile_id: profile.id
      });
      setBirthChart(chartResponse.data);
      toast.success('Birth chart generated!');
    } catch (error) {
      console.error('Error creating birth profile:', error);
      toast.error('Failed to save birth details. Please try again.');
    } finally {
      setLoading({ birthChart: false });
    }
  };

  const handleGenerateBirthChart = async () => {
    if (!birthProfile) return;
    
    setLoading({ birthChart: true });
    try {
      const response = await axios.post(`${API}/birthchart/generate`, {
        profile_id: birthProfile.id
      });
      setBirthChart(response.data);
      toast.success('Birth chart generated!');
    } catch (error) {
      console.error('Error generating birth chart:', error);
      toast.error('Failed to generate birth chart. Please try again.');
    } finally {
      setLoading({ birthChart: false });
    }
  };

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <Button
          data-testid="back-to-home"
          onClick={() => navigate('/home')}
          variant="ghost"
          className="mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Home
        </Button>

        <h1 className="text-4xl font-playfair font-semibold mb-8 text-center">Birth Chart Analysis</h1>

        {profileLoading ? (
          <div className="flex items-center justify-center py-20">
            <Sparkles className="h-8 w-8 text-gold animate-pulse" />
          </div>
        ) : (
          <div className="space-y-6">
          {!birthProfile ? (
            <BirthDetailsForm
              onSubmit={handleBirthDetailsSubmit}
              isLoading={loading.birthChart}
            />
          ) : (
            <>
              <BirthDetailsForm
                existingProfile={birthProfile}
                isLoading={false}
              />
              {!birthChart && (
                <Button
                  data-testid="generate-birthchart"
                  onClick={handleGenerateBirthChart}
                  disabled={loading.birthChart}
                  className="w-full h-12 text-base font-semibold bg-primary hover:bg-gold hover:text-primary-foreground transition-all duration-300"
                >
                  {loading.birthChart ? 'Generating...' : 'Generate Birth Chart'}
                </Button>
              )}
              <BirthChartDisplay
                report={birthChart}
                isLoading={loading.birthChart}
                profile={birthProfile}
              />
            </>
          )}
          </div>
        )}
      </div>
    </div>
  );
};