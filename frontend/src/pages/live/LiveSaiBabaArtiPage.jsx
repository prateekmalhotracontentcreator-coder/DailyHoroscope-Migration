import React, { useCallback, useRef, useState } from 'react';
import {
  ExternalLink,
  Heart,
  Play,
  Radio,
  ScrollText,
  Volume2,
  VolumeX,
  Youtube,
} from 'lucide-react';
import { Link } from 'react-router-dom';

import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { useLiveTv } from '../../hooks/useLiveTv';

const SITE = 'https://www.everydayhoroscope.in';
const YT_CHANNEL = 'https://www.youtube.com/@SkyHoundStudios';

// ─── Full Arti lyrics ─────────────────────────────────────────────────────────
const LYRICS = [
  {
    hindi: 'आरती साईं बाबा, सौख्यदातारा जीवा',
    roman: 'Arati Sai Baba, saukhyadataara jeeva',
    english: 'I offer prayers to Sai Baba -- giver of happiness and peace to every living being',
  },
  {
    hindi: 'चरणरजतळी द्यावा, दासा विसावा',
    roman: 'Charanarajatali dyava, dasa visava',
    english: 'Grant us the sacred dust of Thy lotus feet; give rest and refuge to Thy devotees',
  },
  {
    hindi: 'जाळूनिया अनंगा, स्वस्वरूपी राहे दंगा',
    roman: 'Jaluniya ananga, svasvarupi rahe danga',
    english: 'Having burned away all bodily desires, remain absorbed in Thy own divine Self',
  },
  {
    hindi: 'मुमुक्षु जना दावी, निज डोळा श्रीरंगा',
    roman: 'Mumukshu jana davi, nija dola Shriranga',
    english: 'Reveal Thyself to seekers of liberation through Thine own compassionate divine eyes',
  },
  {
    hindi: 'जय मनी जैसा भाव, तया तैसा अनुभव',
    roman: 'Jaya mani jaisa bhava, taya taisa anubhava',
    english: 'As is the faith in the heart of the devotee, so exactly is the grace and experience granted',
  },
  {
    hindi: 'दाविसी दयाघना, ऐसी तुझी ही माया',
    roman: 'Davisi dayaghana, aisi tujhi hi maya',
    english: 'Thou showest Thy boundless compassion -- such is Thy all-encompassing divine grace and maya',
  },
  {
    hindi: 'तुमचे नाम ध्यातां, हरे संकट चिंता',
    roman: 'Tumache naama dhyata, hare sankata chinta',
    english: 'By meditating on Thy holy name, all troubles, fears, and anxieties are completely dissolved',
  },
  {
    hindi: 'कलियुगी अवतार, सगुण परब्रह्म साचार',
    roman: 'Kaliyugi avatara, saguna parabrahma sachara',
    english: 'The incarnation of this age of Kali -- the Supreme Brahman who descended in human form',
  },
  {
    hindi: 'अवतीर्ण झाला स्वामी, दत्त दिगंबर',
    roman: 'Avatirna jhala svami, Datta Digambara',
    english: 'The Lord has descended -- Datta Digambara, boundless and transcending all directions',
  },
];

// ─── Devotional library items (future playlist foundation) ───────────────────
const ARTI_LIBRARY = [
  {
    id: 'sai-baba',
    label: 'Sai Baba Arti',
    sub: 'Om Sai Ram · Shirdi',
    icon: '🙏',
    active: true,
  },
  {
    id: 'ganesh',
    label: 'Ganesh Vandana',
    sub: 'Jai Ganesh · Morning',
    icon: '🐘',
    active: false,
    soon: true,
  },
  {
    id: 'hanuman',
    label: 'Hanuman Chalisa',
    sub: 'Jai Bajrangbali · Daily',
    icon: '🚩',
    active: false,
    soon: true,
  },
  {
    id: 'durga',
    label: 'Durga Arti',
    sub: 'Jai Ambe Gauri · Evening',
    icon: '🪔',
    active: false,
    soon: true,
  },
];

// ─── Schema.org VideoObject ───────────────────────────────────────────────────
function buildSchema(video) {
  return {
    '@context': 'https://schema.org',
    '@type': 'VideoObject',
    name: 'Live Sai Baba Arti | Om Sai Ram | EverydayHoroscope',
    description:
      'Continuous live Sai Baba Arti devotional stream on EverydayHoroscope. Full Hindi lyrics with English meaning and transliteration. Om Sai Ram. Experience divine blessings from Shirdi 24/7.',
    thumbnailUrl: video?.thumbnail_url || `${SITE}/og-image.jpg`,
    uploadDate: video?.generated_at || new Date().toISOString(),
    contentUrl: video?.website_video_url || SITE,
    embedUrl: video?.youtube_embed_url || video?.website_video_url || SITE,
    publisher: { '@type': 'Organization', name: 'EverydayHoroscope', url: SITE },
  };
}

// ─── Full-viewport hero player + control console ─────────────────────────────
// Uses a callback ref to set elem.muted=true SYNCHRONOUSLY before the browser
// evaluates its autoplay policy -- the React `muted` JSX prop is unreliable.
function HeroPlayer({ videoUrl, posterUrl, title }) {
  const videoRef = useRef(null);
  const [muted, setMuted] = useState(true);
  const [playing, setPlaying] = useState(false);

  const attachRef = useCallback(
    (el) => {
      if (!el) return;
      el.muted = true;
      el.defaultMuted = true;
      videoRef.current = el;
      el.play()
        .then(() => setPlaying(true))
        .catch(() => setPlaying(false));
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [videoUrl],
  );

  const toggleMute = () => {
    const next = !muted;
    setMuted(next);
    if (videoRef.current) videoRef.current.muted = next;
  };

  const handleManualPlay = () => {
    if (!videoRef.current) return;
    videoRef.current.play()
      .then(() => setPlaying(true))
      .catch(() => {});
  };

  return (
    <div className="flex w-full flex-col bg-black">
      {/* ── Video canvas ── */}
      <div className="relative w-full aspect-video lg:aspect-auto lg:h-[calc(75vh-56px)] overflow-hidden" style={{ minHeight: '220px' }}>
        <video
          ref={attachRef}
          key={videoUrl}
          src={videoUrl}
          poster={posterUrl}
          autoPlay
          loop
          playsInline
          preload="auto"
          className="h-full w-full object-contain"
          onPlay={() => setPlaying(true)}
        />

        {/* 🔴 LIVE badge */}
        <div className="absolute left-4 top-4 z-20 flex items-center gap-2 rounded-full bg-black/75 px-3 py-1.5 backdrop-blur-sm">
          <span className="relative flex h-2.5 w-2.5">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-500 opacity-75" />
            <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-red-500" />
          </span>
          <span className="text-xs font-bold uppercase tracking-[0.18em] text-white">
            Live · Sai Baba Arti
          </span>
        </div>

        {/* Manual play overlay -- shown only when autoplay is blocked */}
        {!playing && (
          <button
            type="button"
            onClick={handleManualPlay}
            className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-[2px] transition hover:bg-black/50"
            aria-label="Play Sai Baba Arti"
          >
            <div className="grid h-24 w-24 place-items-center rounded-full bg-gold/90 text-black shadow-[0_12px_40px_rgba(197,160,89,0.6)]">
              <Play className="h-10 w-10 translate-x-0.5" />
            </div>
          </button>
        )}
      </div>

      {/* ── Player console / control bar ── */}
      <div className="flex shrink-0 items-center justify-between gap-4 border-t border-gold/20 bg-card/95 px-5 py-3 backdrop-blur-sm">
        <div className="flex items-center gap-3 min-w-0">
          {/* Play / status indicator */}
          {!playing ? (
            <button
              type="button"
              onClick={handleManualPlay}
              className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-gold text-black shadow-[0_4px_14px_rgba(197,160,89,0.5)] transition hover:bg-gold/90"
              aria-label="Play"
            >
              <Play className="h-4 w-4 translate-x-0.5" />
            </button>
          ) : (
            <div className="flex h-9 w-9 shrink-0 items-center justify-center gap-0.5">
              {[0, 1, 2].map((i) => (
                <span
                  key={i}
                  className="inline-block w-1 rounded-full bg-gold"
                  style={{
                    height: `${12 + i * 4}px`,
                    animation: `pulse 0.8s ease-in-out ${i * 0.15}s infinite alternate`,
                  }}
                />
              ))}
            </div>
          )}
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold text-foreground">
              {title || 'LIVE Sai Baba Arti | Om Sai Ram'}
            </p>
            <p className="text-xs text-muted-foreground">
              {playing ? 'Playing · continuous loop · 24/7' : 'Tap ▶ to begin devotional stream'}
            </p>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <button
            type="button"
            onClick={toggleMute}
            className="inline-flex items-center gap-1.5 rounded-full border border-gold/30 bg-background/60 px-4 py-2 text-xs font-semibold text-gold transition hover:bg-gold/10"
          >
            {muted ? <VolumeX className="h-4 w-4" /> : <Volume2 className="h-4 w-4" />}
            {muted ? 'Unmute' : 'Mute'}
          </button>
          <a
            href={YT_CHANNEL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 rounded-full border border-red-500/30 bg-red-500/10 px-4 py-2 text-xs font-semibold text-red-400 transition hover:bg-red-500/20"
          >
            <Youtube className="h-4 w-4" />
            YouTube
          </a>
        </div>
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function LiveSaiBabaArtiPage() {
  const { data, loading } = useLiveTv();

  return (
    <div className="min-h-screen bg-background text-foreground">
      <SEO
        title="Live Sai Baba Arti | Om Sai Ram | 24/7 Devotional Stream"
        description="Watch Sai Baba Arti live 24/7 on EverydayHoroscope. Continuous devotional stream with full Hindi lyrics, English transliteration, and meaning. Experience divine blessings from Shirdi. Om Sai Ram."
        url={`${SITE}/live-sai-baba-arti`}
        schema={buildSchema(data)}
      />

      {/* ── HERO: Full-viewport immersive player + console ───────────────────── */}
      <section className="w-full bg-black">
        {loading ? (
          <div className="flex h-[56vw] max-h-[60vh] min-h-[220px] w-full items-center justify-center bg-black">
            <div className="text-center">
              <div className="mx-auto mb-5 h-12 w-12 animate-spin rounded-full border-4 border-gold/25 border-t-gold" />
              <p className="text-sm font-medium tracking-wider text-gold/60">Connecting to Live Arti...</p>
            </div>
          </div>
        ) : data?.website_video_url ? (
          <HeroPlayer
            videoUrl={data.website_video_url}
            posterUrl={data.thumbnail_url}
            title={data.title}
          />
        ) : (
          <div className="flex h-[56vw] max-h-[60vh] min-h-[220px] w-full flex-col items-center justify-center gap-6 bg-gradient-to-br from-black via-[#0d0a05] to-[#191205]">
            <div className="grid h-28 w-28 place-items-center rounded-full border border-gold/30 bg-gold/10 text-6xl shadow-[0_0_60px_rgba(197,160,89,0.2)]">
              🙏
            </div>
            <div className="text-center">
              <p className="font-playfair text-3xl font-semibold text-gold">Om Sai Ram</p>
              <p className="mt-3 max-w-md text-sm leading-7 text-white/45">
                Live stream activates when a source video is configured.
              </p>
            </div>
          </div>
        )}
      </section>

      {/* ── YouTube channel strip ─────────────────────────────────────────────── */}
      <div className="border-b border-gold/15 bg-gold/[0.05]">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            <Radio className="h-4 w-4 shrink-0 text-gold" />
            <span>Continuous devotional stream · loops 24/7 · starts muted</span>
          </div>
          <a
            href={YT_CHANNEL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex shrink-0 items-center gap-2 rounded-full border border-red-500/35 bg-red-500/10 px-5 py-2 text-sm font-semibold text-red-400 transition hover:bg-red-500/20"
          >
            <Youtube className="h-4 w-4" />
            Watch on YouTube
            <ExternalLink className="h-3.5 w-3.5 opacity-70" />
          </a>
        </div>
      </div>

      {/* ── Main content ──────────────────────────────────────────────────────── */}
      <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">

        {/* Page title */}
        <div className="mb-16 max-w-4xl">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
            <Heart className="h-3.5 w-3.5" />
            Shirdi Sai Baba · Devotional Media
          </div>
          <h1 className="font-playfair text-5xl font-bold leading-tight text-foreground sm:text-6xl">
            Live Sai Baba Arti
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-muted-foreground">
            Experience the divine grace of Shirdi Sai Baba through a continuous devotional Arti stream.
            The player loops at source level, starts muted for browser compatibility, and offers
            one-tap unmute for the full Arti audio.{' '}
            <strong className="font-semibold text-foreground">Om Sai Ram.</strong>
          </p>
        </div>

        {/* ── Arti Library / Playlist ───────────────────────────────────────── */}
        <section className="mb-16">
          <div className="mb-6">
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.28em] text-gold/80">
              Devotional Library
            </p>
            <h2 className="font-playfair text-3xl font-semibold text-foreground">
              Arti Playlist
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              The active stream is shown below. More Artis are added as the library grows.
            </p>
          </div>

          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {ARTI_LIBRARY.map((item) => (
              <div
                key={item.id}
                className={`relative flex items-center gap-4 rounded-2xl border px-5 py-4 transition ${
                  item.active
                    ? 'border-gold/40 bg-gold/[0.08] shadow-[0_0_24px_rgba(197,160,89,0.12)]'
                    : 'border-gold/10 bg-card/60 opacity-60'
                }`}
              >
                <div
                  className={`grid h-12 w-12 shrink-0 place-items-center rounded-2xl text-2xl ${
                    item.active ? 'bg-gold/15 border border-gold/30' : 'bg-card border border-gold/10'
                  }`}
                >
                  {item.icon}
                </div>
                <div className="min-w-0">
                  <p className="truncate font-semibold text-foreground">{item.label}</p>
                  <p className="mt-0.5 truncate text-xs text-muted-foreground">{item.sub}</p>
                </div>
                {item.active && (
                  <div className="absolute right-3 top-3 flex items-center gap-1 rounded-full bg-gold/20 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-gold">
                    <span className="h-1.5 w-1.5 rounded-full bg-red-500" />
                    Live
                  </div>
                )}
                {item.soon && (
                  <div className="absolute right-3 top-3 rounded-full bg-card px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
                    Soon
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* ── About Shirdi Sai Baba ─────────────────────────────────────────── */}
        <section className="mb-16 overflow-hidden rounded-[30px] border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-card to-card p-8 shadow-[0_28px_70px_-24px_rgba(197,160,89,0.22)] lg:p-12">
          <div className="grid gap-12 lg:grid-cols-[1.5fr_1fr] lg:items-start">
            <div>
              <p className="mb-3 text-xs font-semibold uppercase tracking-[0.28em] text-gold/80">
                About the Saint
              </p>
              <h2 className="mb-7 font-playfair text-4xl font-semibold text-foreground">
                Shirdi Sai Baba
              </h2>
              <div className="space-y-5 text-base leading-8 text-muted-foreground">
                <p>
                  Shirdi Sai Baba was a revered spiritual master who resided in the small village of
                  Shirdi, Maharashtra, India. Venerated by millions of devotees worldwide -- Hindu and
                  Muslim alike -- he is considered an incarnation of divine compassion. His core
                  teaching,{' '}
                  <em className="text-foreground">"Shraddha and Saburi"</em> (Faith and Patience),
                  remains the eternal cornerstone of his philosophy.
                </p>
                <p>
                  Sai Baba performed countless miracles throughout his lifetime -- healing the sick,
                  feeding the hungry, and guiding seekers of all faiths toward the one formless God.
                  He spent his days at the Dwarkamai mosque in Shirdi, always keeping a sacred fire
                  (dhuni) burning: a symbol of his eternal, unwavering presence and warmth.
                </p>
                <p>
                  He took Mahasamadhi on 15 October 1918, yet his devotees believe he continues to
                  guide and bless all who call upon his name with sincere faith. The Arti sung at
                  Shirdi -- five times daily -- is the sacred hymn honouring his eternal divine grace.
                  May his blessings reach you through this continuous stream.
                </p>
              </div>
            </div>
            <div className="grid gap-3">
              {[
                { label: 'Core Teaching', value: 'Shraddha & Saburi -- Faith and Patience' },
                { label: 'Sacred Abode', value: 'Dwarkamai Mosque, Shirdi, Maharashtra' },
                { label: 'Mahasamadhi', value: '15 October 1918' },
                { label: 'Daily Artis', value: 'Five -- Kakad, Madhyan, Dhoop, Shej, Satka' },
                { label: 'Philosophy', value: 'Sarva Dharma Sambhav -- all paths lead to one God' },
                { label: 'Mantra', value: 'Om Sai Ram · Sai Baba Ki Jai' },
              ].map(({ label, value }) => (
                <div
                  key={label}
                  className="flex gap-4 rounded-2xl border border-gold/15 bg-gold/[0.04] px-5 py-4"
                >
                  <div className="mt-0.5 shrink-0 text-gold">✦</div>
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold/70">
                      {label}
                    </p>
                    <p className="mt-1 text-sm leading-6 text-foreground">{value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Lyrics table ─────────────────────────────────────────────────── */}
        <section id="lyrics" className="mb-16">
          <div className="mb-8">
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.28em] text-gold/80">
              Sacred Hymn
            </p>
            <h2 className="font-playfair text-4xl font-semibold text-foreground">
              Sai Baba Arti -- Lyrics &amp; English Meaning
            </h2>
            <p className="mt-4 max-w-2xl text-sm leading-7 text-muted-foreground">
              The Arti is sung in Marathi and Hindi. Below you will find the original Devanagari
              script, Roman transliteration, and the English meaning of each verse.
            </p>
          </div>

          <div className="overflow-x-auto rounded-[24px] border border-gold/20 bg-card/80">
            <div className="min-w-[720px] grid grid-cols-[1.1fr_1fr_1.2fr] border-b border-gold/15 bg-gold/[0.06] px-6 py-3.5 text-xs font-semibold uppercase tracking-[0.22em] text-gold/70">
              <span>Original (Hindi / Marathi)</span>
              <span className="border-l border-gold/10 pl-6">Transliteration</span>
              <span className="border-l border-gold/10 pl-6">English Meaning</span>
            </div>
            <div className="min-w-[720px] divide-y divide-gold/10">
              {LYRICS.map((line, i) => (
                <div
                  key={i}
                  className="grid grid-cols-[1.1fr_1fr_1.2fr] px-6 py-5 transition-colors hover:bg-gold/[0.03]"
                >
                  <p className="pr-6 text-base leading-8 text-foreground">{line.hindi}</p>
                  <p className="border-l border-gold/10 pl-6 pr-6 font-playfair text-base italic leading-8 text-muted-foreground">
                    {line.roman}
                  </p>
                  <p className="border-l border-gold/10 pl-6 text-sm leading-7 text-muted-foreground">
                    {line.english}
                  </p>
                </div>
              ))}
            </div>
          </div>
          <p className="mt-4 text-xs text-muted-foreground">
            Scroll right on smaller screens to see all three columns.
          </p>
        </section>

        {/* ── Feature cards ─────────────────────────────────────────────────── */}
        <section className="mb-16 grid gap-5 sm:grid-cols-3">
          {[
            {
              icon: Heart,
              title: 'Continuous Darshan',
              body: 'The stream uses a normalised MP4 directly -- it loops without waiting for a YouTube publish cycle, giving uninterrupted Sai Baba darshan any time of day.',
            },
            {
              icon: Radio,
              title: 'Temple-Safe Playback',
              body: 'Autoplay begins muted for browser compliance. One tap on Unmute enables the full Arti audio experience.',
            },
            {
              icon: ScrollText,
              title: 'SEO Discovery Page',
              body: 'Shareable, indexable, and rich with lyrics, meaning, and schema markup -- so new devotees searching for Sai Baba Arti find their way here.',
            },
          ].map(({ icon: Icon, title, body }) => (
            <div
              key={title}
              className="rounded-[22px] border border-gold/20 bg-gold/[0.04] p-6 shadow-sm backdrop-blur-sm"
            >
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-2xl border border-gold/25 bg-gold/10 text-gold">
                <Icon className="h-5 w-5" />
              </div>
              <h3 className="mb-2 font-playfair text-xl font-semibold text-foreground">{title}</h3>
              <p className="text-sm leading-7 text-muted-foreground">{body}</p>
            </div>
          ))}
        </section>

        {/* ── Cross-links ───────────────────────────────────────────────────── */}
        <section className="mb-16">
          <div className="mb-7">
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.28em] text-gold/80">
              Explore the Temple
            </p>
            <h2 className="font-playfair text-3xl font-semibold text-foreground">
              More sacred tools for your daily practice
            </h2>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                to: '/panchang',
                label: 'Daily Panchang',
                description: 'Auspicious timings, tithi, nakshatra, and choghadiya for today',
                icon: '🗓',
                external: false,
              },
              {
                to: '/daily-horoscope',
                label: 'Daily Horoscope',
                description: 'Vedic daily guidance for all 12 zodiac signs',
                icon: '⭐',
                external: false,
              },
              {
                to: '/individual-reports',
                label: 'Vedic Reports',
                description: 'Karmic Debt, Career Blueprint, Shadow Self, and more',
                icon: '📜',
                external: false,
              },
              {
                to: YT_CHANNEL,
                label: 'YouTube Channel',
                description: 'Subscribe for Arti videos, horoscopes, and daily Vedic content',
                icon: '▶',
                external: true,
              },
            ].map(({ to, label, description, icon, external }) => {
              const inner = (
                <>
                  <div className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl border border-gold/20 bg-gold/[0.08] text-xl">
                    {icon}
                  </div>
                  <div>
                    <p className="font-semibold text-foreground transition-colors group-hover:text-gold">
                      {label}
                    </p>
                    <p className="mt-1 text-xs leading-5 text-muted-foreground">{description}</p>
                  </div>
                </>
              );
              const cls =
                'group flex gap-4 rounded-[20px] border border-gold/20 bg-card/80 p-5 transition-colors hover:border-gold/40 hover:bg-gold/[0.06]';
              return external ? (
                <a key={label} href={to} target="_blank" rel="noreferrer" className={cls}>
                  {inner}
                </a>
              ) : (
                <Link key={label} to={to} className={cls}>
                  {inner}
                </Link>
              );
            })}
          </div>
        </section>

        {/* ── YouTube subscribe banner ──────────────────────────────────────── */}
        <section className="overflow-hidden rounded-[28px] border border-red-500/20 bg-gradient-to-br from-red-950/30 via-card to-card p-8 shadow-[0_24px_60px_-20px_rgba(239,68,68,0.14)] sm:p-10">
          <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
            <div className="max-w-xl">
              <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-red-500/30 bg-red-500/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.2em] text-red-400">
                <Youtube className="h-3.5 w-3.5" />
                YouTube Channel
              </div>
              <h3 className="font-playfair text-3xl font-semibold text-foreground">
                Watch Sai Baba Arti on YouTube
              </h3>
              <p className="mt-4 text-sm leading-7 text-muted-foreground">
                Subscribe for Sai Baba Arti videos, daily horoscope updates, Vedic astrology
                guidance, and devotional content. Om Sai Ram.
              </p>
            </div>
            <a
              href={YT_CHANNEL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex shrink-0 items-center gap-2 rounded-full bg-red-600 px-7 py-3.5 text-sm font-semibold text-white shadow-[0_12px_32px_rgba(239,68,68,0.35)] transition hover:bg-red-500"
            >
              <Youtube className="h-4 w-4" />
              Subscribe Now
              <ExternalLink className="h-3.5 w-3.5 opacity-80" />
            </a>
          </div>
        </section>

      </div>

      <Footer />
    </div>
  );
}
