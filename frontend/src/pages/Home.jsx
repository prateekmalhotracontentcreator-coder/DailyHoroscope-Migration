import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../components/ui/card';
import { Sparkles, Sun, Calendar, TrendingUp, Star, Heart, Crown, BookOpen } from 'lucide-react';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';

export const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      id: 'daily',
      title: 'Daily Horoscope',
      description: 'Get your personalized daily cosmic guidance',
      icon: Sun,
      color: 'text-orange-500',
      bgColor: 'bg-orange-500/10',
      path: '/horoscope/daily'
    },
    {
      id: 'weekly',
      title: 'Weekly Horoscope',
      description: 'Plan your week with astrological insights',
      icon: Calendar,
      color: 'text-blue-500',
      bgColor: 'bg-blue-500/10',
      path: '/horoscope/weekly'
    },
    {
      id: 'monthly',
      title: 'Monthly Horoscope',
      description: 'Navigate the month ahead with confidence',
      icon: TrendingUp,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
      path: '/horoscope/monthly'
    },
    {
      id: 'birthchart',
      title: 'Birth Chart Analysis',
      description: 'Comprehensive Vedic astrology report',
      icon: Star,
      color: 'text-gold',
      bgColor: 'bg-gold/10',
      path: '/birth-chart',
      premium: true
    },
    {
      id: 'kundali',
      title: 'Kundali Milan',
      description: 'Marriage compatibility analysis',
      icon: Heart,
      color: 'text-pink-500',
      bgColor: 'bg-pink-500/10',
      path: '/kundali-milan',
      premium: true
    },
    {
      id: 'brihat',
      title: 'Brihat Kundli Pro',
      description: '40+ page comprehensive Vedic life report',
      icon: Crown,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
      path: '/brihat-kundli',
      premium: true
    },
    {
      id: 'blog',
      title: 'Cosmic Blog',
      description: 'Astrology insights and zodiac guides',
      icon: BookOpen,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
      path: '/blog'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Header */}
      <Header />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-playfair font-semibold mb-4">
            Your Daily Dose of Cosmic Guidance
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Discover what the stars have aligned for you. Get free daily horoscope predictions and explore premium astrology services.
          </p>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            
            return (
              <Card
                key={feature.id}
                data-testid={`feature-card-${feature.id}`}
                className="group relative p-8 border-2 border-border hover:border-gold transition-all duration-300 cursor-pointer hover:scale-105 hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.3)]"
                onClick={() => navigate(feature.path)}
              >
                {feature.premium && (
                  <div className="absolute top-4 right-4">
                    <span className="inline-flex items-center space-x-1 bg-gold text-primary-foreground px-2 py-1 rounded-full text-xs font-semibold">
                      <Crown className="h-3 w-3" />
                      <span>PREMIUM</span>
                    </span>
                  </div>
                )}

                <div className={`${feature.bgColor} rounded-sm p-4 w-fit mb-4`}>
                  <Icon className={`h-8 w-8 ${feature.color}`} />
                </div>

                <h3 className="text-2xl font-playfair font-semibold mb-2 group-hover:text-gold transition-colors">
                  {feature.title}
                </h3>

                <p className="text-muted-foreground mb-4">
                  {feature.description}
                </p>

                <div className="flex items-center text-gold text-sm font-semibold group-hover:translate-x-2 transition-transform">
                  Explore
                  <svg className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Info Section */}
        <div className="mt-16 text-center">
          <Card className="p-8 bg-gradient-to-br from-card to-muted border-gold/30">
            <Sparkles className="h-12 w-12 text-gold mx-auto mb-4" />
            <h3 className="text-2xl font-playfair font-semibold mb-2">
              Your Astrological Journey Awaits
            </h3>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Whether you're seeking daily guidance or deep insights into your life path, 
              our AI-powered astrology platform provides authentic, personalized readings 
              based on Vedic and Western astrological principles.
            </p>
          </Card>
        </div>
      </div>
      <Footer />
    </div>
  );
};
