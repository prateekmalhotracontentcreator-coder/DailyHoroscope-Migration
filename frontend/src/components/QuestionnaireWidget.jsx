import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  BriefcaseBusiness,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Crown,
  HeartHandshake,
  LoaderCircle,
  Lock,
  MapPin,
  Sparkles,
  Users,
} from "lucide-react";
import { Link } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "";
const PROFILE_API = `${BACKEND_URL}/api/user/context-profile`;
const COMPLETION_API = `${BACKEND_URL}/api/user/context-profile/completion`;

const DEFAULT_PROFILE = {
  user_id: "",
  salary_bracket: "",
  family_wealth_tier: "",
  siblings_count: "",
  current_city: "",
  travel_frequency: "",
  relationship_status: "",
  parents_data: {
    father: { dob: "", place: "" },
    mother: { dob: "", place: "" },
  },
  beta_score: 1,
  gamma_score: 1,
  completion_pct: 0,
  last_updated: null,
};

const FIELD_LABELS = {
  salary_bracket: "Monthly income",
  family_wealth_tier: "Family financial background",
  siblings_count: "Number of siblings",
  current_city: "Current city of residence",
  travel_frequency: "International travel frequency",
  relationship_status: "Relationship status",
  "parents_data.father.dob": "Father's date of birth",
  "parents_data.father.place": "Father's place of birth",
  "parents_data.mother.dob": "Mother's date of birth",
  "parents_data.mother.place": "Mother's place of birth",
};

const SECTION_DEFINITIONS = [
  {
    id: "personal",
    title: "Personal Circumstances",
    description: "Income, family background, and sibling context sharpen beta and gamma calibration.",
    icon: BriefcaseBusiness,
    fields: ["salary_bracket", "family_wealth_tier", "siblings_count"],
    saveLabel: "Save personal circumstances",
  },
  {
    id: "life",
    title: "Life & Location",
    description: "Residence and travel habits help Arc Angel interpret movement and environment signals.",
    icon: MapPin,
    fields: ["current_city", "travel_frequency"],
    saveLabel: "Save life & location",
  },
  {
    id: "relationships",
    title: "Relationships",
    description: "Relationship context improves how family and partnership themes are weighted.",
    icon: HeartHandshake,
    fields: ["relationship_status"],
    saveLabel: "Save relationship details",
  },
  {
    id: "family",
    title: "Family Background",
    description: "Optional for enhanced Vedic accuracy through the Kota Chakra layer.",
    icon: Users,
    fields: [
      "parents_data.father.dob",
      "parents_data.father.place",
      "parents_data.mother.dob",
      "parents_data.mother.place",
    ],
    saveLabel: "Save family background",
  },
  {
    id: "review",
    title: "Review & Arc Angel Impact",
    description: "See what is still missing and how much more accuracy you can unlock.",
    icon: CheckCircle2,
    fields: Object.keys(FIELD_LABELS),
    reviewOnly: true,
  },
];

const SALARY_OPTIONS = [
  { value: "low", label: "Low", hint: "under Rs50K" },
  { value: "mid", label: "Mid", hint: "Rs50K-Rs2L" },
  { value: "high", label: "High", hint: "above Rs2L" },
];

const WEALTH_OPTIONS = [
  { value: "low", label: "Low" },
  { value: "mid", label: "Mid" },
  { value: "high", label: "High" },
];

const TRAVEL_OPTIONS = [
  { value: "rarely", label: "Rarely", hint: "< 2x/year" },
  { value: "sometimes", label: "Sometimes", hint: "2-5x/year" },
  { value: "frequently", label: "Frequently", hint: "> 5x/year" },
];

const RELATIONSHIP_OPTIONS = [
  { value: "single", label: "Single" },
  { value: "relationship", label: "In a relationship" },
  { value: "married", label: "Married" },
  { value: "separated", label: "Separated" },
  { value: "widowed", label: "Widowed" },
];

function fieldError(error, fallback) {
  return error?.response?.data?.detail || error?.response?.data?.message || fallback;
}

function hasActiveSubscription(subscription, user) {
  if (typeof subscription === "boolean") {
    return subscription;
  }

  const booleanFlags = [
    subscription?.active,
    subscription?.is_active,
    subscription?.isActive,
    subscription?.premium,
    subscription?.is_premium,
    subscription?.subscribed,
    user?.subscription_active,
    user?.is_premium,
    user?.premium,
  ];

  if (booleanFlags.some((value) => value === true)) {
    return true;
  }

  const tierValues = [
    subscription?.plan,
    subscription?.tier,
    subscription?.status,
    subscription?.membership,
    user?.subscription_plan,
    user?.subscription_tier,
    user?.membership,
  ]
    .filter(Boolean)
    .map((value) => String(value).toLowerCase());

  return tierValues.some((value) =>
    ["premium", "pro", "gold", "paid", "active", "subscribed"].includes(value)
  );
}

function normalizeText(value) {
  if (typeof value !== "string") {
    return "";
  }

  return value;
}

function normalizeParent(value) {
  return {
    dob: normalizeText(value?.dob),
    place: normalizeText(value?.place),
  };
}

function normalizeProfile(value) {
  const rawSiblingCount = value?.siblings_count;

  return {
    ...DEFAULT_PROFILE,
    ...value,
    salary_bracket: normalizeText(value?.salary_bracket),
    family_wealth_tier: normalizeText(value?.family_wealth_tier),
    siblings_count:
      rawSiblingCount === 0 ||
      (rawSiblingCount !== null &&
        rawSiblingCount !== undefined &&
        rawSiblingCount !== "" &&
        Number.isFinite(Number(rawSiblingCount)))
        ? Number(rawSiblingCount)
        : "",
    current_city: normalizeText(value?.current_city),
    travel_frequency: normalizeText(value?.travel_frequency),
    relationship_status: normalizeText(value?.relationship_status),
    parents_data: {
      father: normalizeParent(value?.parents_data?.father),
      mother: normalizeParent(value?.parents_data?.mother),
    },
  };
}

function getPathValue(profile, path) {
  return path.split(".").reduce((current, part) => current?.[part], profile);
}

function deriveMissingFields(profile) {
  return Object.keys(FIELD_LABELS).filter((fieldPath) => {
    const value = getPathValue(profile, fieldPath);
    if (typeof value === "number") {
      return Number.isNaN(value);
    }
    return !String(value || "").trim();
  });
}

function normalizeCompletion(value, profile) {
  const rawMissing = Array.isArray(value?.missing_fields) ? value.missing_fields : deriveMissingFields(profile);
  const uniqueMissing = Array.from(new Set(rawMissing));
  const rawPct =
    typeof value?.completion_pct === "number"
      ? value.completion_pct
      : Math.round(((Object.keys(FIELD_LABELS).length - uniqueMissing.length) / Object.keys(FIELD_LABELS).length) * 100);

  return {
    completion_pct: Math.max(0, Math.min(100, Number(rawPct) || 0)),
    missing_fields: uniqueMissing,
  };
}

function completionCopy(completionPct) {
  if (completionPct < 30) {
    return "+10-15% accuracy when completed";
  }

  if (completionPct <= 70) {
    return "+5-10% accuracy when completed";
  }

  return "Nearly there - complete remaining fields for full accuracy";
}

function getSectionMissingCount(section, missingFields) {
  if (section.reviewOnly) {
    return missingFields.length;
  }

  return missingFields.filter((field) => section.fields.includes(field)).length;
}

function getNextIncompleteSection(sections) {
  return sections.find((section) => !section.locked && !section.reviewOnly && section.missingCount > 0) || null;
}

function compactHeadline(premiumActive, completionPct) {
  if (!premiumActive) {
    return "Start your Premium profile";
  }

  if (completionPct >= 100) {
    return "Profile complete";
  }

  return "Complete your next section";
}

function GlassCard({ className = "", children }) {
  return <div className={`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm ${className}`}>{children}</div>;
}

function ProgressRing({ value, size = 56, strokeWidth = 6 }) {
  const safeValue = Math.max(0, Math.min(100, Number(value) || 0));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (safeValue / 100) * circumference;

  return (
    <div className="relative flex h-14 w-14 items-center justify-center">
      <svg viewBox={`0 0 ${size} ${size}`} className="h-full w-full -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          className="stroke-gold/20"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          className="stroke-gold"
          strokeDasharray={`${progress} ${circumference - progress}`}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center text-xs font-semibold text-foreground">
        {safeValue}%
      </div>
    </div>
  );
}

function ProgressBar({ value }) {
  const safeValue = Math.max(0, Math.min(100, Number(value) || 0));

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm font-medium text-foreground">{safeValue}% complete</p>
        <p className="text-sm text-muted-foreground">Persistent dialogue</p>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-gold/20">
        <div className="h-full bg-gold transition-all duration-300" style={{ width: `${safeValue}%` }} />
      </div>
    </div>
  );
}

function SectionStatus({ section }) {
  if (section.locked) {
    return (
      <span className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-background/60 px-3 py-1 text-xs font-semibold text-gold">
        <Lock className="h-3.5 w-3.5" />
        Premium
      </span>
    );
  }

  if (section.missingCount === 0) {
    return (
      <span className="inline-flex items-center gap-2 rounded-full border border-emerald-500/25 bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-500">
        <CheckCircle2 className="h-3.5 w-3.5" />
        Complete
      </span>
    );
  }

  return (
    <span className="inline-flex items-center rounded-full border border-gold/20 bg-background/60 px-3 py-1 text-xs font-semibold text-muted-foreground">
      {section.missingCount} missing
    </span>
  );
}

function RadioGroupField({ legend, value, options, onChange }) {
  return (
    <fieldset className="space-y-3">
      <legend className="text-sm font-medium text-foreground">{legend}</legend>
      <div className="grid gap-3 sm:grid-cols-2">
        {options.map((option) => {
          const selected = value === option.value;

          return (
            <label
              key={option.value}
              className={`cursor-pointer rounded-xl border px-4 py-3 transition ${
                selected
                  ? "border-gold bg-gold/10 shadow-sm"
                  : "border-gold/20 bg-background/60 hover:border-gold/40 hover:bg-gold/5"
              }`}
            >
              <input
                type="radio"
                name={legend}
                value={option.value}
                checked={selected}
                onChange={(event) => onChange(event.target.value)}
                className="sr-only"
              />
              <div className="flex items-start gap-3">
                <span
                  className={`mt-0.5 flex h-5 w-5 items-center justify-center rounded-full border transition ${
                    selected ? "border-gold bg-gold/15" : "border-gold/35 bg-background"
                  }`}
                >
                  <span className={`h-2.5 w-2.5 rounded-full ${selected ? "bg-gold" : "bg-transparent"}`} />
                </span>
                <span className="space-y-1">
                  <span className="block text-sm font-medium text-foreground">{option.label}</span>
                  {option.hint ? (
                    <span className="block text-xs text-muted-foreground">{option.hint}</span>
                  ) : null}
                </span>
              </div>
            </label>
          );
        })}
      </div>
    </fieldset>
  );
}

function UpgradePrompt() {
  return (
    <div className="space-y-4 rounded-xl border border-dashed border-gold/30 bg-background/60 p-5">
      <div className="flex items-start gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gold/10 text-gold">
          <Crown className="h-5 w-5" />
        </div>
        <div className="space-y-1">
          <p className="font-medium text-foreground">Upgrade to Premium</p>
          <p className="text-sm text-muted-foreground">
            Unlock the rest of the questionnaire to improve beta and gamma accuracy for your reports.
          </p>
        </div>
      </div>
      <p className="text-sm text-muted-foreground">
        Free members can start with personal circumstances, then upgrade to continue the full profile.
      </p>
    </div>
  );
}

export default function QuestionnaireWidget({
  compact = false,
  onSaveSuccess = () => {},
}) {
  const { user, subscription } = useAuth();
  const premiumActive = hasActiveSubscription(subscription, user);

  const [profile, setProfile] = useState(DEFAULT_PROFILE);
  const [completion, setCompletion] = useState({
    completion_pct: 0,
    missing_fields: Object.keys(FIELD_LABELS),
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [savingSection, setSavingSection] = useState("");
  const [expandedSection, setExpandedSection] = useState("personal");
  const [saveNotice, setSaveNotice] = useState({
    sectionId: "",
    message: "",
  });

  const sections = useMemo(
    () =>
      SECTION_DEFINITIONS.map((section, index) => ({
        ...section,
        locked: !premiumActive && index > 0,
        missingCount: getSectionMissingCount(section, completion.missing_fields),
      })),
    [completion.missing_fields, premiumActive]
  );

  const firstIncompleteSection = useMemo(() => getNextIncompleteSection(sections), [sections]);
  const compactSection = compact ? firstIncompleteSection || null : null;
  const hasLockedSections = useMemo(
    () => sections.some((section) => section.locked && !section.reviewOnly),
    [sections]
  );
  const nextSectionAfterSave = useMemo(() => {
    if (!saveNotice.sectionId) {
      return null;
    }

    const savedIndex = sections.findIndex((section) => section.id === saveNotice.sectionId);
    return (
      sections
        .slice(savedIndex + 1)
        .find((section) => !section.locked && !section.reviewOnly && section.missingCount > 0) || null
    );
  }, [saveNotice.sectionId, sections]);

  useEffect(() => {
    if (!user) {
      setLoading(false);
      return undefined;
    }

    let active = true;

    async function loadProfileData() {
      setLoading(true);
      setError("");

      try {
        const [profileResponse, completionResponse] = await Promise.all([
          axios.get(PROFILE_API, { withCredentials: true }),
          axios.get(COMPLETION_API, { withCredentials: true }),
        ]);

        if (!active) {
          return;
        }

        const nextProfile = normalizeProfile(profileResponse.data || {});
        const nextCompletion = normalizeCompletion(completionResponse.data || {}, nextProfile);

        setProfile(nextProfile);
        setCompletion(nextCompletion);
        setExpandedSection((currentSection) => {
          if (currentSection && currentSection !== "review") {
            return currentSection;
          }

          const nextOpenSection =
            SECTION_DEFINITIONS.find((section) => {
              if (!premiumActive && section.id !== "personal") {
                return false;
              }

              const missingCount = getSectionMissingCount(section, nextCompletion.missing_fields);
              return !section.reviewOnly && missingCount > 0;
            }) || SECTION_DEFINITIONS[0];

          return nextOpenSection.id;
        });
      } catch (requestError) {
        if (!active) {
          return;
        }

        setError(fieldError(requestError, "Unable to load your questionnaire right now."));
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadProfileData();

    return () => {
      active = false;
    };
  }, [premiumActive, user]);

  const missingFieldLabels = useMemo(() => {
    return completion.missing_fields
      .map((field) => FIELD_LABELS[field] || field)
      .filter(Boolean);
  }, [completion.missing_fields]);

  const updateField = (key, value) => {
    setProfile((previousValue) => ({
      ...previousValue,
      [key]: value,
    }));
  };

  const updateParentField = (parentKey, fieldKey, value) => {
    setProfile((previousValue) => ({
      ...previousValue,
      parents_data: {
        ...previousValue.parents_data,
        [parentKey]: {
          ...previousValue.parents_data[parentKey],
          [fieldKey]: value,
        },
      },
    }));
  };

  const refreshCompletion = async (currentSectionId) => {
    const [profileResponse, completionResponse] = await Promise.all([
      axios.get(PROFILE_API, { withCredentials: true }),
      axios.get(COMPLETION_API, { withCredentials: true }),
    ]);

    const nextProfile = normalizeProfile(profileResponse.data || {});
    const nextCompletion = normalizeCompletion(completionResponse.data || {}, nextProfile);

    setProfile(nextProfile);
    setCompletion(nextCompletion);
    setSaveNotice({
      sectionId: currentSectionId,
      message: "Saved successfully.",
    });
    onSaveSuccess(nextProfile);

    const nextOpenSection =
      SECTION_DEFINITIONS.find((section, index) => {
        if (!premiumActive && index > 0) {
          return false;
        }

        return (
          !section.reviewOnly &&
          getSectionMissingCount(section, nextCompletion.missing_fields) > 0
        );
      }) || SECTION_DEFINITIONS[0];

    setExpandedSection(nextOpenSection.id);
  };

  const saveSection = async (sectionId) => {
    setSavingSection(sectionId);
    setError("");
    setSaveNotice({ sectionId: "", message: "" });

    let payload = {};

    if (sectionId === "personal") {
      payload = {
        salary_bracket: profile.salary_bracket || null,
        family_wealth_tier: profile.family_wealth_tier || null,
        siblings_count:
          profile.siblings_count === "" || profile.siblings_count === null
            ? null
            : Math.max(0, Math.min(10, Number(profile.siblings_count))),
      };
    }

    if (sectionId === "life") {
      payload = {
        current_city: profile.current_city.trim() || null,
        travel_frequency: profile.travel_frequency || null,
      };
    }

    if (sectionId === "relationships") {
      payload = {
        relationship_status: profile.relationship_status || null,
      };
    }

    if (sectionId === "family") {
      payload = {
        parents_data: {
          father: {
            dob: profile.parents_data.father.dob || null,
            place: profile.parents_data.father.place.trim() || null,
          },
          mother: {
            dob: profile.parents_data.mother.dob || null,
            place: profile.parents_data.mother.place.trim() || null,
          },
        },
      };
    }

    try {
      await axios.put(PROFILE_API, payload, { withCredentials: true });
      await refreshCompletion(sectionId);
    } catch (requestError) {
      setError(fieldError(requestError, "We could not save this section. Please try again."));
    } finally {
      setSavingSection("");
    }
  };

  const renderSectionBody = (section) => {
    if (section.locked) {
      return <UpgradePrompt />;
    }

    if (section.id === "personal") {
      return (
        <div className="space-y-6">
          <RadioGroupField
            legend="What is your approximate monthly income?"
            value={profile.salary_bracket}
            options={SALARY_OPTIONS}
            onChange={(value) => updateField("salary_bracket", value)}
          />

          <RadioGroupField
            legend="How would you describe your family's financial background?"
            value={profile.family_wealth_tier}
            options={WEALTH_OPTIONS}
            onChange={(value) => updateField("family_wealth_tier", value)}
          />

          <label className="block space-y-2">
            <span className="text-sm font-medium text-foreground">Number of siblings</span>
            <input
              type="number"
              min="0"
              max="10"
              inputMode="numeric"
              value={profile.siblings_count}
              onChange={(event) => {
                const rawValue = event.target.value;
                if (rawValue === "") {
                  updateField("siblings_count", "");
                  return;
                }

                const numericValue = Math.max(0, Math.min(10, Number(rawValue)));
                updateField("siblings_count", Number.isNaN(numericValue) ? "" : numericValue);
              }}
              className="w-full rounded-xl border border-gold/20 bg-background px-4 py-3 text-foreground outline-none transition focus:border-gold"
            />
          </label>
        </div>
      );
    }

    if (section.id === "life") {
      return (
        <div className="space-y-6">
          <label className="block space-y-2">
            <span className="text-sm font-medium text-foreground">
              What is your current city of residence?
            </span>
            <input
              type="text"
              value={profile.current_city}
              onChange={(event) => updateField("current_city", event.target.value)}
              className="w-full rounded-xl border border-gold/20 bg-background px-4 py-3 text-foreground outline-none transition focus:border-gold"
              placeholder="Enter your city"
            />
          </label>

          <RadioGroupField
            legend="How often do you travel internationally?"
            value={profile.travel_frequency}
            options={TRAVEL_OPTIONS}
            onChange={(value) => updateField("travel_frequency", value)}
          />
        </div>
      );
    }

    if (section.id === "relationships") {
      return (
        <RadioGroupField
          legend="What is your current relationship status?"
          value={profile.relationship_status}
          options={RELATIONSHIP_OPTIONS}
          onChange={(value) => updateField("relationship_status", value)}
        />
      );
    }

    if (section.id === "family") {
      return (
        <div className="space-y-6">
          <p className="text-sm text-muted-foreground">
            Providing your parents' birth data enables the enhanced Kota Chakra accuracy layer.
            This is fully optional.
          </p>

          <div className="grid gap-5 lg:grid-cols-2">
            <div className="space-y-4 rounded-xl border border-gold/15 bg-background/60 p-4">
              <h4 className="font-medium text-foreground">Father</h4>
              <label className="block space-y-2">
                <span className="text-sm font-medium text-foreground">Date of birth</span>
                <input
                  type="date"
                  value={profile.parents_data.father.dob}
                  onChange={(event) => updateParentField("father", "dob", event.target.value)}
                  className="w-full rounded-xl border border-gold/20 bg-background px-4 py-3 text-foreground outline-none transition focus:border-gold"
                />
              </label>
              <label className="block space-y-2">
                <span className="text-sm font-medium text-foreground">Place of birth</span>
                <input
                  type="text"
                  value={profile.parents_data.father.place}
                  onChange={(event) => updateParentField("father", "place", event.target.value)}
                  className="w-full rounded-xl border border-gold/20 bg-background px-4 py-3 text-foreground outline-none transition focus:border-gold"
                  placeholder="Enter birth place"
                />
              </label>
            </div>

            <div className="space-y-4 rounded-xl border border-gold/15 bg-background/60 p-4">
              <h4 className="font-medium text-foreground">Mother</h4>
              <label className="block space-y-2">
                <span className="text-sm font-medium text-foreground">Date of birth</span>
                <input
                  type="date"
                  value={profile.parents_data.mother.dob}
                  onChange={(event) => updateParentField("mother", "dob", event.target.value)}
                  className="w-full rounded-xl border border-gold/20 bg-background px-4 py-3 text-foreground outline-none transition focus:border-gold"
                />
              </label>
              <label className="block space-y-2">
                <span className="text-sm font-medium text-foreground">Place of birth</span>
                <input
                  type="text"
                  value={profile.parents_data.mother.place}
                  onChange={(event) => updateParentField("mother", "place", event.target.value)}
                  className="w-full rounded-xl border border-gold/20 bg-background px-4 py-3 text-foreground outline-none transition focus:border-gold"
                  placeholder="Enter birth place"
                />
              </label>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="space-y-5">
        <div className="grid gap-4 lg:grid-cols-[0.9fr,1.1fr]">
          <div className="rounded-xl border border-gold/15 bg-background/60 p-5">
            <p className="text-sm font-medium text-foreground">Current completion</p>
            <p className="mt-2 text-3xl font-semibold text-gold">{completion.completion_pct}%</p>
            <p className="mt-3 text-sm text-muted-foreground">
              {completionCopy(completion.completion_pct)}
            </p>
          </div>

          <div className="rounded-xl border border-gold/15 bg-background/60 p-5">
            <p className="text-sm font-medium text-foreground">Missing fields</p>
            {missingFieldLabels.length ? (
              <div className="mt-3 flex flex-wrap gap-2">
                {missingFieldLabels.map((label) => (
                  <span
                    key={label}
                    className="inline-flex rounded-full border border-gold/20 bg-background px-3 py-1 text-xs font-medium text-muted-foreground"
                  >
                    {label}
                  </span>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm text-muted-foreground">
                Nothing missing. Your Arc Angel profile is fully populated.
              </p>
            )}
          </div>
        </div>

        <Link
          to="/arc-angel"
          className="inline-flex items-center text-sm font-semibold text-gold transition hover:opacity-80"
        >
          View My Arc Angel Profile
          <ChevronRight className="ml-1 h-4 w-4" />
        </Link>
      </div>
    );
  };

  if (!user) {
    return (
      <GlassCard className="p-5">
        <p className="text-sm text-muted-foreground">Sign in to personalise your readings.</p>
      </GlassCard>
    );
  }

  if (loading) {
    return (
      <GlassCard className="p-6">
        <div className="flex items-center gap-3 text-muted-foreground">
          <LoaderCircle className="h-5 w-5 animate-spin text-gold" />
          <span className="text-sm">Loading your questionnaire...</span>
        </div>
      </GlassCard>
    );
  }

  if (error && !profile.user_id && completion.completion_pct === 0) {
    return (
      <GlassCard className="p-6">
        <div className="space-y-4">
          <p className="text-sm text-red-500">{error}</p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="inline-flex rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10"
          >
            Try again
          </button>
        </div>
      </GlassCard>
    );
  }

  if (compact) {
    if (!compactSection && hasLockedSections) {
      return (
        <GlassCard className="p-5">
          <div className="flex items-start justify-between gap-4">
            <div className="space-y-2">
              <p className="text-sm font-semibold text-foreground">
                {compactHeadline(premiumActive, completion.completion_pct)}
              </p>
              <p className="text-sm text-muted-foreground">
                Your first section is saved. Upgrade to unlock the remaining questionnaire sections.
              </p>
            </div>
            <ProgressRing value={completion.completion_pct} />
          </div>
          <div className="mt-4">
            <UpgradePrompt />
          </div>
          <Link
            to="/questionnaire"
            className="mt-4 inline-flex items-center text-sm font-semibold text-gold transition hover:opacity-80"
          >
            Complete full questionnaire
            <ChevronRight className="ml-1 h-4 w-4" />
          </Link>
        </GlassCard>
      );
    }

    if (!compactSection) {
      return (
        <GlassCard className="p-5">
          <div className="flex items-start justify-between gap-4">
            <div className="space-y-2">
              <p className="text-sm font-semibold text-foreground">
                {compactHeadline(premiumActive, completion.completion_pct)}
              </p>
              <p className="text-sm text-muted-foreground">
                Your onboarding profile is complete and Arc Angel has the full available context.
              </p>
            </div>
            <ProgressRing value={completion.completion_pct} />
          </div>
          <Link
            to="/questionnaire"
            className="mt-4 inline-flex items-center text-sm font-semibold text-gold transition hover:opacity-80"
          >
            Complete full questionnaire
            <ChevronRight className="ml-1 h-4 w-4" />
          </Link>
        </GlassCard>
      );
    }

    const CompactIcon = compactSection.icon;

    return (
      <GlassCard className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">
              {compactHeadline(premiumActive, completion.completion_pct)}
            </p>
            <h3 className="text-lg font-semibold text-foreground">{compactSection.title}</h3>
            <p className="text-sm text-muted-foreground">{compactSection.description}</p>
          </div>
          <ProgressRing value={completion.completion_pct} />
        </div>

        <div className="mt-5 rounded-xl border border-gold/15 bg-background/60 p-4">
          {saveNotice.message ? (
            <div className="mb-4 flex flex-wrap items-center gap-3 rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm">
              <span className="font-medium text-emerald-500">{saveNotice.message}</span>
              {nextSectionAfterSave ? (
                <span className="text-muted-foreground">
                  Next section -> {nextSectionAfterSave.title}
                </span>
              ) : null}
            </div>
          ) : null}

          <div className="mb-4 flex items-center gap-3 border-l-4 border-gold/70 pl-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gold/10 text-gold">
              <CompactIcon className="h-5 w-5" />
            </div>
            <div>
              <p className="font-medium text-foreground">{compactSection.title}</p>
              <p className="text-sm text-muted-foreground">{compactSection.missingCount} fields left</p>
            </div>
          </div>

          {renderSectionBody(compactSection)}

          {compactSection.reviewOnly ? null : (
            <button
              type="button"
              onClick={() => saveSection(compactSection.id)}
              disabled={savingSection === compactSection.id}
              className="mt-6 inline-flex items-center justify-center rounded-full bg-gold px-5 py-2.5 text-sm font-semibold text-background transition hover:bg-gold/90 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {savingSection === compactSection.id ? (
                <>
                  <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : (
                compactSection.saveLabel
              )}
            </button>
          )}
        </div>

        {error ? <p className="mt-4 text-sm text-red-500">{error}</p> : null}

        <Link
          to="/questionnaire"
          className="mt-5 inline-flex items-center text-sm font-semibold text-gold transition hover:opacity-80"
        >
          Complete full questionnaire
          <ChevronRight className="ml-1 h-4 w-4" />
        </Link>
      </GlassCard>
    );
  }

  return (
    <div className="space-y-6">
      <GlassCard className="p-6 sm:p-7">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div className="space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.18em] text-gold">
              <Sparkles className="h-4 w-4" />
              Personalise Your Readings
            </div>
            <div className="space-y-2">
              <h1 className="text-3xl font-semibold text-foreground sm:text-4xl">
                Personalise Your Readings
              </h1>
              <p className="max-w-2xl text-sm leading-7 text-muted-foreground">
                Each section you complete improves your Arc Angel accuracy.
              </p>
            </div>
          </div>
          <ProgressRing value={completion.completion_pct} size={72} strokeWidth={7} />
        </div>

        <div className="mt-6">
          <ProgressBar value={completion.completion_pct} />
        </div>
      </GlassCard>

      {error ? (
        <GlassCard className="border-red-500/30 p-5">
          <p className="text-sm text-red-500">{error}</p>
        </GlassCard>
      ) : null}

      {saveNotice.message ? (
        <GlassCard className="border-emerald-500/20 bg-emerald-500/10 p-4">
          <div className="flex flex-wrap items-center gap-3 text-sm">
            <span className="font-medium text-emerald-500">{saveNotice.message}</span>
            {nextSectionAfterSave ? (
              <span className="text-muted-foreground">Next section -> {nextSectionAfterSave.title}</span>
            ) : null}
          </div>
        </GlassCard>
      ) : null}

      <div className="space-y-4">
        {sections.map((section) => {
          const Icon = section.icon;
          const isExpanded = expandedSection === section.id;

          return (
            <GlassCard key={section.id} className="overflow-hidden">
              <button
                type="button"
                onClick={() => setExpandedSection(isExpanded ? "" : section.id)}
                className="flex w-full items-start justify-between gap-4 px-5 py-5 text-left sm:px-6"
              >
                <div className="flex min-w-0 items-start gap-4">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gold/10 text-gold">
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="min-w-0 space-y-2">
                    <div className="border-l-4 border-gold/70 pl-4">
                      <p className="text-lg font-semibold text-foreground">{section.title}</p>
                    </div>
                    <p className="text-sm leading-6 text-muted-foreground">{section.description}</p>
                  </div>
                </div>

                <div className="flex shrink-0 items-center gap-3">
                  <SectionStatus section={section} />
                  {isExpanded ? (
                    <ChevronDown className="h-5 w-5 text-muted-foreground" />
                  ) : (
                    <ChevronRight className="h-5 w-5 text-muted-foreground" />
                  )}
                </div>
              </button>

              {isExpanded ? (
                <div className="border-t border-gold/10 px-5 py-5 sm:px-6">
                  {renderSectionBody(section)}

                  {!section.locked && !section.reviewOnly ? (
                    <button
                      type="button"
                      onClick={() => saveSection(section.id)}
                      disabled={savingSection === section.id}
                      className="mt-6 inline-flex items-center justify-center rounded-full bg-gold px-5 py-2.5 text-sm font-semibold text-background transition hover:bg-gold/90 disabled:cursor-not-allowed disabled:opacity-70"
                    >
                      {savingSection === section.id ? (
                        <>
                          <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
                          Saving...
                        </>
                      ) : (
                        section.saveLabel
                      )}
                    </button>
                  ) : null}
                </div>
              ) : null}
            </GlassCard>
          );
        })}
      </div>
    </div>
  );
}
