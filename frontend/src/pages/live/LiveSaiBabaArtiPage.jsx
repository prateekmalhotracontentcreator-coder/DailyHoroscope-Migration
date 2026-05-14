import React from 'react';
import { ExternalLink, Heart, Radio, ScrollText } from 'lucide-react';

import { Footer } from '../../components/Footer';
import { LiveTVPlayer } from '../../components/LiveTVPanel';
import { SEO } from '../../components/SEO';
import { Card } from '../../components/ui/card';
import { useLiveTv } from '../../hooks/useLiveTv';

const SITE = 'https://www.everydayhoroscope.in';

const LYRICS = [
  {
    hindi: 'आरती साईं बाबा, सौख्यदातारा जीवा',
    transliteration: 'Arati Sai Baba, saukhyadataara jeeva',
  },
  {
    hindi: 'चरणरजतळी द्यावा, दासा विसावा',
    transliteration: 'Charanarajatali dyava, dasa visava',
  },
  {
    hindi: 'जाळूनिया अनंगा, स्वस्वरूपी राहे दंगा',
    transliteration: 'Jaluniya ananga, svasvarupi rahe danga',
  },
  {
    hindi: 'मुमुक्षु जना दावी, निज डोळा श्रीरंगा',
    transliteration: 'Mumukshu jana davi, nija dola Shriranga',
  },
  {
    hindi: 'जय मनी जैसा भाव, तया तैसा अनुभव',
    transliteration: 'Jaya mani jaisa bhava, taya taisa anubhava',
  },
  {
    hindi: 'दाविसी दयाघना, ऐसी तुझी ही माया',
    transliteration: 'Davisi dayaghana, aisi tujhi hi maya',
  },
];

function buildSchema(video) {
  if (!video) return null;
  return {
    '@context': 'https://schema.org',
    '@type': 'VideoObject',
    name: video.title || 'Live Sai Baba Arti | Om Sai Ram',
    description: video.description || 'Continuous live Sai Baba Arti for darshan and devotional listening.',
    thumbnailUrl: video.thumbnail_url,
    uploadDate: video.generated_at,
    contentUrl: video.youtube_url || video.website_video_url,
    embedUrl: video.youtube_embed_url || video.website_video_url,
    publisher: {
      '@type': 'Organization',
      name: 'EverydayHoroscope',
      url: SITE,
    },
  };
}

export default function LiveSaiBabaArtiPage() {
  const { data, loading, error } = useLiveTv();

  return (
    <div className="min-h-screen bg-background text-foreground">
      <SEO
        title="Live Sai Baba Arti | Om Sai Ram"
        description="Watch Sai Baba Arti live 24/7 on EverydayHoroscope. Experience divine blessings with continuous Sai Baba Aarti and a dedicated devotional page."
        url={`${SITE}/live-sai-baba-arti`}
        schema={buildSchema(data)}
      />

      <main className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
        <section className="mb-10 overflow-hidden rounded-[28px] border border-gold/20 bg-gradient-to-br from-gold/10 via-card to-card p-6 shadow-[0_24px_80px_-30px_rgba(197,160,89,0.35)] sm:p-8">
          <div className="mb-6 flex flex-wrap items-center gap-3 text-xs font-semibold uppercase tracking-[0.22em] text-gold">
            <span className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-background/60 px-3 py-1.5">
              <Radio className="h-3.5 w-3.5" />
              Live Sai Baba Arti
            </span>
            <span className="rounded-full border border-gold/15 bg-card/70 px-3 py-1.5 text-muted-foreground">
              Temple-native devotional media
            </span>
          </div>

          <div className="grid gap-8 lg:grid-cols-[minmax(0,1.35fr)_minmax(320px,0.9fr)] lg:items-center">
            <div>
              <h1 className="font-cinzel text-4xl font-bold leading-tight sm:text-5xl">
                Live Sai Baba Arti
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
                Keep a continuous Sai Baba darshan stream open inside the Temple. The website player loops at the player level,
                starts muted for browser safety, and gives devotees a simple one-tap unmute experience.
              </p>

              <div className="mt-6 flex flex-wrap gap-3">
                <a
                  href="#lyrics"
                  className="inline-flex items-center gap-2 rounded-full bg-gold px-5 py-2.5 text-sm font-semibold text-primary-foreground transition-colors hover:bg-gold/90"
                >
                  <ScrollText className="h-4 w-4" />
                  Read Arti Lyrics
                </a>
                {data?.youtube_url && (
                  <a
                    href={data.youtube_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 rounded-full border border-gold/25 px-5 py-2.5 text-sm font-semibold text-gold transition-colors hover:bg-gold/10"
                  >
                    Watch on YouTube
                    <ExternalLink className="h-4 w-4" />
                  </a>
                )}
              </div>
            </div>

            <Card className="rounded-[24px] border-gold/20 bg-background/75 p-4 shadow-none">
              {loading ? (
                <div className="flex aspect-video items-center justify-center rounded-2xl border border-dashed border-gold/20 text-sm text-muted-foreground">
                  Loading Live TV...
                </div>
              ) : data?.website_video_url ? (
                <LiveTVPlayer
                  title={data.title || 'Live Sai Baba Arti'}
                  videoUrl={data.website_video_url}
                  posterUrl={data.thumbnail_url}
                />
              ) : (
                <div className="space-y-3 rounded-2xl border border-dashed border-gold/20 bg-card/70 p-6 text-sm text-muted-foreground">
                  <p className="font-semibold text-foreground">Live TV source video is not configured yet.</p>
                  <p>
                    Temple Team can place the source video in `backend/assets/live_tv/sai_baba/` and run the
                    generator script to activate playback on this page and the homepage panel.
                  </p>
                  {error && <p className="text-xs text-muted-foreground">{error}</p>}
                </div>
              )}
            </Card>
          </div>
        </section>

        <section className="mb-8 grid gap-5 md:grid-cols-3">
          {[
            {
              icon: Heart,
              title: 'Continuous Darshan',
              body: 'The website stream uses the normalized MP4 directly, so it can loop smoothly without waiting for a YouTube publish cycle.',
            },
            {
              icon: Radio,
              title: 'Temple-Safe Playback',
              body: 'Autoplay begins muted for browser compliance, with a clear unmute affordance for devotees who want the full arti audio.',
            },
            {
              icon: ScrollText,
              title: 'SEO Landing Page',
              body: 'This page is shareable, indexable, and rich enough to rank beyond a plain embedded player.',
            },
          ].map(({ icon: Icon, title, body }) => (
            <Card key={title} className="rounded-2xl border-gold/20 bg-card/80 p-5 shadow-none">
              <Icon className="mb-4 h-5 w-5 text-gold" />
              <h2 className="mb-2 font-playfair text-xl font-semibold">{title}</h2>
              <p className="text-sm leading-6 text-muted-foreground">{body}</p>
            </Card>
          ))}
        </section>

        <section id="lyrics" className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
          <Card className="rounded-2xl border-gold/20 bg-card/80 p-6 shadow-none">
            <h2 className="mb-5 font-playfair text-2xl font-semibold">Hindi Lyrics</h2>
            <div className="space-y-4">
              {LYRICS.map((line) => (
                <div key={line.hindi} className="rounded-xl border border-gold/10 bg-background/55 px-4 py-3">
                  <p className="text-lg leading-8">{line.hindi}</p>
                </div>
              ))}
            </div>
          </Card>

          <Card className="rounded-2xl border-gold/20 bg-card/80 p-6 shadow-none">
            <h2 className="mb-5 font-playfair text-2xl font-semibold">Transliteration</h2>
            <div className="space-y-4">
              {LYRICS.map((line) => (
                <div key={line.transliteration} className="rounded-xl border border-gold/10 bg-background/55 px-4 py-3">
                  <p className="font-playfair text-lg italic leading-8 text-muted-foreground">{line.transliteration}</p>
                </div>
              ))}
            </div>
          </Card>
        </section>

        <section className="mt-8">
          <Card className="rounded-2xl border-gold/20 bg-card/80 p-6 shadow-none">
            <h2 className="mb-4 font-playfair text-2xl font-semibold">Why this page exists</h2>
            <div className="space-y-4 text-sm leading-7 text-muted-foreground">
              <p>
                The homepage panel keeps darshan present inside the Temple without turning the whole site into a media shell.
                This dedicated page gives Sai Baba devotees a calmer space for longer viewing, lyrics, and search discovery.
              </p>
              <p>
                The architecture is reusable for future devotional streams. Temple Team can swap in another active video,
                keep the same player contract, and publish a new SEO page with the same pipeline.
              </p>
            </div>
          </Card>
        </section>
      </main>

      <Footer />
    </div>
  );
}
