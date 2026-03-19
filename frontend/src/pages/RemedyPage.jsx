import React from 'react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Gem, BookMarked, Shield, Leaf, Zap, Sparkles } from 'lucide-react';

const REMEDY_CONFIG = {
  'gemstones': {
    title: 'Vedic Gemstones',
    icon: Gem,
    desc: 'Ratna Shastra — the science of gemstones in Vedic astrology. Each planet has a ruling gemstone that can strengthen or pacify its influence in your birth chart.',
    items: [
      { name: 'Ruby (Manik)', planet: 'Sun', color: 'text-red-500', benefit: 'Confidence, leadership, vitality' },
      { name: 'Pearl (Moti)', planet: 'Moon', color: 'text-blue-300', benefit: 'Emotional stability, intuition, peace' },
      { name: 'Red Coral (Moonga)', planet: 'Mars', color: 'text-orange-500', benefit: 'Courage, energy, protection' },
      { name: 'Emerald (Panna)', planet: 'Mercury', color: 'text-green-500', benefit: 'Intelligence, communication, business' },
      { name: 'Yellow Sapphire (Pukhraj)', planet: 'Jupiter', color: 'text-yellow-500', benefit: 'Wisdom, wealth, marriage luck' },
      { name: 'Diamond (Heera)', planet: 'Venus', color: 'text-purple-300', benefit: 'Love, luxury, artistic gifts' },
      { name: 'Blue Sapphire (Neelam)', planet: 'Saturn', color: 'text-blue-600', benefit: 'Discipline, career, longevity' },
      { name: 'Hessonite (Gomed)', planet: 'Rahu', color: 'text-amber-700', benefit: 'Clarity, protection from illusions' },
      { name: "Cat's Eye (Lehsunia)", planet: 'Ketu', color: 'text-gray-400', benefit: 'Spiritual growth, moksha path' },
    ],
  },
  'mantras': {
    title: 'Vedic Mantras',
    icon: BookMarked,
    desc: 'Sacred sound vibrations that balance planetary energies. Each Navagraha has specific mantras chanted at prescribed times for maximum effect.',
    items: [
      { name: 'Surya Mantra', planet: 'Sun', color: 'text-yellow-500', benefit: 'Om Hraam Hreem Hraum Sah Suryaya Namah' },
      { name: 'Chandra Mantra', planet: 'Moon', color: 'text-blue-300', benefit: 'Om Shraam Shreem Shraum Sah Chandraya Namah' },
      { name: 'Mangal Mantra', planet: 'Mars', color: 'text-red-500', benefit: 'Om Kraam Kreem Kraum Sah Bhaumaya Namah' },
      { name: 'Budha Mantra', planet: 'Mercury', color: 'text-green-500', benefit: 'Om Braam Breem Braum Sah Budhaya Namah' },
      { name: 'Guru Mantra', planet: 'Jupiter', color: 'text-amber-500', benefit: 'Om Graam Greem Graum Sah Guruve Namah' },
      { name: 'Shukra Mantra', planet: 'Venus', color: 'text-purple-400', benefit: 'Om Draam Dreem Draum Sah Shukraya Namah' },
      { name: 'Shani Mantra', planet: 'Saturn', color: 'text-blue-600', benefit: 'Om Praam Preem Praum Sah Shanaye Namah' },
    ],
  },
  'yantras': {
    title: 'Vedic Yantras',
    icon: Shield,
    desc: 'Sacred geometric diagrams — cosmic antennas that attract and amplify specific planetary energies. Energised and installed facing specific directions.',
    items: [
      { name: 'Shree Yantra', planet: 'Lakshmi / Venus', color: 'text-gold', benefit: 'Abundance, prosperity, fulfillment of desires' },
      { name: 'Surya Yantra', planet: 'Sun', color: 'text-yellow-500', benefit: 'Power, authority, good health' },
      { name: 'Ganesh Yantra', planet: 'Ketu', color: 'text-orange-500', benefit: 'Removal of obstacles, new beginnings' },
      { name: 'Kuber Yantra', planet: 'Mercury / Jupiter', color: 'text-green-500', benefit: 'Wealth attraction, financial stability' },
      { name: 'Baglamukhi Yantra', planet: 'Mars', color: 'text-red-500', benefit: 'Protection from enemies and negative forces' },
      { name: 'Mahamrityunjaya Yantra', planet: 'Moon', color: 'text-blue-300', benefit: 'Health, longevity, overcoming fear' },
    ],
  },
  'feng-shui': {
    title: 'Feng Shui',
    icon: Leaf,
    desc: 'The ancient Chinese art of harmonising your living space with natural energy flow. Combined with Vastu Shastra principles for Indian homes.',
    items: [
      { name: 'Bagua Energy Map', planet: 'All directions', color: 'text-green-500', benefit: 'Balance all 8 life areas in your home' },
      { name: 'Lucky Bamboo', planet: 'Wood element', color: 'text-green-600', benefit: 'Growth, prosperity, good fortune' },
      { name: 'Wind Chimes', planet: 'Metal element', color: 'text-gray-400', benefit: 'Activate positive chi, dispel stagnant energy' },
      { name: 'Water Fountain', planet: 'Water element', color: 'text-blue-500', benefit: 'Flow of wealth and opportunities' },
      { name: 'Crystal Bowl', planet: 'Earth element', color: 'text-purple-300', benefit: 'Stability, grounding, amplification' },
    ],
  },
  'crystal-therapy': {
    title: 'Crystal Therapy',
    icon: Zap,
    desc: 'Healing crystals work on the subtle energy body — chakras and auras — to restore balance. Each crystal resonates with specific chakras and planetary energies.',
    items: [
      { name: 'Clear Quartz', planet: 'Sun / Crown Chakra', color: 'text-white', benefit: 'Amplifies intention, master healer' },
      { name: 'Amethyst', planet: 'Saturn / Third Eye', color: 'text-purple-500', benefit: 'Intuition, protection, spiritual growth' },
      { name: 'Rose Quartz', planet: 'Venus / Heart', color: 'text-pink-400', benefit: 'Unconditional love, emotional healing' },
      { name: 'Black Tourmaline', planet: 'Rahu / Root', color: 'text-gray-600', benefit: 'Protection, grounding, negativity shield' },
      { name: 'Citrine', planet: 'Jupiter / Solar Plexus', color: 'text-yellow-400', benefit: 'Abundance, confidence, solar energy' },
      { name: 'Lapis Lazuli', planet: 'Mercury / Throat', color: 'text-blue-600', benefit: 'Truth, communication, wisdom' },
    ],
  },
};

export const RemedyPage = ({ type = 'gemstones' }) => {
  const config = REMEDY_CONFIG[type] || REMEDY_CONFIG.gemstones;
  const Icon = config.icon;
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <SEO title={`${config.title} — Everyday Horoscope`} description={config.desc} />
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <Icon className="h-3 w-3" /> Engine 7 · Remedial Science
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">{config.title}</h1>
        <p className="text-muted-foreground max-w-xl mx-auto">{config.desc}</p>
      </div>
      <div className="space-y-3">
        {config.items.map((item) => (
          <Card key={item.name} className="p-4 border border-border flex items-center gap-4">
            <div className="w-10 h-10 rounded-sm bg-muted flex items-center justify-center flex-shrink-0">
              <Sparkles className={`h-5 w-5 ${item.color}`} />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-0.5">
                <p className="font-medium text-sm">{item.name}</p>
                <span className="text-xs text-muted-foreground bg-muted px-2 py-0.5 rounded-full">{item.planet}</span>
              </div>
              <p className="text-xs text-muted-foreground">{item.benefit}</p>
            </div>
          </Card>
        ))}
      </div>
      <p className="text-center text-xs text-muted-foreground mt-8">
        Personalised remedy recommendations based on your birth chart are included in all premium reports.
      </p>
    </div>
  );
};
