import React, { useRef, useState } from 'react';
import html2canvas from 'html2canvas';

// ─── Platform icons (inline SVG to avoid extra deps) ────────────────────────

const WhatsAppIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
  </svg>
);

const FacebookIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
  </svg>
);

const XIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.746l7.73-8.835L1.254 2.25H8.08l4.253 5.622zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
  </svg>
);

const InstagramIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
  </svg>
);

const YouTubeIcon = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="h-4 w-4">
    <path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
  </svg>
);

const CopyIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="h-4 w-4">
    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
    <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
  </svg>
);

const DownloadIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="h-4 w-4">
    <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
  </svg>
);

// ─── Share card (the visual card that gets captured as image) ────────────────

export function PanchangShareCard({ data, cardRef }) {
  if (!data) return null;
  const { summary, panchang, special_yogas, observances } = data;
  const yoga = special_yogas?.[0];
  const observance = observances?.[0];
  const dateStr = data.date ? new Date(data.date + 'T00:00:00').toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) : '';

  return (
    <div
      ref={cardRef}
      style={{
        width: 600,
        background: 'linear-gradient(135deg, #0f0e17 0%, #1a1625 50%, #0f0e17 100%)',
        borderRadius: 20,
        padding: 36,
        fontFamily: "'Georgia', serif",
        color: '#f5f0e8',
        position: 'absolute',
        left: -9999,
        top: -9999,
        boxSizing: 'border-box',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 24, borderBottom: '1px solid rgba(197,160,89,0.3)', paddingBottom: 16 }}>
        <div>
          <p style={{ color: '#C5A059', fontSize: 11, letterSpacing: 3, textTransform: 'uppercase', margin: 0 }}>EverydayHoroscope.in</p>
          <p style={{ color: '#f5f0e8', fontSize: 22, fontWeight: 700, margin: '6px 0 0' }}>Vedic Panchang</p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <p style={{ color: '#C5A059', fontSize: 13, margin: 0 }}>{dateStr}</p>
          <p style={{ color: 'rgba(245,240,232,0.6)', fontSize: 11, margin: '4px 0 0' }}>{data.location?.label}, {data.location?.country}</p>
        </div>
      </div>

      {/* Five Limbs grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 20 }}>
        {[
          { label: 'Tithi',     value: panchang?.tithi?.name },
          { label: 'Nakshatra', value: panchang?.nakshatra?.name },
          { label: 'Yoga',      value: panchang?.yoga?.name },
          { label: 'Vara',      value: summary?.weekday },
        ].map(({ label, value }) => (
          <div key={label} style={{ background: 'rgba(197,160,89,0.08)', borderRadius: 10, padding: '10px 14px', border: '1px solid rgba(197,160,89,0.2)' }}>
            <p style={{ color: '#C5A059', fontSize: 10, letterSpacing: 2, textTransform: 'uppercase', margin: 0 }}>{label}</p>
            <p style={{ color: '#f5f0e8', fontSize: 15, fontWeight: 600, margin: '4px 0 0' }}>{value || '—'}</p>
          </div>
        ))}
      </div>

      {/* Sun row */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
        {[
          { label: '☀ Sunrise', value: summary?.sunrise },
          { label: '🌅 Sunset',  value: summary?.sunset },
          { label: '🌙 Moonrise',value: summary?.moonrise || '—' },
        ].map(({ label, value }) => (
          <div key={label} style={{ flex: 1, background: 'rgba(255,255,255,0.04)', borderRadius: 10, padding: '8px 12px', textAlign: 'center' }}>
            <p style={{ color: 'rgba(245,240,232,0.5)', fontSize: 10, margin: 0 }}>{label}</p>
            <p style={{ color: '#f5f0e8', fontSize: 14, fontWeight: 600, margin: '3px 0 0', fontFamily: 'monospace' }}>{value || '—'}</p>
          </div>
        ))}
      </div>

      {/* Special Yoga badge */}
      {yoga && (
        <div style={{ background: yoga.quality === 'good' ? 'rgba(52,211,153,0.1)' : 'rgba(251,191,36,0.1)', border: `1px solid ${yoga.quality === 'good' ? 'rgba(52,211,153,0.3)' : 'rgba(251,191,36,0.3)'}`, borderRadius: 10, padding: '10px 14px', marginBottom: 16 }}>
          <p style={{ color: yoga.quality === 'good' ? '#34d399' : '#fbbf24', fontSize: 13, fontWeight: 700, margin: 0 }}>✦ {yoga.name}</p>
          <p style={{ color: 'rgba(245,240,232,0.7)', fontSize: 11, margin: '4px 0 0' }}>{yoga.meaning.split('—')[0].trim()}</p>
        </div>
      )}

      {/* Observance */}
      {observance && (
        <div style={{ borderTop: '1px solid rgba(197,160,89,0.2)', paddingTop: 14, marginTop: 4 }}>
          <p style={{ color: '#C5A059', fontSize: 11, letterSpacing: 2, textTransform: 'uppercase', margin: '0 0 4px' }}>Today's Observance</p>
          <p style={{ color: '#f5f0e8', fontSize: 14, fontWeight: 600, margin: 0 }}>{observance.name}</p>
        </div>
      )}

      {/* Footer */}
      <div style={{ marginTop: 20, paddingTop: 14, borderTop: '1px solid rgba(197,160,89,0.15)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <p style={{ color: 'rgba(245,240,232,0.4)', fontSize: 10, margin: 0 }}>India's Premium Vedic Astrology Platform</p>
        <p style={{ color: '#C5A059', fontSize: 10, margin: 0, letterSpacing: 1 }}>everydayhoroscope.in</p>
      </div>
    </div>
  );
}

// ─── Share buttons row ───────────────────────────────────────────────────────

export function ShareButtons({ pageUrl, shareText, cardRef, cardData }) {
  const [copied, setCopied] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [showInstaHint, setShowInstaHint] = useState(false);

  const encodedUrl  = encodeURIComponent(pageUrl);
  const encodedText = encodeURIComponent(shareText + '\n' + pageUrl);
  const encodedTweet = encodeURIComponent(shareText);

  const generateImage = async () => {
    if (!cardRef?.current) return null;
    setGenerating(true);
    try {
      const canvas = await html2canvas(cardRef.current, {
        scale: 2,
        useCORS: true,
        backgroundColor: null,
        logging: false,
      });
      return canvas;
    } catch (e) {
      console.error('html2canvas error', e);
      return null;
    } finally {
      setGenerating(false);
    }
  };

  const handleWhatsApp = async () => {
    // Try Web Share API with image first (mobile), else fallback to URL
    if (navigator.canShare && cardRef?.current) {
      const canvas = await generateImage();
      if (canvas) {
        canvas.toBlob(async (blob) => {
          const file = new File([blob], 'panchang.png', { type: 'image/png' });
          if (navigator.canShare({ files: [file] })) {
            try {
              await navigator.share({ files: [file], title: 'Daily Panchang', text: shareText });
              return;
            } catch {}
          }
          window.open(`https://wa.me/?text=${encodedText}`, '_blank');
        });
        return;
      }
    }
    window.open(`https://wa.me/?text=${encodedText}`, '_blank');
  };

  const handleDownload = async (platform) => {
    const canvas = await generateImage();
    if (!canvas) return;
    const link = document.createElement('a');
    link.download = `panchang-${platform}-${new Date().toISOString().slice(0, 10)}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    if (platform === 'instagram' || platform === 'youtube') {
      setShowInstaHint(platform);
      setTimeout(() => setShowInstaHint(false), 4000);
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(pageUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {}
  };

  const buttons = [
    {
      id: 'whatsapp',
      label: 'WhatsApp',
      icon: <WhatsAppIcon />,
      color: 'bg-[#25D366] hover:bg-[#20b856] text-white',
      action: handleWhatsApp,
    },
    {
      id: 'facebook',
      label: 'Facebook',
      icon: <FacebookIcon />,
      color: 'bg-[#1877F2] hover:bg-[#1464d4] text-white',
      action: () => window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`, '_blank'),
    },
    {
      id: 'x',
      label: 'X',
      icon: <XIcon />,
      color: 'bg-black hover:bg-zinc-800 text-white',
      action: () => window.open(`https://twitter.com/intent/tweet?text=${encodedTweet}&url=${encodedUrl}`, '_blank'),
    },
    {
      id: 'instagram',
      label: 'Instagram',
      icon: <InstagramIcon />,
      color: 'bg-gradient-to-br from-[#833ab4] via-[#fd1d1d] to-[#fcb045] hover:opacity-90 text-white',
      action: () => handleDownload('instagram'),
    },
    {
      id: 'youtube',
      label: 'YouTube',
      icon: <YouTubeIcon />,
      color: 'bg-[#FF0000] hover:bg-[#cc0000] text-white',
      action: () => handleDownload('youtube'),
    },
    {
      id: 'download',
      label: 'Save',
      icon: <DownloadIcon />,
      color: 'bg-gold/20 hover:bg-gold/30 text-gold border border-gold/30',
      action: () => handleDownload('panchang'),
    },
    {
      id: 'copy',
      label: copied ? 'Copied!' : 'Copy',
      icon: <CopyIcon />,
      color: copied
        ? 'bg-emerald-500/20 text-emerald-500 border border-emerald-500/30'
        : 'bg-muted hover:bg-muted/80 text-muted-foreground border border-border',
      action: handleCopy,
    },
  ];

  return (
    <div className="space-y-3">
      <p className="text-xs font-semibold uppercase tracking-widest text-gold">Share</p>
      <div className="flex flex-wrap gap-2">
        {buttons.map(btn => (
          <button
            key={btn.id}
            onClick={btn.action}
            disabled={generating}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all ${btn.color} ${generating ? 'opacity-60 cursor-wait' : ''}`}
          >
            {btn.icon}
            {btn.label}
          </button>
        ))}
      </div>
      {showInstaHint === 'instagram' && (
        <p className="text-xs text-muted-foreground bg-muted/50 rounded-lg px-3 py-2">
          📸 Card saved! Open Instagram → Create post → select the downloaded image.
        </p>
      )}
      {showInstaHint === 'youtube' && (
        <p className="text-xs text-muted-foreground bg-muted/50 rounded-lg px-3 py-2">
          ▶ Card saved! Use in YouTube Community post or as a Shorts thumbnail.
        </p>
      )}
    </div>
  );
}
