import React, { useState } from 'react';
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

// ─── Shared utilities ─────────────────────────────────────────────────────────

async function captureCard(cardRef) {
  if (!cardRef?.current) return null;
  try {
    // onclone receives the cloned document and the cloned element.
    // We move only the clone into view — the real DOM element stays at left:-9999px,
    // so there is zero visible flash on screen during capture.
    return await html2canvas(cardRef.current, {
      scale: 2,
      useCORS: true,
      backgroundColor: null,
      logging: false,
      onclone: (_clonedDoc, clonedEl) => {
        clonedEl.style.left = '0px';
        clonedEl.style.top  = '0px';
      },
    });
  } catch (e) {
    console.error('html2canvas error', e);
    return null;
  }
}

function downloadCanvas(canvas, filename) {
  // iOS Safari silently ignores <a download> — use toBlob + window.open so the
  // user can long-press → "Save to Photos" / "Download".
  if (/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream) {
    canvas.toBlob((blob) => {
      if (!blob) return;
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
      setTimeout(() => URL.revokeObjectURL(url), 6000);
    }, 'image/png');
    return;
  }

  // Desktop / Android: toDataURL is synchronous so the anchor click fires
  // immediately in the same call stack — no async gap to lose gesture context.
  const url = canvas.toDataURL('image/png');
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// Try native Web Share API with an image file (works on mobile Chrome/Safari).
// Returns: 'shared' | 'aborted' | 'unsupported'
function nativeShareImage(canvas, filename, title, text) {
  return new Promise((resolve) => {
    canvas.toBlob(async (blob) => {
      if (!blob) { resolve('unsupported'); return; }
      const file = new File([blob], filename, { type: 'image/png' });
      if (!navigator.canShare?.({ files: [file] })) { resolve('unsupported'); return; }
      try {
        await navigator.share({ files: [file], title, text });
        resolve('shared');
      } catch (e) {
        resolve(e.name === 'AbortError' ? 'aborted' : 'unsupported');
      }
    }, 'image/png');
  });
}

// Format ISO datetime string → "6:18 AM" using the offset baked into the string
function fmtISO(iso) {
  if (!iso) return '—';
  // Slice HH:MM from the time portion of the ISO string (location-local time)
  const timePart = iso.slice(11, 16); // "HH:MM"
  const [hStr, mStr] = timePart.split(':');
  const h = parseInt(hStr, 10);
  const m = parseInt(mStr, 10);
  const period = h >= 12 ? 'PM' : 'AM';
  const h12 = h % 12 || 12;
  return `${h12}:${m.toString().padStart(2, '0')} ${period}`;
}

// ─── Panchang Share Card ──────────────────────────────────────────────────────

export function PanchangShareCard({ data, cardRef }) {
  if (!data) return null;
  const { summary, panchang, special_yogas, observances, day_quality_windows } = data;
  const yoga = special_yogas?.[0];
  const obs  = observances?.[0];

  const dateStr = data.date
    ? new Date(data.date + 'T00:00:00').toLocaleDateString('en-IN', {
        weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
      })
    : '';

  // Split timing windows into auspicious / inauspicious
  const auspicious   = (day_quality_windows || []).filter(w => w.quality === 'good');
  const inauspicious = (day_quality_windows || []).filter(w => w.quality !== 'good');

  // Shared table row style factory
  const tableRow = (label, start, end, accent) => (
    <div key={label} style={{
      display: 'grid', gridTemplateColumns: '1fr auto',
      padding: '7px 14px', borderBottom: `1px solid ${accent}22`,
    }}>
      <span style={{ color: '#f5f0e8', fontSize: 16, fontWeight: 500 }}>{label}</span>
      <span style={{ color: accent, fontSize: 15, fontFamily: 'monospace', fontWeight: 700 }}>
        {fmtISO(start)} – {fmtISO(end)}
      </span>
    </div>
  );

  return (
    <div
      ref={cardRef}
      style={{
        width: 900,
        background: 'linear-gradient(160deg, #0e0c18 0%, #1b1530 60%, #0e0c18 100%)',
        borderRadius: 20,
        padding: 52,
        fontFamily: "'Georgia', 'Times New Roman', serif",
        color: '#f5f0e8',
        position: 'fixed',
        left: -9999,
        top: 0,
        pointerEvents: 'none',
        boxSizing: 'border-box',
        border: '1px solid rgba(197,160,89,0.25)',
      }}
    >
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: 28 }}>
        <p style={{ color: '#C5A059', fontSize: 13, letterSpacing: 5, textTransform: 'uppercase', margin: '0 0 8px' }}>
          ✦ EverydayHoroscope.in ✦
        </p>
        <p style={{ color: '#f5f0e8', fontSize: 36, fontWeight: 700, margin: '0 0 6px', letterSpacing: 0.5 }}>
          Vedic Panchang
        </p>
        <p style={{ color: '#C5A059', fontSize: 18, margin: 0 }}>{dateStr}</p>
        <p style={{ color: 'rgba(245,240,232,0.4)', fontSize: 14, margin: '4px 0 0' }}>
          {data.location?.label}{data.location?.country ? `, ${data.location.country}` : ''}
        </p>
      </div>

      {/* Divider */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
        <div style={{ flex: 1, height: 1, background: 'rgba(197,160,89,0.3)' }} />
        <span style={{ color: '#C5A059', fontSize: 18 }}>☀</span>
        <div style={{ flex: 1, height: 1, background: 'rgba(197,160,89,0.3)' }} />
      </div>

      {/* Sun / Moon row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: 12, marginBottom: 24 }}>
        {[
          { label: 'Sunrise',  value: summary?.sunrise,          icon: '☀' },
          { label: 'Sunset',   value: summary?.sunset,           icon: '🌅' },
          { label: 'Moonrise', value: summary?.moonrise || '—',  icon: '🌙' },
          { label: 'Moonset',  value: summary?.moonset  || '—',  icon: '🌑' },
        ].map(({ label, value, icon }) => (
          <div key={label} style={{
            background: 'rgba(197,160,89,0.06)',
            border: '1px solid rgba(197,160,89,0.18)',
            borderRadius: 12, padding: '12px 10px', textAlign: 'center',
          }}>
            <p style={{ fontSize: 22, margin: '0 0 5px' }}>{icon}</p>
            <p style={{ color: 'rgba(245,240,232,0.5)', fontSize: 11, letterSpacing: 1.5, textTransform: 'uppercase', margin: '0 0 4px' }}>{label}</p>
            <p style={{ color: '#f5f0e8', fontSize: 17, fontWeight: 700, margin: 0, fontFamily: 'monospace' }}>{value || '—'}</p>
          </div>
        ))}
      </div>

      {/* Five Limbs */}
      <div style={{ marginBottom: 22 }}>
        <p style={{ color: '#C5A059', fontSize: 12, letterSpacing: 3.5, textTransform: 'uppercase', margin: '0 0 12px', textAlign: 'center' }}>
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
              background: 'rgba(255,255,255,0.04)', borderRadius: 10, padding: '10px 16px',
              borderLeft: '3px solid rgba(197,160,89,0.4)',
            }}>
              <p style={{ color: '#C5A059', fontSize: 11, letterSpacing: 2, textTransform: 'uppercase', margin: '0 0 4px' }}>{label}</p>
              <p style={{ color: '#f5f0e8', fontSize: 17, fontWeight: 700, margin: 0 }}>{value || '—'}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Timing Windows — side by side */}
      {(auspicious.length > 0 || inauspicious.length > 0) && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 20 }}>
          {/* Auspicious */}
          {auspicious.length > 0 && (
            <div style={{
              background: 'rgba(52,211,153,0.06)',
              border: '1px solid rgba(52,211,153,0.25)',
              borderRadius: 12, overflow: 'hidden',
            }}>
              <div style={{ background: 'rgba(52,211,153,0.12)', padding: '8px 14px', borderBottom: '1px solid rgba(52,211,153,0.2)' }}>
                <p style={{ color: '#34d399', fontSize: 12, fontWeight: 700, letterSpacing: 2, textTransform: 'uppercase', margin: 0 }}>
                  ✦ Auspicious
                </p>
              </div>
              {auspicious.map(w => tableRow(w.label, w.start, w.end, '#34d399'))}
            </div>
          )}
          {/* Inauspicious */}
          {inauspicious.length > 0 && (
            <div style={{
              background: 'rgba(239,68,68,0.05)',
              border: '1px solid rgba(239,68,68,0.22)',
              borderRadius: 12, overflow: 'hidden',
            }}>
              <div style={{ background: 'rgba(239,68,68,0.1)', padding: '8px 14px', borderBottom: '1px solid rgba(239,68,68,0.18)' }}>
                <p style={{ color: '#f87171', fontSize: 12, fontWeight: 700, letterSpacing: 2, textTransform: 'uppercase', margin: 0 }}>
                  ⛔ Inauspicious
                </p>
              </div>
              {inauspicious.map(w => tableRow(w.label, w.start, w.end, '#f87171'))}
            </div>
          )}
        </div>
      )}

      {/* Special Yoga */}
      {yoga && (
        <div style={{
          background: yoga.quality === 'good' ? 'rgba(52,211,153,0.08)' : 'rgba(251,191,36,0.08)',
          border: `1px solid ${yoga.quality === 'good' ? 'rgba(52,211,153,0.35)' : 'rgba(251,191,36,0.35)'}`,
          borderRadius: 12, padding: '12px 18px', marginBottom: 16,
          display: 'flex', alignItems: 'flex-start', gap: 14,
        }}>
          <div style={{
            background: yoga.quality === 'good' ? 'rgba(52,211,153,0.2)' : 'rgba(251,191,36,0.2)',
            borderRadius: 8, padding: '5px 12px', flexShrink: 0,
          }}>
            <p style={{ color: yoga.quality === 'good' ? '#34d399' : '#fbbf24', fontSize: 11, fontWeight: 700, margin: 0, letterSpacing: 0.5 }}>
              {yoga.quality === 'good' ? '✦ AUSPICIOUS' : '◆ SPECIAL'}
            </p>
          </div>
          <div>
            <p style={{ color: '#f5f0e8', fontSize: 18, fontWeight: 700, margin: '0 0 3px' }}>{yoga.name}</p>
            <p style={{ color: 'rgba(245,240,232,0.6)', fontSize: 14, margin: 0 }}>
              {yoga.meaning?.split('—')[0]?.trim()}
            </p>
          </div>
        </div>
      )}

      {/* Observance */}
      {obs && (
        <div style={{
          background: 'rgba(197,160,89,0.07)', border: '1px solid rgba(197,160,89,0.25)',
          borderRadius: 12, padding: '11px 18px', marginBottom: 16,
          display: 'flex', alignItems: 'center', gap: 14,
        }}>
          <span style={{ fontSize: 20 }}>🪔</span>
          <div>
            <p style={{ color: '#C5A059', fontSize: 11, letterSpacing: 2.5, textTransform: 'uppercase', margin: '0 0 3px' }}>Today's Observance</p>
            <p style={{ color: '#f5f0e8', fontSize: 18, fontWeight: 700, margin: 0 }}>{obs.name}</p>
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={{
        marginTop: 18, paddingTop: 16, borderTop: '1px solid rgba(197,160,89,0.2)',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      }}>
        <p style={{ color: 'rgba(245,240,232,0.35)', fontSize: 13, margin: 0 }}>India's Premium Vedic Astrology Platform</p>
        <p style={{ color: '#C5A059', fontSize: 15, margin: 0, letterSpacing: 1.5, fontWeight: 700 }}>everydayhoroscope.in</p>
      </div>
    </div>
  );
}

// ─── Horoscope Share Card ─────────────────────────────────────────────────────

function extractOverview(content) {
  if (!content) return '';
  const cleaned = content
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/#{1,6}\s?/g, '')
    .replace(/^([A-Za-z]+)\s*[—\-]+\s*/s, '')
    .trim();
  const cutIdx = cleaned.search(/(Love\s*[&and]+\s*Relationships|Career\s*[&and]+\s*Finances|Health\s*[&and]+\s*Wellness|Lucky\s*Elements?)\s*:/i);
  const overview = cutIdx > 0 ? cleaned.substring(0, cutIdx).trim() : cleaned;
  const sentences = overview.match(/[^.!?]+[.!?]+/g) || [];
  return sentences.slice(0, 2).join(' ').trim() || overview.substring(0, 200);
}

function extractLucky(content) {
  if (!content) return null;
  const match = content.match(/Lucky\s*Elements?\s*:([\s\S]*?)(?:\n\n|$)/i);
  return match ? match[1].trim().substring(0, 130) : null;
}

const ELEMENT_COLORS = {
  Fire:  { bg: 'rgba(239,68,68,0.08)',  border: 'rgba(239,68,68,0.35)',  accent: '#f87171' },
  Earth: { bg: 'rgba(34,197,94,0.08)',  border: 'rgba(34,197,94,0.35)',  accent: '#4ade80' },
  Air:   { bg: 'rgba(99,102,241,0.08)', border: 'rgba(99,102,241,0.35)', accent: '#818cf8' },
  Water: { bg: 'rgba(56,189,248,0.08)', border: 'rgba(56,189,248,0.35)', accent: '#38bdf8' },
};

export function HoroscopeShareCard({ cardRef, signName, signSymbol, signDates, signElement, horoscopeType, content }) {
  if (!signName) return null;
  const overview  = extractOverview(content);
  const lucky     = extractLucky(content);
  const elColor   = ELEMENT_COLORS[signElement] || ELEMENT_COLORS.Fire;
  const today     = new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  const typeLabel = horoscopeType === 'weekly' ? 'Weekly' : horoscopeType === 'monthly' ? 'Monthly' : 'Daily';

  return (
    <div
      ref={cardRef}
      style={{
        width: 900,
        background: 'linear-gradient(160deg, #0e0c18 0%, #1b1530 60%, #0e0c18 100%)',
        borderRadius: 20, padding: 56,
        fontFamily: "'Georgia', 'Times New Roman', serif",
        color: '#f5f0e8',
        position: 'fixed', left: -9999, top: 0,
        pointerEvents: 'none',
        boxSizing: 'border-box',
        border: '1px solid rgba(197,160,89,0.25)',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 34 }}>
        <div style={{ flex: 1, height: 1, background: 'rgba(197,160,89,0.3)' }} />
        <span style={{ color: '#C5A059', fontSize: 13, letterSpacing: 4, textTransform: 'uppercase' }}>EverydayHoroscope.in</span>
        <div style={{ flex: 1, height: 1, background: 'rgba(197,160,89,0.3)' }} />
      </div>

      <div style={{ textAlign: 'center', marginBottom: 28 }}>
        <div style={{
          display: 'inline-block', width: 100, height: 100, borderRadius: '50%',
          background: elColor.bg, border: `2px solid ${elColor.border}`,
          lineHeight: '100px', fontSize: 50, marginBottom: 18, textAlign: 'center',
        }}>
          {signSymbol}
        </div>
        <p style={{ color: '#f5f0e8', fontSize: 42, fontWeight: 700, margin: '0 0 8px' }}>{signName}</p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: 20 }}>
          <span style={{ color: 'rgba(245,240,232,0.45)', fontSize: 15 }}>{signDates}</span>
          <span style={{ color: elColor.accent, fontSize: 15, fontWeight: 600 }}>{signElement}</span>
        </div>
      </div>

      <div style={{
        background: 'rgba(197,160,89,0.1)', border: '1px solid rgba(197,160,89,0.3)',
        borderRadius: 10, padding: '10px 20px', textAlign: 'center', marginBottom: 26,
        boxSizing: 'border-box',
      }}>
        <p style={{ color: '#C5A059', fontSize: 14, letterSpacing: 2.5, textTransform: 'uppercase', margin: '0 0 3px', fontWeight: 700 }}>
          {typeLabel} Horoscope
        </p>
        <p style={{ color: 'rgba(245,240,232,0.55)', fontSize: 13, margin: 0 }}>{today}</p>
      </div>

      {overview && (
        <div style={{
          background: 'rgba(255,255,255,0.04)', borderRadius: 12,
          padding: '18px 22px', marginBottom: 20, borderLeft: `4px solid ${elColor.accent}`,
        }}>
          <p style={{ color: 'rgba(245,240,232,0.88)', fontSize: 18, lineHeight: 1.7, margin: 0 }}>{overview}</p>
        </div>
      )}

      {lucky && (
        <div style={{
          background: 'rgba(197,160,89,0.06)', border: '1px solid rgba(197,160,89,0.25)',
          borderRadius: 12, padding: '14px 20px', marginBottom: 18,
        }}>
          <p style={{ color: '#C5A059', fontSize: 12, letterSpacing: 3, textTransform: 'uppercase', margin: '0 0 8px', fontWeight: 700 }}>
            ✦ Lucky Elements
          </p>
          <p style={{ color: 'rgba(245,240,232,0.75)', fontSize: 16, lineHeight: 1.6, margin: 0 }}>{lucky}</p>
        </div>
      )}

      <div style={{
        marginTop: 22, paddingTop: 18, borderTop: '1px solid rgba(197,160,89,0.2)',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      }}>
        <p style={{ color: 'rgba(245,240,232,0.35)', fontSize: 13, margin: 0 }}>India's Premium Vedic Astrology Platform</p>
        <p style={{ color: '#C5A059', fontSize: 15, margin: 0, letterSpacing: 1.5, fontWeight: 700 }}>everydayhoroscope.in</p>
      </div>
    </div>
  );
}

// ─── Share Buttons ────────────────────────────────────────────────────────────

export function ShareButtons({ pageUrl, shareText, cardRef, filename = 'share-card', fbPageCaption = null }) {
  const [copied, setCopied]           = useState(false);
  const [generating, setGenerating]   = useState(false);
  const [hint, setHint]               = useState(null);
  const [fbPosting, setFbPosting]     = useState(false);

  const cardFilename  = `${filename}-${new Date().toISOString().slice(0, 10)}.png`;
  const encodedUrl    = encodeURIComponent(pageUrl);
  const encodedText   = encodeURIComponent(shareText + '\n' + pageUrl);
  const encodedTweet  = encodeURIComponent(shareText);

  const showHint = (message, duration = 7000) => {
    setHint(message);
    setTimeout(() => setHint(null), duration);
  };

  const getCanvas = async () => {
    setGenerating(true);
    const canvas = await captureCard(cardRef);
    setGenerating(false);
    if (!canvas) {
      showHint('⚠️ Could not generate card image. Please try again.', 5000);
    }
    return canvas;
  };

  // ── WhatsApp: native file share on mobile, download + wa.me on desktop ──────
  const handleWhatsApp = async () => {
    const canvas = await getCanvas();
    if (!canvas) {
      window.open(`https://wa.me/?text=${encodedText}`, '_blank');
      return;
    }
    // On mobile, try native share sheet (Android/iOS WhatsApp can receive the file directly).
    // Skip this on desktop — nativeShareImage adds extra async overhead and the
    // Windows/macOS share sheet doesn't reliably send images to WhatsApp anyway.
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    if (isMobile) {
      const result = await nativeShareImage(canvas, cardFilename, shareText, shareText + '\n' + pageUrl);
      if (result === 'shared' || result === 'aborted') return;
    }
    // Desktop (or mobile fallback): download card, then open wa.me
    downloadCanvas(canvas, cardFilename);
    setTimeout(() => window.open(`https://wa.me/?text=${encodedText}`, '_blank'), 400);
    showHint('📲 Card saved! Open WhatsApp → tap the 📎 attach icon → select the downloaded image to share it.');
  };

  // ── Facebook: try native share first (mobile), else download + sharer ──────
  const handleFacebook = async () => {
    const canvas = await getCanvas();
    if (canvas) {
      const result = await nativeShareImage(canvas, cardFilename, shareText, pageUrl);
      if (result === 'shared' || result === 'aborted') return;
      downloadCanvas(canvas, cardFilename);
    }
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`, '_blank');
    showHint('📷 Card downloaded — create a new Facebook post and upload the image directly for best results.');
  };

  // ── X/Twitter: share URL (no image API without auth) ─────────────────────
  const handleX = () => {
    window.open(`https://twitter.com/intent/tweet?text=${encodedTweet}&url=${encodedUrl}`, '_blank');
  };

  // ── Instagram / YouTube / Save — always download directly, no share sheet ──
  const handleDownload = async (platform) => {
    const canvas = await getCanvas();
    if (!canvas) return;
    // Download straight to device — never open native share sheet here,
    // as dismissing it would skip the download entirely.
    downloadCanvas(canvas, cardFilename);
    const messages = {
      instagram: '📸 Card saved! Open Instagram → tap + → Post → select the downloaded image.',
      youtube:   '▶ Card saved! Use in YouTube Community post or as a Shorts thumbnail.',
    };
    showHint(messages[platform] || '✅ Card saved to your device.');
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(pageUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {}
  };

  // ── Post card image directly to Facebook Page (admin only) ──────────────────
  const handlePostToFBPage = async () => {
    const canvas = await getCanvas();
    if (!canvas) return;
    setFbPosting(true);
    setHint(null);
    try {
      await new Promise((resolve, reject) => {
        canvas.toBlob(async (blob) => {
          if (!blob) { reject(new Error('Failed to generate image')); return; }
          const formData = new FormData();
          formData.append('image', blob, cardFilename);
          formData.append('message', fbPageCaption || shareText);
          formData.append('channels', 'facebook');
          const API = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
          const adminToken = localStorage.getItem('admin_token');
          const res = await fetch(`${API}/api/admin/social/post-image`, {
            method: 'POST',
            body: formData,
            credentials: 'include',
            headers: adminToken ? { Authorization: `Bearer ${adminToken}` } : {},
          });
          if (!res.ok) {
            const err = await res.json().catch(() => ({}));
            reject(new Error(err.detail || `Server error ${res.status}`));
            return;
          }
          const data = await res.json();
          const result = data.results?.[0];
          if (result?.success) {
            resolve(result.post_id);
          } else {
            reject(new Error(result?.error || 'Post failed'));
          }
        }, 'image/png');
      });
      showHint('✅ Posted to EverydayHoroscope Facebook Page successfully!', 6000);
    } catch (e) {
      const msg = e.message || 'Unknown error';
      if (msg.includes('401') || msg.includes('authenticated')) {
        showHint('🔒 Admin login required — go to /admin to sign in first.', 7000);
      } else {
        showHint(`❌ Facebook post failed: ${msg}`, 7000);
      }
    } finally {
      setFbPosting(false);
    }
  };

  const buttons = [
    { id: 'whatsapp',  label: 'WhatsApp',  icon: <WhatsAppIcon />,  color: 'bg-[#25D366] hover:bg-[#20b856] text-white',                                             action: handleWhatsApp },
    { id: 'facebook',  label: 'Facebook',  icon: <FacebookIcon />,  color: 'bg-[#1877F2] hover:bg-[#1464d4] text-white',                                             action: handleFacebook },
    { id: 'x',         label: 'X',         icon: <XIcon />,         color: 'bg-black hover:bg-zinc-800 text-white',                                                   action: handleX },
    { id: 'instagram', label: 'Instagram', icon: <InstagramIcon />, color: 'bg-gradient-to-br from-[#833ab4] via-[#fd1d1d] to-[#fcb045] hover:opacity-90 text-white', action: () => handleDownload('instagram') },
    { id: 'youtube',   label: 'YouTube',   icon: <YouTubeIcon />,   color: 'bg-[#FF0000] hover:bg-[#cc0000] text-white',                                             action: () => handleDownload('youtube') },
    { id: 'save',      label: 'Save Card', icon: <DownloadIcon />,  color: 'bg-gold/20 hover:bg-gold/30 text-gold border border-gold/30',                            action: () => handleDownload('save') },
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
        {fbPageCaption !== null && (
          <button
            onClick={handlePostToFBPage}
            disabled={generating || fbPosting}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all bg-[#1877F2] hover:bg-[#1464d4] text-white ${(generating || fbPosting) ? 'opacity-60 cursor-wait' : ''}`}
          >
            <FacebookIcon />
            {fbPosting ? 'Posting…' : 'Post to Page'}
          </button>
        )}
      </div>
      {hint && (
        <p className="text-xs text-muted-foreground bg-muted/50 rounded-lg px-3 py-2.5 leading-relaxed">
          {hint}
        </p>
      )}
    </div>
  );
}
