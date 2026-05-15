import React, { forwardRef } from 'react';

const VERDICT_THEME = {
  YES: {
    badgeBg: '#c5a059',
    badgeText: '#20150a',
  },
  WAIT: {
    badgeBg: '#315f9f',
    badgeText: '#f8fafc',
  },
  NO: {
    badgeBg: '#a93f3f',
    badgeText: '#fff7ed',
  },
  PRAY: {
    badgeBg: '#6d47a7',
    badgeText: '#faf5ff',
  },
};

const truncateLine = (value = '', limit = 150) =>
  value.length > limit ? `${value.slice(0, limit).trim()}...` : value;

export const KrishnaShareCard = forwardRef(function KrishnaShareCard({ reading }, ref) {
  if (!reading) return null;

  const theme = VERDICT_THEME[reading.verdict_display] || VERDICT_THEME.WAIT;
  const actionLine = truncateLine(
    (reading.what_to_do?.english_block || reading.krishna_message?.english_block || '')
      .split('. ')
      .filter(Boolean)[0] || ''
  );

  return (
    <div
      ref={ref}
      style={{
        width: 900,
        minHeight: 520,
        position: 'fixed',
        left: -9999,
        top: 0,
        pointerEvents: 'none',
        background: 'linear-gradient(160deg, #13111d 0%, #19162a 55%, #0f0e18 100%)',
        color: '#f5efe3',
        borderRadius: 28,
        border: '1px solid rgba(197,160,89,0.22)',
        overflow: 'hidden',
        boxSizing: 'border-box',
        fontFamily: "'Playfair Display', Georgia, serif",
        boxShadow: '0 28px 80px rgba(0,0,0,0.28)',
      }}
    >
      <div style={{ background: 'linear-gradient(90deg, #0d1323 0%, #151b2b 100%)', padding: '28px 40px 24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16 }}>
          <div>
            <p style={{ margin: 0, fontSize: 12, letterSpacing: 4, textTransform: 'uppercase', color: '#c5a059', fontWeight: 700 }}>
              EverydayHoroscope
            </p>
            <p style={{ margin: '10px 0 0', fontSize: 34, fontWeight: 700, color: '#f8f2e8' }}>
              Krishna Prashnavali
            </p>
          </div>
          <div style={{ width: 120, height: 1, background: 'linear-gradient(90deg, rgba(197,160,89,0.0), rgba(197,160,89,0.9), rgba(197,160,89,0.0))' }} />
        </div>
      </div>

      <div style={{ padding: '28px 44px 34px' }}>
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            minWidth: 140,
            padding: '12px 28px',
            borderRadius: 999,
            background: theme.badgeBg,
            color: theme.badgeText,
            fontSize: 24,
            fontWeight: 700,
            letterSpacing: 1.2,
            margin: '0 auto 22px',
          }}
        >
          {reading.verdict_display}
        </div>

        <p style={{ margin: '0 auto 16px', textAlign: 'center', fontSize: 28, lineHeight: 1.45, color: '#f8f2e8', maxWidth: 720 }}>
          {reading.chaupai_phrase}
        </p>

        <p style={{ margin: '0 auto 24px', textAlign: 'center', fontSize: 20, lineHeight: 1.4, color: '#d8c4a0', maxWidth: 700, fontWeight: 600 }}>
          {reading.title?.english_block}
        </p>

        <div
          style={{
            borderTop: '1px solid rgba(197,160,89,0.22)',
            borderBottom: '1px solid rgba(197,160,89,0.22)',
            padding: '24px 12px',
            marginBottom: 24,
          }}
        >
          <p
            style={{
              margin: 0,
              textAlign: 'center',
              fontSize: 24,
              lineHeight: 1.5,
              color: '#f6efe3',
              fontStyle: 'italic',
              maxWidth: 740,
              marginInline: 'auto',
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
            }}
          >
            {truncateLine(reading.krishna_answer?.english_block || '', 220)}
          </p>
        </div>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            background: 'rgba(197,160,89,0.08)',
            border: '1px solid rgba(197,160,89,0.18)',
            borderRadius: 18,
            padding: '18px 20px',
            marginBottom: 28,
          }}
        >
          <span style={{ fontSize: 24 }}>🌿</span>
          <p style={{ margin: 0, fontSize: 18, lineHeight: 1.5, color: '#f0e6d5' }}>
            {actionLine || 'Act with sincerity, steadiness, and remembrance.'}
          </p>
        </div>

        <p style={{ margin: 0, textAlign: 'center', fontSize: 15, letterSpacing: 0.6, color: '#c5a059' }}>
          everydayhoroscope.in/krishna-prashnavali
        </p>
      </div>
    </div>
  );
});

export default KrishnaShareCard;
