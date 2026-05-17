import React, { useEffect } from "react";
import { Link, Navigate } from "react-router-dom";

import QuestionnaireWidget from "../../components/QuestionnaireWidget";
import { useAuth } from "../../context/AuthContext";

// Host app wiring:
// import QuestionnairePage from "./pages/QuestionnairePage";
// <Route path="/questionnaire" element={<PrivateRoute><QuestionnairePage /></PrivateRoute>} />

export default function QuestionnairePage() {
  const { user } = useAuth();

  useEffect(() => {
    document.title = "Personalise Your Readings | EverydayHoroscope";
  }, []);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="mb-6 rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm p-5">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-gold">
            Complete Your Arc Angel Profile
          </p>
          <p className="mt-2 text-sm leading-6 text-muted-foreground">
            Every question answered raises your confidence percentage. Upgrade to Arc Angel Pro for Individual Reports that elevate each domain's accuracy by up to 43%.
          </p>
          <Link
            to="/individual-reports"
            className="mt-4 inline-flex items-center rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10"
          >
            Explore Reports &rarr;
          </Link>
        </div>
        <QuestionnaireWidget compact={false} />
      </div>
    </div>
  );
}
