import React from 'react';
import StrategistThemeProvider from '../../components/strategist/StrategistThemeProvider';
import '../../styles/strategist-tokens.css';

export default function StrategistMaintenancePage() {
  return (
    <StrategistThemeProvider>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '80vh',
        gap: '1.25rem',
        padding: '2rem',
        textAlign: 'center',
      }}>
        <span style={{
          fontFamily: '"Cinzel", serif',
          fontSize: '1.5rem',
          color: 'var(--strategist-gold)',
          letterSpacing: '0.12em',
        }}>
          ◆ THE STRATEGIST
        </span>
        <p style={{
          fontFamily: '"Cinzel", serif',
          fontSize: '0.85rem',
          letterSpacing: '0.1em',
          color: 'var(--strategist-fg-mute, #8a7d65)',
          maxWidth: '320px',
          lineHeight: 1.7,
        }}>
          Upgrading your war room.
          <br />
          Back shortly.
        </p>
      </div>
    </StrategistThemeProvider>
  );
}
