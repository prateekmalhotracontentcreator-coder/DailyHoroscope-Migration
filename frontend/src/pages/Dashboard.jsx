import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { HoroscopeCard } from '../components/HoroscopeCard';
import { BirthDetailsForm } from '../components/BirthDetailsForm';
import { BirthChartDisplay } from '../components/BirthChartDisplay';
import { KundaliMilanForm } from '../components/KundaliMilanForm';
import { KundaliMilanDisplay } from '../components/KundaliMilanDisplay';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Button } from '../components/ui/button';
import axios from 'axios';
import { ArrowLeft, Sparkles } from 'lucide-react';
import { toast } from 'sonner';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const Dashboard = () => {
  const navigate = useNavigate();
  const [selectedSign, setSelectedSign] = useState(null);
  const [signs, setSigns] = useState([]);
  const [horoscopes, setHoroscopes] = useState({
    daily: null,
    weekly: null,
    monthly: null
  });
  const [loading, setLoading] = useState({
    daily: false,
    weekly: false,
    monthly: false,
    birthChart: false,
    kundaliMilan: false
  });
  const [activeTab, setActiveTab] = useState('daily');
  const [birthProfile, setBirthProfile] = useState(null);
  const [birthChart, setBirthChart] = useState(null);
  const [kundaliMilan, setKundaliMilan] = useState(null);
  const [savedProfiles, setSavedProfiles] = useState([]);

  useEffect(() => {
    const savedSign = localStorage.getItem('selected-sign');
    if (!savedSign) {
      navigate('/');
      return;
    }
    setSelectedSign(savedSign);
    fetchSigns();
    fetchHoroscope(savedSign, 'daily');
    loadBirthProfile();
  }, [navigate]);

  const fetchSigns = async () => {
    try {
      const response = await axios.get(`${API}/signs`);
      setSigns(response.data);
    } catch (error) {
      console.error('Error fetching signs:', error);
    }
  };

  const fetchHoroscope = async (sign, type) => {
    if (horoscopes[type]) return; // Already loaded

    setLoading((prev) => ({ ...prev, [type]: true }));
    try {
      const response = await axios.get(`${API}/horoscope/${sign}/${type}`);
      setHoroscopes((prev) => ({ ...prev, [type]: response.data }));
    } catch (error) {
      console.error(`Error fetching ${type} horoscope:`, error);
    } finally {
      setLoading((prev) => ({ ...prev, [type]: false }));
    }
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    if (!horoscopes[tab] && selectedSign) {
      fetchHoroscope(selectedSign, tab);
    }
  };

  const currentSignData = signs.find((s) => s.id === selectedSign);

  if (!selectedSign) {
    return null;
  }

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Button
            data-testid="back-button"
            onClick={() => navigate('/')}
            variant="ghost"
            className="mb-6 hover:bg-muted transition-colors"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Change Sign
          </Button>

          {currentSignData && (
            <div className="flex items-center space-x-6 p-8 rounded-sm border border-border bg-card">
              <span className="text-8xl font-playfair leading-none">
                {currentSignData.symbol}
              </span>
              <div className="flex-1">
                <h1 className="text-4xl md:text-5xl font-playfair font-semibold tracking-tight mb-2">
                  {currentSignData.name}
                </h1>
                <p className="text-sm text-muted-foreground uppercase tracking-[0.2em] font-semibold mb-1">
                  {currentSignData.dates}
                </p>
                <p className="text-sm text-gold uppercase tracking-wider flex items-center">
                  <Sparkles className="h-4 w-4 mr-2" />
                  {currentSignData.element} Element
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Horoscope Tabs */}
        <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-8 bg-muted p-1 rounded-sm h-auto">
            <TabsTrigger
              data-testid="tab-daily"
              value="daily"
              className="py-3 text-base font-semibold data-[state=active]:bg-card data-[state=active]:text-foreground data-[state=active]:shadow-sm rounded-sm transition-all"
            >
              Daily
            </TabsTrigger>
            <TabsTrigger
              data-testid="tab-weekly"
              value="weekly"
              className="py-3 text-base font-semibold data-[state=active]:bg-card data-[state=active]:text-foreground data-[state=active]:shadow-sm rounded-sm transition-all"
            >
              Weekly
            </TabsTrigger>
            <TabsTrigger
              data-testid="tab-monthly"
              value="monthly"
              className="py-3 text-base font-semibold data-[state=active]:bg-card data-[state=active]:text-foreground data-[state=active]:shadow-sm rounded-sm transition-all"
            >
              Monthly
            </TabsTrigger>
          </TabsList>

          <TabsContent value="daily" data-testid="content-daily">
            <HoroscopeCard
              title="Daily Horoscope"
              content={horoscopes.daily?.content}
              isLoading={loading.daily}
              type="daily"
            />
          </TabsContent>

          <TabsContent value="weekly" data-testid="content-weekly">
            <HoroscopeCard
              title="Weekly Horoscope"
              content={horoscopes.weekly?.content}
              isLoading={loading.weekly}
              type="weekly"
            />
          </TabsContent>

          <TabsContent value="monthly" data-testid="content-monthly">
            <HoroscopeCard
              title="Monthly Horoscope"
              content={horoscopes.monthly?.content}
              isLoading={loading.monthly}
              type="monthly"
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};