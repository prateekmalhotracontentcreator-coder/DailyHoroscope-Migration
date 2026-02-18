import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ZodiacCard } from '../components/ZodiacCard';
import axios from 'axios';
import { Sparkles } from 'lucide-react';
import { Button } from '../components/ui/button';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const Landing = () => {
  const navigate = useNavigate();
  const [signs, setSigns] = useState([]);
  const [selectedSign, setSelectedSign] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSigns();
    const savedSign = localStorage.getItem('selected-sign');
    if (savedSign) {
      setSelectedSign(savedSign);
    }
  }, []);

  const fetchSigns = async () => {
    try {
      const response = await axios.get(`${API}/signs`);
      setSigns(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching signs:', error);
      setLoading(false);
    }
  };

  const handleSignSelect = (sign) => {
    setSelectedSign(sign.id);
    localStorage.setItem('selected-sign', sign.id);
  };

  const handleContinue = () => {
    if (selectedSign) {
      navigate('/dashboard');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Sparkles className="h-16 w-16 text-gold mx-auto mb-4 animate-pulse" />
          <p className="text-xl font-playfair italic text-muted-foreground">Loading zodiac signs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-6">
            <Sparkles className="h-8 w-8 text-gold mr-3" />
            <h1 className="text-5xl md:text-7xl font-playfair font-medium tracking-tight leading-none">
              Cosmic Wisdom
            </h1>
          </div>
          <p className="text-base md:text-lg leading-relaxed text-muted-foreground max-w-2xl mx-auto">
            Discover what the stars have aligned for you. Select your zodiac sign to reveal your daily cosmic guidance.
          </p>
        </div>

        {/* Zodiac Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-12">
          {signs.map((sign) => (
            <ZodiacCard
              key={sign.id}
              sign={sign}
              onClick={handleSignSelect}
              selected={selectedSign === sign.id}
            />
          ))}
        </div>

        {/* Continue Button */}
        {selectedSign && (
          <div className="text-center animate-in fade-in duration-500">
            <Button
              data-testid="continue-button"
              onClick={handleContinue}
              size="lg"
              className="px-12 py-6 text-lg font-semibold bg-primary hover:bg-gold hover:text-primary-foreground transition-all duration-300 rounded-sm"
            >
              View My Horoscope
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};