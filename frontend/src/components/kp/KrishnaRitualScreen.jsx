import React, { useEffect, useState } from "react";

const RITUAL_DURATION_MS = 25000;
const FADE_DURATION_MS = 1500;

export default function KrishnaRitualScreen({ onComplete }) {
  const [showBreathPrompt, setShowBreathPrompt] = useState(false);
  const [showConnectionPrompt, setShowConnectionPrompt] = useState(false);
  const [dismissing, setDismissing] = useState(false);

  useEffect(() => {
    const breathTimer = window.setTimeout(() => setShowBreathPrompt(true), 5000);
    const connectionTimer = window.setTimeout(() => setShowConnectionPrompt(true), 12000);
    const completeTimer = window.setTimeout(() => {
      setDismissing(true);
      window.setTimeout(() => onComplete?.(), FADE_DURATION_MS);
    }, RITUAL_DURATION_MS);

    return () => {
      window.clearTimeout(breathTimer);
      window.clearTimeout(connectionTimer);
      window.clearTimeout(completeTimer);
    };
  }, [onComplete]);

  function handleReady() {
    if (dismissing) return;
    setDismissing(true);
    window.setTimeout(() => onComplete?.(), FADE_DURATION_MS);
  }

  return (
    <div
      className={`absolute inset-0 z-20 overflow-hidden rounded-[1.75rem] bg-neutral-950 transition-opacity ${
        dismissing ? "pointer-events-none opacity-0" : "opacity-100"
      }`}
      style={{ transitionDuration: "1500ms" }}
    >
      <style>{`
        @keyframes kpOrbExpand {
          0% { transform: scale(1); }
          100% { transform: scale(8); }
        }
        @keyframes kpOrbPulse {
          0%, 100% { opacity: 0.72; }
          50% { opacity: 1; }
        }
        @keyframes kpFadeInUp {
          from { opacity: 0; transform: translateY(16px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      <div className="flex h-full min-h-[34rem] flex-col items-center justify-center px-6 py-10 text-center">
        <div className="relative flex flex-1 items-center justify-center">
          <div
            className="absolute left-1/2 top-1/2 h-8 w-8 -translate-x-1/2 -translate-y-1/2 rounded-full bg-white/90 blur-[8px]"
            style={{
              boxShadow: "0 0 60px 20px rgba(255,255,255,0.08)",
              animation: "kpOrbExpand 8s ease-out forwards, kpOrbPulse 4s ease-in-out infinite",
            }}
          />
          <div className="relative z-10 mx-auto max-w-xl space-y-4">
            <p className="m-0 text-[11px] uppercase tracking-[0.34em] text-amber-300/80">Krishna Prashnavali</p>
            <h3 className="m-0 font-playfair text-4xl italic text-white md:text-5xl">Close your eyes.</h3>
            {showBreathPrompt ? (
              <p
                className="m-0 text-sm leading-7 text-white/60 md:text-base"
                style={{ animation: "kpFadeInUp 0.9s ease-out both" }}
              >
                Breathe in. Visualise a pure white light at your heart centre.
              </p>
            ) : null}
            {showConnectionPrompt ? (
              <p
                className="m-0 text-sm leading-7 text-white/60 md:text-base"
                style={{ animation: "kpFadeInUp 0.9s ease-out both" }}
              >
                When you feel a connection, open your eyes and tap your letter.
              </p>
            ) : null}
          </div>
        </div>

        <button
          type="button"
          onClick={handleReady}
          className="mt-8 text-sm text-white/40 transition hover:text-white/70"
        >
          I&apos;m ready
        </button>
      </div>
    </div>
  );
}
