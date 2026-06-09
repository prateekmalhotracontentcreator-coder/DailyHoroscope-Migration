from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pymongo import ASCENDING, DESCENDING, IndexModel

from ke_schema_constants import (
    ALL_PLANETS,
    ENGINE_DEPENDENCY_IDENTIFIERS,
    LEGACY_CLAIM_SCOPES,
    STANDARD_PLANETS,
    UPAGRAHA_PLANETS,
    VALID_ASHTAKAVARGA_SYSTEMS,
    VALID_CANCELLATION_TRIGGERS,
    VALID_CLAIM_AXES,
    VALID_CONDITION_TYPES,
    VALID_CROSS_TEXT_RELATIONSHIPS,
    VALID_DASHA_SYSTEMS,
    VALID_NULLIFICATION_TYPES,
    VALID_PLANET_CATEGORIES,
    VALID_REFERENCE_POINTS,
    VALID_SCOPES,
    VALID_SIGNS,
)


VoiceTone = Literal["classical", "modern_analytical", "kp_technical", "spiritual", "popular"]
ConditionType = str
ClaimScope = str
ClaimPolarity = Literal["positive", "negative", "mixed", "neutral"]
TimingBias = Literal["early", "on_time", "late", "cyclical", "none"]
StrengthBand = Literal["low", "medium", "high", "extreme"]
SubjectScope = Literal["self", "partner", "household", "family"]
RepresentationMode = Literal["synthesis", "tension", "honest_uncertainty"]
BridgeType = Literal["contrast", "reinforcement", "transition", "deepening", "temporal", "cross_science"]
ConfidenceBand = Literal["LOW", "MEDIUM", "HIGH", "VERIFIED"]
DataQuality = Literal["low", "medium", "high"]
ApprovalStatus = Literal[
    "pending_review",
    "approved",
    "rejected",
    "auto_approved",
    "pending_human_review",
    "flagged",
]
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


def _lower_or_none(value: str | None) -> str | None:
    if value is None:
        return None
    return str(value).strip().lower()


class VedhaNullifier(FlexiblePayload):
    vedha_house: int
    exception_planets: list[str] = Field(default_factory=list)
    nullification_type: str

    @field_validator("nullification_type")
    @classmethod
    def validate_nullification_type(cls, value: str) -> str:
        lowered = _lower_or_none(value)
        if lowered not in VALID_NULLIFICATION_TYPES:
            raise ValueError(f"Unsupported nullification_type: {value}")
        return lowered or value

    @field_validator("exception_planets")
    @classmethod
    def validate_exception_planets(cls, value: list[str]) -> list[str]:
        invalid = [planet for planet in value if _lower_or_none(planet) not in ALL_PLANETS]
        if invalid:
            raise ValueError(f"Unsupported exception_planets: {', '.join(invalid)}")
        return value


class CrossTextMatch(FlexiblePayload):
    rule_id: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    relationship: str

    @field_validator("relationship")
    @classmethod
    def validate_relationship(cls, value: str) -> str:
        lowered = _lower_or_none(value)
        if lowered not in VALID_CROSS_TEXT_RELATIONSHIPS:
            raise ValueError(f"Unsupported cross_text_matches relationship: {value}")
        return lowered or value


class RuleCondition(FlexiblePayload):
    type: ConditionType
    planet: str | None = None
    planet_category: str | None = None
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
    antardasha_planet: str | None = None
    dasha_system: str | None = None
    level: str | None = None
    transit_house: int | None = None
    cusp_num: int | None = None
    sub_lord: str | None = None
    cancellation_trigger: str | None = None
    reference_point: str | None = None
    system: str | None = None
    dot_count_min: int | None = None
    dot_count_max: int | None = None
    sub_conditions: list[dict[str, Any]] = Field(default_factory=list)
    operator: str | None = None

    @field_validator("type")
    @classmethod
    def validate_condition_type(cls, value: str) -> str:
        lowered = _lower_or_none(value)
        if lowered not in VALID_CONDITION_TYPES:
            raise ValueError(f"Unsupported condition.type: {value}")
        return lowered or value

    @field_validator(
        "planet",
        "aspected_by",
        "conjunct_with",
        "lord",
        "dasha_active",
        "dasha_lord",
        "antardasha_planet",
        "sub_lord",
    )
    @classmethod
    def validate_planet_like_fields(cls, value: str | None) -> str | None:
        lowered = _lower_or_none(value)
        if lowered is not None and lowered not in ALL_PLANETS:
            raise ValueError(f"Unsupported planet value: {value}")
        return lowered

    @field_validator("planets")
    @classmethod
    def validate_planet_list(cls, value: list[str]) -> list[str]:
        lowered = [_lower_or_none(item) for item in value]
        invalid = [item for item in lowered if item not in ALL_PLANETS]
        if invalid:
            raise ValueError(f"Unsupported planets value: {', '.join(invalid)}")
        return [item for item in lowered if item is not None]

    @field_validator("sign")
    @classmethod
    def validate_sign(cls, value: str | None) -> str | None:
        lowered = _lower_or_none(value)
        if lowered is not None and lowered not in VALID_SIGNS:
            raise ValueError(f"Unsupported sign value: {value}")
        return lowered

    @field_validator("planet_category")
    @classmethod
    def validate_planet_category(cls, value: str | None) -> str | None:
        lowered = _lower_or_none(value)
        if lowered is not None and lowered not in VALID_PLANET_CATEGORIES:
            raise ValueError(f"Unsupported planet_category: {value}")
        return lowered

    @field_validator("dasha_system")
    @classmethod
    def validate_dasha_system(cls, value: str | None) -> str | None:
        lowered = _lower_or_none(value)
        if lowered is not None and lowered not in VALID_DASHA_SYSTEMS:
            raise ValueError(f"Unsupported dasha_system: {value}")
        return lowered

    @field_validator("cancellation_trigger")
    @classmethod
    def validate_cancellation_trigger(cls, value: str | None) -> str | None:
        lowered = _lower_or_none(value)
        if lowered is not None and lowered not in VALID_CANCELLATION_TRIGGERS:
            raise ValueError(f"Unsupported cancellation_trigger: {value}")
        return lowered

    @field_validator("reference_point")
    @classmethod
    def validate_reference_point(cls, value: str | None) -> str | None:
        lowered = _lower_or_none(value)
        if lowered is not None and lowered not in VALID_REFERENCE_POINTS:
            raise ValueError(f"Unsupported reference_point: {value}")
        return lowered

    @field_validator("system")
    @classmethod
    def validate_ashtakavarga_system(cls, value: str | None) -> str | None:
        lowered = _lower_or_none(value)
        if lowered is not None and lowered not in VALID_ASHTAKAVARGA_SYSTEMS:
            raise ValueError(f"Unsupported system: {value}")
        return lowered

    @model_validator(mode="after")
    def validate_condition_shape(self) -> "RuleCondition":
        if self.dot_count_max is not None and self.dot_count_min is not None and self.dot_count_max < self.dot_count_min:
            raise ValueError("dot_count_max must be greater than or equal to dot_count_min")

        planet_category = self.planet_category or ("physical" if self.planet else None)
        if planet_category:
            self.planet_category = planet_category

        if self.planet and self.planet in UPAGRAHA_PLANETS and self.planet_category != "upagraha":
            raise ValueError("Upagraha planets must include planet_category='upagraha'")
        if self.planet and self.planet in STANDARD_PLANETS and self.planet_category == "upagraha":
            raise ValueError("Standard planets cannot use planet_category='upagraha'")

        if self.type == "dasha_period" and not self.dasha_system:
            self.dasha_system = "vimshottari"

        return self


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


class ValidationResult(BaseModel):
    verdict: str = ""
    flag_reason: str = ""
    corrected_confidence: str = ""
    validated_by: str = ""
    validated_at: str = ""
    contradiction_ids: list[str] = Field(default_factory=list)
    contradiction_summary: str = ""

    model_config = ConfigDict(extra="ignore")


class InterpretationRuleDocument(StrictDocument):
    rule_id: str
    version: int = Field(default=1, ge=1)
    science_id: str = "vedic_astrology"
    approval_status: ApprovalStatus = "pending_review"
    life_domain: str
    claim_axis: str
    secondary_axis: str | None = None
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
    vedha_nullifier: VedhaNullifier | None = None
    engine_dependency: list[str] | None = None
    cross_text_matches: list[CrossTextMatch] | None = None
    conflicts_with: list[str] = Field(default_factory=list)
    weight: float = Field(default=1.0, ge=0.0)
    tags: list[str] = Field(default_factory=list)
    active: bool = True
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    validation: ValidationResult = Field(default_factory=ValidationResult)

    @field_validator("claim_scope")
    @classmethod
    def validate_claim_scope(cls, value: str) -> str:
        lowered = _lower_or_none(value)
        valid_scopes = set(VALID_SCOPES) | set(LEGACY_CLAIM_SCOPES)
        if lowered not in valid_scopes:
            raise ValueError(f"Unsupported claim_scope: {value}")
        return lowered or value

    @field_validator("claim_axis")
    @classmethod
    def validate_claim_axis(cls, value: str) -> str:
        lowered = _lower_or_none(value)
        if lowered not in VALID_CLAIM_AXES:
            raise ValueError(f"Unsupported claim_axis: {value}")
        return lowered or value

    @field_validator("secondary_axis")
    @classmethod
    def validate_secondary_axis(cls, value: str | None) -> str | None:
        lowered = _lower_or_none(value)
        if lowered is not None and lowered not in VALID_CLAIM_AXES:
            raise ValueError(f"Unsupported secondary_axis: {value}")
        return lowered

    @field_validator("engine_dependency")
    @classmethod
    def validate_engine_dependency(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value
        lowered = [_lower_or_none(item) for item in value]
        invalid = [item for item in lowered if item not in ENGINE_DEPENDENCY_IDENTIFIERS]
        if invalid:
            raise ValueError(f"Unsupported engine_dependency values: {', '.join(invalid)}")
        return [item for item in lowered if item is not None]

    @model_validator(mode="after")
    def validate_rule_shape(self) -> "InterpretationRuleDocument":
        if self.condition.type == "lagna_sign" and self.claim_scope != "natal_lagna":
            raise ValueError("Rules with condition.type='lagna_sign' must use claim_scope='natal_lagna'")
        return self


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
    period_quality: PeriodQuality | None = None
    confidence_pct: int = Field(default=0, ge=0, le=100)
    period_indicator: str | None = None
    correlated_modules: list[str] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=utc_now)


class ArcAngelPillar1(StrictDocument):
    areas_completed: list[str] = Field(default_factory=list)
    social_sphere_areas_completed: list[str] = Field(default_factory=list)
    score: int = Field(default=0, ge=0, le=24)
    max_score: int = Field(default=24, ge=0)


class ArcAngelPillar2(StrictDocument):
    reports_run: list[str] = Field(default_factory=list)
    score: int = Field(default=0, ge=0, le=12)
    max_score: int = Field(default=12, ge=0)


class ArcAngelPillar3(StrictDocument):
    tarot_love_score: int = Field(default=0, ge=0, le=5)
    strategist_score: int = Field(default=0, ge=0, le=5)
    pillar_3_score: int = Field(default=0, ge=0, le=10)
    last_ritual_date: datetime | None = None
    decay_started_at: datetime | None = None
    max_score: int = Field(default=10, ge=0)
    note: str = "Decay engine wired in ARC-2. Sprint 3 reads stored pillar_3_score only."


class UserArcAngelProfileDocument(StrictDocument):
    user_id: str
    birth_date: str
    birth_time: str
    birth_place: str
    computed_at: datetime = Field(default_factory=utc_now)
    engine_label: str = "Vedic Astrology Engine Activated"
    overall_confidence_pct: int = Field(default=0, ge=0, le=100)
    pillar_1: ArcAngelPillar1 = Field(default_factory=ArcAngelPillar1)
    pillar_2: ArcAngelPillar2 = Field(default_factory=ArcAngelPillar2)
    pillar_3: ArcAngelPillar3 = Field(default_factory=ArcAngelPillar3)
    data_completeness: ArcAngelDataCompleteness = Field(default_factory=ArcAngelDataCompleteness)
    domains: list[ArcAngelDomainSnapshot] = Field(default_factory=list)


class ParentBirthIdentity(StrictDocument):
    dob: str
    pob_city: str
    current_city: str


class ParentsBirthData(StrictDocument):
    father: ParentBirthIdentity | None = None
    mother: ParentBirthIdentity | None = None


class ParentSimple(StrictDocument):
    dob: str | None = None
    place: str | None = None


class ParentsData(StrictDocument):
    father: ParentSimple | None = None
    mother: ParentSimple | None = None


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
    parents_data: ParentsData | None = None
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
    tension_blocks: list["TensionBlock"] = Field(default_factory=list)


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


class KnowledgeNarrativeDomain(StrictDocument):
    domain: str
    headline: str
    body: list[str] = Field(default_factory=list)
    lucky_elements: dict[str, Any] = Field(default_factory=dict)
    timing_window: str
    confidence_tier: ConfidenceBand
    tranche_adjusted: bool = False


class KnowledgeNarrativeRequest(StrictDocument):
    chart: dict[str, Any] = Field(default_factory=dict)
    categories: list[str] = Field(default_factory=list)
    max_rules: int = Field(default=50, ge=1, le=100)
    context: KnowledgeRequestContext = Field(default_factory=KnowledgeRequestContext)
    tension_blocks: list[TensionBlock] = Field(default_factory=list)
    user_context: dict[str, Any] = Field(default_factory=dict)
    author_voice_id: str | None = None
    model: str | None = None


class KnowledgeNarrativeResponse(StrictDocument):
    rule_count: int = Field(default=0, ge=0)
    matched_domains: list[str] = Field(default_factory=list)
    narratives: list[KnowledgeNarrativeDomain] = Field(default_factory=list)
    author_voice_id: str | None = None
    model: str | None = None
    error: str | None = None


KnowledgeRequestContext.model_rebuild()


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
