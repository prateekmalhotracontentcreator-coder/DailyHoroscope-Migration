import React from 'react';
import { Header } from '../components/Header';
import { SEO } from '../components/SEO';
import { Footer } from '../components/Footer';
import { Sparkles, Star, Heart, Shield } from 'lucide-react';

export const AboutUs = () => {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title="About Us — SkyHound Studios"
        description="Learn about Everyday Horoscope and SkyHound Studios — the team bringing ancient Vedic astrology insights to seekers worldwide."
        url="https://everydayhoroscope.in/about"
      />
      <Header />

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <Sparkles className="h-10 w-10 text-gold mx-auto mb-4" />
          <h1 className="text-4xl font-playfair font-bold mb-4">About Everyday Horoscope</h1>
          <p className="text-xl text-muted-foreground">Bridging ancient wisdom with modern precision</p>
        </div>

        <div className="space-y-6">
          <div className="p-6 rounded-xl border border-border bg-card">
            <div className="flex items-center space-x-3 mb-4">
              <Star className="h-6 w-6 text-gold" />
              <h2 className="text-2xl font-playfair font-semibold m-0">Who We Are</h2>
            </div>
            <p className="text-muted-foreground leading-relaxed">
              Everyday Horoscope is a Vedic astrology platform operated by <strong>SkyHound Studios</strong>. We combine the timeless traditions of Vedic astrology with modern technology to deliver deeply personal, insightful guidance to our users every day.
            </p>
          </div>

          <div className="p-6 rounded-xl border border-border bg-card">
            <div className="flex items-center space-x-3 mb-4">
              <Heart className="h-6 w-6 text-gold" />
              <h2 className="text-2xl font-playfair font-semibold m-0">Our Mission</h2>
            </div>
            <p className="text-muted-foreground leading-relaxed">
              We believe everyone deserves access to meaningful self-reflection tools. Our mission is to make astrological wisdom accessible, actionable, and relevant to modern life — whether you're seeking daily guidance, understanding your birth chart, or exploring compatibility with a loved one.
            </p>
          </div>

          <div className="p-6 rounded-xl border border-border bg-card">
            <div className="flex items-center space-x-3 mb-4">
              <Shield className="h-6 w-6 text-gold" />
              <h2 className="text-2xl font-playfair font-semibold m-0">Our Approach</h2>
            </div>
            <p className="text-muted-foreground leading-relaxed">
              All insights on Everyday Horoscope are generated using authentic Vedic astrological frameworks — Parashari, KP, and Jaimini systems — interpreted and delivered with modern precision. Our content is designed for informational, reflective, and experiential purposes. We encourage users to engage with our content as a tool for personal reflection and self-discovery.
            </p>
          </div>

          <div className="p-6 rounded-xl border border-gold/30 bg-gold/5 text-center">
            <p className="text-muted-foreground text-sm">
              Everyday Horoscope is a product of <strong>SkyHound Studios</strong>.<br />
              Registered in India. All services governed by the laws of India, jurisdiction: Delhi.
            </p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};
