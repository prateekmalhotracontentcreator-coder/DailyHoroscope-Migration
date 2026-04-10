from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field
from pymongo import ASCENDING, DESCENDING, IndexModel


VoiceTone = Literal["classical", "modern_analytical", "kp_technical", "spiritual", "popular"]
ConditionType = Literal[
    "planet_in_house",
    "planet_in_sign",
    "planet_in_nakshatra",
    "planet_aspect",
    "planet_conjunction",
    "planet_dignity",
    "planet_retrograde",
    "house_lord_in_house",
    "yoga",
    "dasha_period",
    "transit",
    "kp_sublord",
    "composite",
]
ClaimScope = Literal["tendency", "event_timing", "window", "trait"]
ClaimPolarity = Literal["positive", "negative", "mixed", "neutral"]
TimingBias = Literal["early", "on_time", "late", "cyclical", "none"]
StrengthBand = Literal["low", "medium", "high", "extreme"]
SubjectScope = Literal["self", "partner", "household", "family"]
RepresentationMode = Literal["synthesis", "tension", "honest_uncertainty"]
BridgeType = Literal["contrast", "reinforcement", "transition", "deepening", "temporal", "cross_science"]
ConfidenceBand = Literal["LOW", "MEDIUM", "HIGH", "VERIFIED"]
DataQuality = Literal["low", "medium", "high"]
ApprovalStatus = Literal["pending_review", "approved", "rejected"]
ImportStatus = Literal["staged", "validated", "imported", "failed"]
PeriodQuality = Literal["auspicious", "neutral", "inauspicious"]

COLLECTION_INTERPRETATION_RULES = "interpretation_rules"
COLLECTION_AUTHOR_VOICES = "author_voices"
COLLECTION_NARRATIVE_BRIDGES = "narrative_bridges"
COLLECTION_IMPORT_BATCHES = "import_batches"
COLLECTION_CROSS_SCIENCE_COMBINATIONS = "cross_science_combinations"
COLLECTION_SCIENCE_REGISTRY = "science_registry"
COLLECTION_USER_ARC_ANGEL_PROFILE = "user_arc_angel_profile"
COLLECTION_USER_CONTEXT_PROFILE = "user_context_profile"
COLLECTION_CASE_STUDIES = "case_studies"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StrictDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, arbitrary_types_allowed=True)

    id: Any | None = Field(default=None, alias="_id")


class FlexiblePayload(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True, arbitrary_types_allowed=True)


class RuleCondition(FlexiblePayload):
    type: ConditionType
    planet: str | None = None
    planets: list[str] = Field(default_factory=list)
    house: int | None = None
    sign: str | None = None
    dignity: str | None = None
    retrograde: bool | None = None
    aspected_by: str | None = None
    aspecting_house: int | None = None
    conjunct_with: str | None = None
    nakshatra: str | None = None
    dasha_active: str | None = None
    source_house: int | None = None
    target_house: int | None = None
    lord: str | None = None
    yoga_name: str | None = None
    dasha_lord: str | None = None
    level: str | None = None
    transit_house: int | None = None
    cusp_num: int | None = None
    sub_lord: str | None = None
    sub_conditions: list[dict[str, Any]] = Field(default_factory=list)
    operator: str | None = None


class InterpretationPassage(StrictDocument):
    text: str
    source: str
    chapter: str
    word_count: int = Field(ge=0)
    voice_tone: VoiceTone
    confidence: ConfidenceBand | None = None
    paraphrase_notes: str | None = None


class SecondarySource(StrictDocument):
    text: str
    chapter: str
    voice_tone: VoiceTone


class InterpretationBlock(StrictDocument):
    summary: str
    detailed: str
    full_text_passages: list[InterpretationPassage] = Field(default_factory=list)
    positive_aspects: list[str] = Field(default_factory=list)
    challenging_aspects: list[str] = Field(default_factory=list)
    remedies: list[str] = Field(default_factory=list)


class RuleSourceMetadata(StrictDocument):
    primary: str
    chapter: str
    author_voice: VoiceTone
    secondary_sources: list[SecondarySource] = Field(default_factory=list)
    batch_id: str


class RuleModifier(StrictDocument):
    condition: dict[str, Any] = Field(default_factory=dict)
    effect: str
    note: str


class InterpretationRuleDocument(StrictDocument):
    rule_id: str
    version: int = Field(default=1, ge=1)
    science_id: str = "vedic_astrology"
    approval_status: ApprovalStatus = "pending_review"
    life_domain: str
    claim_axis: str
    claim_scope: ClaimScope
    claim_polarity: ClaimPolarity
    timing_bias: TimingBias
    strength_band: StrengthBand
    subject_scope: SubjectScope
    authority_override: str | None = None
    mutually_exclusive_with: list[str] = Field(default_factory=list)
    passage_ref_id: str | None = None
    condition: RuleCondition
    interpretation: InterpretationBlock
    categories: list[str] = Field(default_factory=list)
    priority: int = Field(default=5, ge=0, le=10)
    intensity_score: float = Field(default=0.0, ge=0.0)
    source: RuleSourceMetadata
    modifiers: list[RuleModifier] = Field(default_factory=list)
    conflicts_with: list[str] = Field(default_factory=list)
    weight: float = Field(default=1.0, ge=0.0)
    tags: list[str] = Field(default_factory=list)
    active: bool = True
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class AuthorVoiceDocument(StrictDocument):
    voice_id: VoiceTone
    display_name: str
    tone_description: str
    example_authors: list[str] = Field(default_factory=list)
    llm_instruction: str
    active: bool = True
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class NarrativeBridgeDocument(StrictDocument):
    bridge_type: BridgeType
    context: str
    phrases: list[str] = Field(default_factory=list)
    active: bool = True
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ImportBatchDocument(StrictDocument):
    batch_id: str
    amendment_contract_id: str | None = None
    source_book: str
    import_status: ImportStatus = "staged"
    approval_status: ApprovalStatus = "pending_review"
    file_name: str | None = None
    rules_submitted: int = Field(default=0, ge=0)
    rules_imported: int = Field(default=0, ge=0)
    duplicate_count: int = Field(default=0, ge=0)
    conflict_count: int = Field(default=0, ge=0)
    error_count: int = Field(default=0, ge=0)
    index_refreshed: bool = False
    notes: str | None = None
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ScienceTrigger(StrictDocument):
    conditions: list[str] = Field(default_factory=list)
    min_match: int = Field(default=1, ge=1)


class CrossScienceScoring(StrictDocument):
    min_sciences_matched: int = Field(default=2, ge=1)
    intensity_when_all_four: float = Field(default=0.0, ge=0.0)
    intensity_when_three: float = Field(default=0.0, ge=0.0)
    intensity_when_two: float = Field(default=0.0, ge=0.0)


class CrossScienceCombinationDocument(StrictDocument):
    combo_id: str
    title: str
    theme: str
    triggers: dict[str, ScienceTrigger] = Field(default_factory=dict)
    confidence_weights: dict[str, float] = Field(default_factory=dict)
    scoring: CrossScienceScoring
    categories: list[str] = Field(default_factory=list)
    active: bool = True
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ScienceRegistryDocument(StrictDocument):
    science_id: str
    display_name: str
    hierarchy_rank: int = Field(ge=1)
    authority_domain: list[str] = Field(default_factory=list)
    defers_to: list[str] = Field(default_factory=list)
    complements: list[str] = Field(default_factory=list)
    contradiction_policy: str
    active: bool = True
    added_phase: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ArcAngelDataCompleteness(StrictDocument):
    birth_data: bool = False
    questionnaire: bool = False
    modules_run: list[str] = Field(default_factory=list)
    parents_data: bool = False


class ArcAngelPeriod(StrictDocument):
    start: str
    end: str
    driver: str


class ArcAngelDomainSnapshot(StrictDocument):
    domain_id: str
    domain_label: str
    domain_description: str | None = None
    primary_bhavas: list[int] = Field(default_factory=list)
    auspicious_periods: list[ArcAngelPeriod] = Field(default_factory=list)
    inauspicious_periods: list[ArcAngelPeriod] = Field(default_factory=list)
    period_quality_now: PeriodQuality | None = None
    confidence_pct: int = Field(default=0, ge=0, le=100)
    period_indicator: str | None = None
    correlated_modules: list[str] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=utc_now)


class UserArcAngelProfileDocument(StrictDocument):
    user_id: str
    computed_at: datetime = Field(default_factory=utc_now)
    overall_confidence_pct: int = Field(default=0, ge=0, le=100)
    data_completeness: ArcAngelDataCompleteness = Field(default_factory=ArcAngelDataCompleteness)
    domains: list[ArcAngelDomainSnapshot] = Field(default_factory=list)


class ParentBirthIdentity(StrictDocument):
    dob: str
    pob_city: str
    current_city: str


class ParentsBirthData(StrictDocument):
    father: ParentBirthIdentity | None = None
    mother: ParentBirthIdentity | None = None


class UserContextProfileDocument(StrictDocument):
    user_id: str
    questionnaire_version: str
    salary_bracket: str | None = None
    family_wealth_tier: str | None = None
    siblings_count: int | None = Field(default=None, ge=0)
    current_city: str | None = None
    travel_frequency: str | None = None
    relationship_status: str | None = None
    parents_birth_data: ParentsBirthData | None = None
    beta_score: float = Field(default=1.0, ge=0.0)
    gamma_score: float = Field(default=1.0, ge=0.0)
    last_updated: datetime = Field(default_factory=utc_now)


class CaseStudyBirthData(StrictDocument):
    date: str
    time: str
    place: str
    latitude: float
    longitude: float
    timezone: str


class KnownOutcome(StrictDocument):
    life_domain: str
    claim_axis: str
    outcome: str
    timing: str
    notes: str | None = None


class EnginePrediction(StrictDocument):
    life_domain: str
    claim_axis: str
    predicted_outcome: str
    period_quality: PeriodQuality | None = None
    confidence: float | None = Field(default=None, ge=0.0)
    matched_rule_ids: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=utc_now)


class CaseStudyDocument(StrictDocument):
    case_id: str
    subject: str
    birth_data: CaseStudyBirthData
    known_outcomes: list[KnownOutcome] = Field(default_factory=list)
    engine_predictions: list[EnginePrediction] = Field(default_factory=list)
    accuracy_score: float | None = Field(default=None, ge=0.0)
    validated: bool = False
    source_book: str
    data_quality: DataQuality
    added_phase: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ContextSignal(StrictDocument):
    score: float = 1.0
    source: str | None = None
    event: str | None = None
    region: str | None = None
    factors: list[str] = Field(default_factory=list)


class KnowledgeRequestContext(StrictDocument):
    backbone_science_id: str = "vedic_astrology"
    alpha: float | ContextSignal = 1.0
    beta: float | ContextSignal = 1.0
    gamma: float | ContextSignal = 1.0


class TensionClaim(StrictDocument):
    science_id: str
    summary: str
    effective_confidence: float = Field(ge=0.0)
    authority_rank: int = Field(ge=1)


class TensionBlock(StrictDocument):
    life_domain: str
    claim_axis: str
    representation_mode: RepresentationMode
    dominant_science: str
    backbone_science_id: str
    confidence_delta: float = Field(ge=0.0)
    contradiction_score: float = Field(ge=0.0)
    contradiction_types: list[str] = Field(default_factory=list)
    tranche_adjustments_applied: bool = False
    low_confidence: bool = False
    claims: list[TensionClaim] = Field(default_factory=list)


def knowledge_collection_models() -> dict[str, type[BaseModel]]:
    return {
        COLLECTION_INTERPRETATION_RULES: InterpretationRuleDocument,
        COLLECTION_AUTHOR_VOICES: AuthorVoiceDocument,
        COLLECTION_NARRATIVE_BRIDGES: NarrativeBridgeDocument,
        COLLECTION_IMPORT_BATCHES: ImportBatchDocument,
        COLLECTION_CROSS_SCIENCE_COMBINATIONS: CrossScienceCombinationDocument,
        COLLECTION_SCIENCE_REGISTRY: ScienceRegistryDocument,
        COLLECTION_USER_ARC_ANGEL_PROFILE: UserArcAngelProfileDocument,
        COLLECTION_USER_CONTEXT_PROFILE: UserContextProfileDocument,
        COLLECTION_CASE_STUDIES: CaseStudyDocument,
    }


def knowledge_index_models() -> dict[str, list[IndexModel]]:
    return {
        COLLECTION_INTERPRETATION_RULES: [
            IndexModel([("rule_id", ASCENDING), ("version", ASCENDING)], unique=True, name="rule_version_unique"),
            IndexModel([("active", ASCENDING), ("science_id", ASCENDING), ("life_domain", ASCENDING), ("claim_axis", ASCENDING)], name="active_science_domain_axis"),
            IndexModel([("condition.type", ASCENDING), ("condition.planet", ASCENDING), ("condition.house", ASCENDING)], name="condition_planet_house"),
            IndexModel([("claim_axis", ASCENDING), ("claim_scope", ASCENDING), ("timing_bias", ASCENDING)], name="claim_axis_scope_timing"),
            IndexModel([("categories", ASCENDING)], name="categories_lookup"),
            IndexModel([("tags", ASCENDING)], name="tags_lookup"),
            IndexModel([("active", ASCENDING), ("priority", DESCENDING)], name="active_priority"),
            IndexModel([("source.batch_id", ASCENDING)], name="source_batch_lookup"),
            IndexModel([("source.primary", ASCENDING), ("source.chapter", ASCENDING)], name="source_primary_chapter"),
            IndexModel([("approval_status", ASCENDING), ("active", ASCENDING)], name="approval_status_active"),
        ],
        COLLECTION_AUTHOR_VOICES: [
            IndexModel([("voice_id", ASCENDING)], unique=True, name="voice_id_unique"),
            IndexModel([("active", ASCENDING)], name="voice_active"),
        ],
        COLLECTION_NARRATIVE_BRIDGES: [
            IndexModel([("bridge_type", ASCENDING), ("context", ASCENDING)], unique=True, name="bridge_type_context_unique"),
            IndexModel([("active", ASCENDING)], name="bridge_active"),
        ],
        COLLECTION_IMPORT_BATCHES: [
            IndexModel([("batch_id", ASCENDING)], unique=True, name="batch_id_unique"),
            IndexModel([("approval_status", ASCENDING), ("import_status", ASCENDING)], name="batch_status_lookup"),
            IndexModel([("created_at", DESCENDING)], name="batch_created_desc"),
        ],
        COLLECTION_CROSS_SCIENCE_COMBINATIONS: [
            IndexModel([("combo_id", ASCENDING)], unique=True, name="combo_id_unique"),
            IndexModel([("theme", ASCENDING)], name="combo_theme"),
            IndexModel([("categories", ASCENDING), ("active", ASCENDING)], name="combo_category_active"),
        ],
        COLLECTION_SCIENCE_REGISTRY: [
            IndexModel([("science_id", ASCENDING)], unique=True, name="science_id_unique"),
            IndexModel([("active", ASCENDING), ("hierarchy_rank", ASCENDING)], name="science_active_rank"),
        ],
        COLLECTION_USER_ARC_ANGEL_PROFILE: [
            IndexModel([("user_id", ASCENDING)], unique=True, name="arc_angel_user_unique"),
            IndexModel([("computed_at", DESCENDING)], name="arc_angel_computed_desc"),
        ],
        COLLECTION_USER_CONTEXT_PROFILE: [
            IndexModel([("user_id", ASCENDING)], unique=True, name="context_user_unique"),
            IndexModel([("last_updated", DESCENDING)], name="context_updated_desc"),
        ],
        COLLECTION_CASE_STUDIES: [
            IndexModel([("case_id", ASCENDING)], unique=True, name="case_id_unique"),
            IndexModel([("source_book", ASCENDING), ("data_quality", ASCENDING)], name="case_source_quality"),
            IndexModel([("validated", ASCENDING), ("accuracy_score", DESCENDING)], name="case_validated_accuracy"),
        ],
    }


async def ensure_knowledge_indexes(db: Any) -> dict[str, list[str]]:
    created: dict[str, list[str]] = {}
    for collection_name, index_models in knowledge_index_models().items():
        if not index_models:
            created[collection_name] = []
            continue
        result = await db[collection_name].create_indexes(index_models)
        created[collection_name] = list(result)
    return created
