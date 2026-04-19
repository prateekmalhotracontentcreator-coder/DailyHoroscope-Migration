import React, { useEffect } from "react";
import { Navigate } from "react-router-dom";

import QuestionnaireWidget from "../components/QuestionnaireWidget";
import { useAuth } from "../context/AuthContext";

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
        <QuestionnaireWidget compact={false} />
      </div>
    </div>
  );
}
