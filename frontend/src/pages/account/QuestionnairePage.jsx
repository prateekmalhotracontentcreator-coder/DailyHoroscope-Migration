import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import QuestionnaireWidget from "../../components/QuestionnaireWidget";
import { useAuth } from "../../context/AuthContext";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const QUESTIONNAIRE_PROFILE_API = `${BACKEND_URL}/api/knowledge-engine/questionnaire/profile`;
const QUESTIONNAIRE_SUBMIT_API = `${BACKEND_URL}/api/knowledge-engine/questionnaire/submit`;

function fieldError(error, fallback) {
  return error?.response?.data?.detail || error?.response?.data?.message || fallback;
}

export default function QuestionnairePage() {
  const { user } = useAuth();
  const [questionnaireProfile, setQuestionnaireProfile] = useState(null);
  const [loading, setLoading] = useState(Boolean(user));
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [showRetake, setShowRetake] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    document.title = "Personalise Your Readings | EverydayHoroscope";
  }, []);

  useEffect(() => {
    if (!user) {
      setLoading(false);
      setQuestionnaireProfile(null);
      return;
    }

    let active = true;

    async function fetchQuestionnaireProfile() {
      setLoading(true);
      setError("");
      try {
        const response = await axios.get(QUESTIONNAIRE_PROFILE_API, { withCredentials: true });
        if (!active) {
          return;
        }
        setQuestionnaireProfile(response.data || null);
      } catch (requestError) {
        if (!active) {
          return;
        }
        setQuestionnaireProfile({ completed: false, beta: 1.0, gamma: 1.0, focus_domains: [] });
        setError(fieldError(requestError, "Unable to load your questionnaire profile right now."));
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void fetchQuestionnaireProfile();
    return () => {
      active = false;
    };
  }, [user]);

  const completed = Boolean(questionnaireProfile?.completed) && !showRetake;
  const focusDomains = useMemo(
    () => (questionnaireProfile?.focus_domains || []).map((value) => String(value || "").replace(/_/g, " ")),
    [questionnaireProfile]
  );

  const handleSubmit = async (answers) => {
    setSubmitting(true);
    setError("");
    setSuccessMessage("");
    try {
      const response = await axios.post(
        QUESTIONNAIRE_SUBMIT_API,
        { answers },
        { withCredentials: true }
      );
      setQuestionnaireProfile({
        completed: true,
        beta: response.data?.beta ?? 1.0,
        gamma: response.data?.gamma ?? 1.0,
        focus_domains: response.data?.focus_domains || [],
        completed_at: response.data?.completed_at || null,
      });
      setShowRetake(false);
      setSuccessMessage("Your Cosmic Profile is set ✦ Your Vedic readings now include beta and gamma context.");
    } catch (requestError) {
      setError(fieldError(requestError, "We could not finalise your questionnaire. Please try again."));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-6 rounded-xl border border-gold/20 bg-gold/[0.04] p-5 shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-gold">
            Complete Your Arc Angel Profile
          </p>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">
            Your questionnaire sharpens Knowledge Engine context, improves Arc Angel confidence, and calibrates which life themes matter most right now.
          </p>
        </div>

        {!user ? (
          <div className="rounded-xl border border-gold/20 bg-card p-6 shadow-sm">
            <p className="text-lg font-semibold text-foreground">Sign in to unlock your Cosmic Profile</p>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">
              Save your questionnaire, personalise your Vedic readings, and carry your Arc Angel confidence across devices.
            </p>
            <Link
              to="/login"
              className="mt-4 inline-flex items-center rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10"
            >
              Sign in to continue
            </Link>
          </div>
        ) : loading ? (
          <div className="rounded-xl border border-gold/20 bg-card p-6 shadow-sm">
            <p className="text-sm text-muted-foreground">Loading your Cosmic Profile...</p>
          </div>
        ) : completed ? (
          <div className="space-y-5">
            <div className="rounded-xl border border-gold/20 bg-card p-6 shadow-sm">
              <p className="text-lg font-semibold text-foreground">Your Cosmic Profile is active ✦</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Your focus context is now calibrating your Vedic readings. These multipliers shape how Knowledge Engine weights your personal timing and priorities.
              </p>
              <div className="mt-5 grid gap-4 sm:grid-cols-2">
                <div className="rounded-xl border border-gold/15 bg-background/60 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Beta</p>
                  <p className="mt-2 text-3xl font-semibold text-foreground">{questionnaireProfile?.beta ?? 1.0}</p>
                  <p className="mt-2 text-sm text-muted-foreground">Life-phase context multiplier</p>
                </div>
                <div className="rounded-xl border border-gold/15 bg-background/60 p-4">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Gamma</p>
                  <p className="mt-2 text-3xl font-semibold text-foreground">{questionnaireProfile?.gamma ?? 1.0}</p>
                  <p className="mt-2 text-sm text-muted-foreground">Current focus-area multiplier</p>
                </div>
              </div>
              {focusDomains.length ? (
                <div className="mt-5">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Focus Domains</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {focusDomains.map((domain) => (
                      <span
                        key={domain}
                        className="inline-flex rounded-full border border-gold/20 bg-background px-3 py-1 text-xs font-medium text-muted-foreground"
                      >
                        {domain}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
              <div className="mt-6 flex flex-wrap gap-3">
                <Link
                  to="/arc-angel"
                  className="inline-flex items-center rounded-full bg-gold px-4 py-2 text-sm font-semibold text-background transition hover:bg-gold/90"
                >
                  View Your Arc Angel Reading →
                </Link>
                <button
                  type="button"
                  onClick={() => setShowRetake(true)}
                  className="inline-flex items-center rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10"
                >
                  Retake questionnaire
                </button>
              </div>
            </div>
            {successMessage ? (
              <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-4 text-sm text-emerald-600">
                {successMessage}
              </div>
            ) : null}
          </div>
        ) : (
          <div className="space-y-4">
            {successMessage ? (
              <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-4 text-sm text-emerald-600">
                {successMessage}
              </div>
            ) : null}
            {error ? (
              <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-500">
                {error}
              </div>
            ) : null}
            {submitting ? (
              <div className="rounded-xl border border-gold/20 bg-card p-4 text-sm text-muted-foreground shadow-sm">
                Calibrating your beta and gamma profile...
              </div>
            ) : null}
            <QuestionnaireWidget compact={false} onComplete={handleSubmit} />
          </div>
        )}
      </div>
    </div>
  );
}
