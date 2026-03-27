import React, { useRef, useState } from 'react';
import html2canvas from 'html2canvas';

// ─── Platform icons (inline SVG) ─────────────────────────────────────────────

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

// ─── Shared image generation utility ─────────────────────────────────────────

async function captureCard(cardRef) {
  if (!cardRef?.current) return null;
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
  }
}

function downloadCanvas(canvas, filename) {
  const link = document.createElement('a');
  link.download = filename;
  link.href = canvas.toDataURL('image/png');
  link.click();
}

// ─── Panchang Share Card ──────────────────────────────────────────────────────

export function PanchangShareCard({ data, cardRef }) {
  if (!data) return null;
  const { summary, panchang, special_yogas, observances } = data;
  const yoga = special_yogas?.[0];
  const obs = observances?.[0];
  const dateStr = data.date
    ? new Date(data.date + 'T00:00:00').toLocaleDateString('en-IN', {
        weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
      })
    : '';

  // Decorative corner SVG path helper
  const corner = (flip) => (
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none"
      style={{ position: 'absolute', ...flip }}
    >
      <path d="M2 38 L2 8 Q2 2 8 2 L38 2" stroke="#C5A059" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
      <circle cx="2" cy="38" r="2" fill="#C5A059" opacity="0.6"/>
      <circle cx="38" cy="2" r="2" fill="#C5A059" opacity="0.6"/>
    </svg>
  );

  return (
    <div
      ref={cardRef}
      style={{
        width: 600,
        background: 'linear-gradient(160deg, #0e0c18 0%, #1b1530 60%, #0e0c18 100%)',
        borderRadius: 16,
        padding: 40,
        fontFamily: "'Georgia', 'Times New Roman', serif",
        color: '#f5f0e8',
        position: 'absolute',
        left: -9999,
        top: -9999,
        boxSizing: 'border-box',
        border: '1px solid rgba(197,160,89,0.25)',
      }}
    >
      {/* Corner decorations */}
      <div style={{ position: 'absolute', top: 10, left: 10 }}>{corner({ top: 0, left: 0 })}</div>
      <div style={{ position: 'absolute', top: 10, right: 10, transform: 'scaleX(-1)' }}>{corner({ top: 0, left: 0 })}</div>
      <div style={{ position: 'absolute', bottom: 10, left: 10, transform: 'scaleY(-1)' }}>{corner({ top: 0, left: 0 })}</div>
      <div style={{ position: 'absolute', bottom: 10, right: 10, transform: 'scale(-1)' }}>{corner({ top: 0, left: 0 })}</div>

      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: 24 }}>
        <p style={{ color: '#C5A059', fontSize: 10, letterSpacing: 4, textTransform: 'uppercase', margin: '0 0 6px' }}>
          ✦ EverydayHoroscope.in ✦
        </p>
        <p style={{ color: '#f5f0e8', fontSize: 26, fontWeight: 700, margin: '0 0 4px', letterSpacing: 0.5 }}>
          Vedic Panchang
        </p>
        <p style={{ color: '#C5A059', fontSize: 13, margin: 0 }}>{dateStr}</p>
        <p style={{ color: 'rgba(245,240,232,0.45)', fontSize: 11, margin: '3px 0 0' }}>
          {data.location?.label}{data.location?.country ? `, ${data.location.country}` : ''}
        </p>
      </div>

      {/* Divider */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 22 }}>
        <div style={{ flex: 1, height: 1, background: 'rgba(197,160,89,0.3)' }} />
        <span style={{ color: '#C5A059', fontSize: 14 }}>☀</span>
        <div style={{ flex: 1, height: 1, background: 'rgba(197,160,89,0.3)' }} />
      </div>

      {/* Sun/Moon row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 10, marginBottom: 22 }}>
        {[
          { label: 'Sunrise',  value: summary?.sunrise,  icon: '☀' },
          { label: 'Sunset',   value: summary?.sunset,   icon: '🌅' },
          { label: 'Moonrise', value: summary?.moonrise || '—', icon: '🌙' },
          { label: 'Moonset',  value: summary?.moonset  || '—', icon: '🌑' },
        ].map(({ label, value, icon }) => (
          <div key={label} style={{
            background: 'rgba(197,160,89,0.06)',
            border: '1px solid rgba(197,160,89,0.18)',
            borderRadius: 10,
            padding: '9px 8px',
            textAlign: 'center',
          }}>
            <p style={{ fontSize: 16, margin: '0 0 3px' }}>{icon}</p>
            <p style={{ color: 'rgba(245,240,232,0.5)', fontSize: 9, letterSpacing: 1, textTransform: 'uppercase', margin: '0 0 3px' }}>{label}</p>
            <p style={{ color: '#f5f0e8', fontSize: 13, fontWeight: 600, margin: 0, fontFamily: 'monospace' }}>{value || '—'}</p>
          </div>
        ))}
      </div>

      {/* Five Limbs */}
      <div style={{ marginBottom: 18 }}>
        <p style={{ color: '#C5A059', fontSize: 9, letterSpacing: 3, textTransform: 'uppercase', margin: '0 0 10px', textAlign: 'center' }}>
          Pancha Anga — Five Limbs
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10 }}>
          {[
            { label: 'Tithi',     value: panchang?.tithi?.name },
            { label: 'Nakshatra', value: panchang?.nakshatra?.name },
            { label: 'Yoga',      value: panchang?.yoga?.name },
            { label: 'Karana',    value: panchang?.karana?.name },
            { label: 'Vara',      value: summary?.weekday },
            { label: 'Paksha',    value: summary?.paksha },
          ].map(({ label, value }) => (
            <div key={label} style={{
              background: 'rgba(255,255,255,0.04)',
              borderRadius: 8,
              padding: '8px 12px',
              borderLeft: '2px solid rgba(197,160,89,0.4)',
            }}>
              <p style={{ color: '#C5A059', fontSize: 9, letterSpacing: 1.5, textTransform: 'uppercase', margin: '0 0 3px' }}>{label}</p>
              <p style={{ color: '#f5f0e8', fontSize: 13, fontWeight: 600, margin: 0 }}>{value || '—'}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Special Yoga */}
      {yoga && (
        <div style={{
          background: yoga.quality === 'good' ? 'rgba(52,211,153,0.08)' : 'rgba(251,191,36,0.08)',
          border: `1px solid ${yoga.quality === 'good' ? 'rgba(52,211,153,0.35)' : 'rgba(251,191,36,0.35)'}`,
          borderRadius: 10,
          padding: '10px 14px',
          marginBottom: 14,
          display: 'flex',
          alignItems: 'flex-start',
          gap: 10,
        }}>
          <div style={{
            background: yoga.quality === 'good' ? 'rgba(52,211,153,0.2)' : 'rgba(251,191,36,0.2)',
            borderRadius: 6,
            padding: '4px 8px',
            flexShrink: 0,
          }}>
            <p style={{ color: yoga.quality === 'good' ? '#34d399' : '#fbbf24', fontSize: 10, fontWeight: 700, margin: 0, letterSpacing: 0.5 }}>
              {yoga.quality === 'good' ? '✦ AUSPICIOUS' : '◆ SPECIAL'}
            </p>
          </div>
          <div>
            <p style={{ color: '#f5f0e8', fontSize: 13, fontWeight: 700, margin: '0 0 2px' }}>{yoga.name}</p>
            <p style={{ color: 'rgba(245,240,232,0.6)', fontSize: 11, margin: 0 }}>
              {yoga.meaning?.split('—')[0]?.trim()}
            </p>
          </div>
        </div>
      )}

      {/* Observance */}
      {obs && (
        <div style={{
          background: 'rgba(197,160,89,0.07)',
          border: '1px solid rgba(197,160,89,0.25)',
          borderRadius: 10,
          padding: '9px 14px',
          marginBottom: 14,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
        }}>
          <span style={{ fontSize: 16 }}>🪔</span>
          <div>
            <p style={{ color: '#C5A059', fontSize: 9, letterSpacing: 2, textTransform: 'uppercase', margin: '0 0 2px' }}>Today's Observance</p>
            <p style={{ color: '#f5f0e8', fontSize: 13, fontWeight: 600, margin: 0 }}>{obs.name}</p>
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={{
        marginTop: 18,
        paddingTop: 14,
        borderTop: '1px solid rgba(197,160,89,0.2)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <p style={{ color: 'rgba(245,240,232,0.35)', fontSize: 10, margin: 0 }}>India's Premium Vedic Astrology Platform</p>
        <p style={{ color: '#C5A059', fontSize: 11, margin: 0, letterSpacing: 1.5, fontWeight: 700 }}>everydayhoroscope.in</p>
      </div>
    </div>
  );
}

// ─── Horoscope Share Card ─────────────────────────────────────────────────────

// Extract a snippet from horoscope content (first 2 sentences of overview)
function extractOverview(content) {
  if (!content) return '';
  const cleaned = content
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/#{1,6}\s?/g, '')
    .replace(/^([A-Za-z]+)\s*[—\-]+\s*/s, '')
    .trim();
  // Take text before first section heading
  const cutIdx = cleaned.search(/(Love\s*[&and]+\s*Relationships|Career\s*[&and]+\s*Finances|Health\s*[&and]+\s*Wellness|Lucky\s*Elements?)\s*:/i);
  const overview = cutIdx > 0 ? cleaned.substring(0, cutIdx).trim() : cleaned;
  // Max 2 sentences
  const sentences = overview.match(/[^.!?]+[.!?]+/g) || [];
  return sentences.slice(0, 2).join(' ').trim() || overview.substring(0, 200);
}

function extractLucky(content) {
  if (!content) return null;
  const match = content.match(/Lucky\s*Elements?\s*:([\s\S]*?)(?:\n\n|$)/i);
  if (!match) return null;
  return match[1].trim().substring(0, 120);
}

const ELEMENT_COLORS = {
  Fire:  { bg: 'rgba(239,68,68,0.08)',  border: 'rgba(239,68,68,0.35)',  accent: '#f87171' },
  Earth: { bg: 'rgba(34,197,94,0.08)',  border: 'rgba(34,197,94,0.35)',  accent: '#4ade80' },
  Air:   { bg: 'rgba(99,102,241,0.08)', border: 'rgba(99,102,241,0.35)', accent: '#818cf8' },
  Water: { bg: 'rgba(56,189,248,0.08)', border: 'rgba(56,189,248,0.35)', accent: '#38bdf8' },
};

export function HoroscopeShareCard({ cardRef, signName, signSymbol, signDates, signElement, horoscopeType, content }) {
  if (!signName) return null;

  const overview = extractOverview(content);
  const lucky    = extractLucky(content);
  const elColor  = ELEMENT_COLORS[signElement] || ELEMENT_COLORS.Fire;
  const today    = new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  const typeLabel = horoscopeType === 'weekly' ? 'Weekly' : horoscopeType === 'monthly' ? 'Monthly' : 'Daily';

  return (
    <div
      ref={cardRef}
      style={{
        width: 600,
        background: 'linear-gradient(160deg, #0e0c18 0%, #1b1530 60%, #0e0c18 100%)',
        borderRadius: 16,
        padding: 40,
        fontFamily: "'Georgia', 'Times New Roman', serif",
        color: '#f5f0e8',
        position: 'absolute',
        left: -9999,
        top: -9999,
        boxSizing: 'border-box',
        border: '1px solid rgba(197,160,89,0.25)',
      }}
    >
      {/* Decorative top line */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 26 }}>
        <div style={{ flex: 1, height: 1, background: 'rgba(197,160,89,0.3)' }} />
        <span style={{ color: '#C5A059', fontSize: 10, letterSpacing: 3, textTransform: 'uppercase' }}>EverydayHoroscope.in</span>
        <div style={{ flex: 1, height: 1, background: 'rgba(197,160,89,0.3)' }} />
      </div>

      {/* Sign header */}
      <div style={{ textAlign: 'center', marginBottom: 24 }}>
        <div style={{
          display: 'inline-block',
          width: 72,
          height: 72,
          borderRadius: '50%',
          background: elColor.bg,
          border: `2px solid ${elColor.border}`,
          lineHeight: '72px',
          fontSize: 36,
          marginBottom: 14,
          textAlign: 'center',
        }}>
          {signSymbol}
        </div>
        <p style={{ color: '#f5f0e8', fontSize: 30, fontWeight: 700, margin: '0 0 4px', letterSpacing: 0.5 }}>{signName}</p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: 16, marginTop: 6 }}>
          <span style={{ color: 'rgba(245,240,232,0.45)', fontSize: 11 }}>{signDates}</span>
          <span style={{ color: elColor.accent, fontSize: 11, fontWeight: 600 }}>{signElement}</span>
        </div>
      </div>

      {/* Type + date badge */}
      <div style={{
        background: 'rgba(197,160,89,0.1)',
        border: '1px solid rgba(197,160,89,0.3)',
        borderRadius: 8,
        padding: '7px 16px',
        textAlign: 'center',
        marginBottom: 22,
        display: 'inline-block',
        width: '100%',
        boxSizing: 'border-box',
      }}>
        <p style={{ color: '#C5A059', fontSize: 11, letterSpacing: 2, textTransform: 'uppercase', margin: '0 0 2px', fontWeight: 700 }}>
          {typeLabel} Horoscope
        </p>
        <p style={{ color: 'rgba(245,240,232,0.55)', fontSize: 10, margin: 0 }}>{today}</p>
      </div>

      {/* Overview */}
      {overview && (
        <div style={{
          background: 'rgba(255,255,255,0.04)',
          borderRadius: 10,
          padding: '14px 18px',
          marginBottom: 18,
          borderLeft: `3px solid ${elColor.accent}`,
        }}>
          <p style={{ color: 'rgba(245,240,232,0.85)', fontSize: 14, lineHeight: 1.65, margin: 0 }}>
            {overview}
          </p>
        </div>
      )}

      {/* Lucky elements */}
      {lucky && (
        <div style={{
          background: 'rgba(197,160,89,0.06)',
          border: '1px solid rgba(197,160,89,0.25)',
          borderRadius: 10,
          padding: '11px 16px',
          marginBottom: 14,
        }}>
          <p style={{ color: '#C5A059', fontSize: 9, letterSpacing: 2.5, textTransform: 'uppercase', margin: '0 0 6px', fontWeight: 700 }}>
            ✦ Lucky Elements
          </p>
          <p style={{ color: 'rgba(245,240,232,0.75)', fontSize: 12, lineHeight: 1.55, margin: 0 }}>{lucky}</p>
        </div>
      )}

      {/* Footer */}
      <div style={{
        marginTop: 20,
        paddingTop: 14,
        borderTop: '1px solid rgba(197,160,89,0.2)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <p style={{ color: 'rgba(245,240,232,0.35)', fontSize: 10, margin: 0 }}>India's Premium Vedic Astrology Platform</p>
        <p style={{ color: '#C5A059', fontSize: 11, margin: 0, letterSpacing: 1.5, fontWeight: 700 }}>everydayhoroscope.in</p>
      </div>
    </div>
  );
}

// ─── Generic share buttons (used for both Panchang and Horoscope) ─────────────

export function ShareButtons({ pageUrl, shareText, cardRef, filename = 'share-card' }) {
  const [copied, setCopied]           = useState(false);
  const [generating, setGenerating]   = useState(false);
  const [hint, setHint]               = useState(null); // { platform, message }

  const encodedUrl   = encodeURIComponent(pageUrl);
  const encodedText  = encodeURIComponent(shareText + '\n' + pageUrl);
  const encodedTweet = encodeURIComponent(shareText);

  const getCanvas = async () => {
    setGenerating(true);
    const canvas = await captureCard(cardRef);
    setGenerating(false);
    return canvas;
  };

  const handleWhatsApp = async () => {
    // Always download card first so user has the image ready, then open wa.me
    const canvas = await getCanvas();
    if (canvas) {
      downloadCanvas(canvas, `${filename}-${new Date().toISOString().slice(0, 10)}.png`);
    }
    // Open WhatsApp link simultaneously (slight delay so download triggers first)
    setTimeout(() => {
      window.open(`https://wa.me/?text=${encodedText}`, '_blank');
    }, 300);
    setHint({ platform: 'whatsapp', message: '📲 Card saved to your device — open WhatsApp, tap the attachment icon, and select the downloaded image.' });
    setTimeout(() => setHint(null), 6000);
  };

  const handleFacebook = async () => {
    // Download card + open Facebook sharer
    const canvas = await getCanvas();
    if (canvas) downloadCanvas(canvas, `${filename}-facebook-${new Date().toISOString().slice(0, 10)}.png`);
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`, '_blank');
    setHint({ platform: 'facebook', message: '📷 Card downloaded — upload it as a photo when posting on Facebook.' });
    setTimeout(() => setHint(null), 6000);
  };

  const handleX = () => {
    window.open(`https://twitter.com/intent/tweet?text=${encodedTweet}&url=${encodedUrl}`, '_blank');
  };

  const handleDownload = async (platform) => {
    const canvas = await getCanvas();
    if (!canvas) return;
    downloadCanvas(canvas, `${filename}-${platform}-${new Date().toISOString().slice(0, 10)}.png`);
    const messages = {
      instagram: '📸 Card saved! Open Instagram → Create post → select the downloaded image.',
      youtube:   '▶ Card saved! Use in YouTube Community post or as a Shorts thumbnail.',
      save:      '✅ Card saved to your device.',
    };
    setHint({ platform, message: messages[platform] || messages.save });
    setTimeout(() => setHint(null), 5000);
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(pageUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {}
  };

  const buttons = [
    { id: 'whatsapp',  label: 'WhatsApp',  icon: <WhatsAppIcon />,  color: 'bg-[#25D366] hover:bg-[#20b856] text-white',                                            action: handleWhatsApp },
    { id: 'facebook',  label: 'Facebook',  icon: <FacebookIcon />,  color: 'bg-[#1877F2] hover:bg-[#1464d4] text-white',                                            action: handleFacebook },
    { id: 'x',         label: 'X',         icon: <XIcon />,         color: 'bg-black hover:bg-zinc-800 text-white',                                                  action: handleX },
    { id: 'instagram', label: 'Instagram', icon: <InstagramIcon />, color: 'bg-gradient-to-br from-[#833ab4] via-[#fd1d1d] to-[#fcb045] hover:opacity-90 text-white', action: () => handleDownload('instagram') },
    { id: 'youtube',   label: 'YouTube',   icon: <YouTubeIcon />,   color: 'bg-[#FF0000] hover:bg-[#cc0000] text-white',                                            action: () => handleDownload('youtube') },
    { id: 'save',      label: 'Save Card', icon: <DownloadIcon />,  color: 'bg-gold/20 hover:bg-gold/30 text-gold border border-gold/30',                           action: () => handleDownload('save') },
    {
      id: 'copy', label: copied ? 'Copied!' : 'Copy Link', icon: <CopyIcon />,
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
      {hint && (
        <p className="text-xs text-muted-foreground bg-muted/50 rounded-lg px-3 py-2">
          {hint.message}
        </p>
      )}
    </div>
  );
}
