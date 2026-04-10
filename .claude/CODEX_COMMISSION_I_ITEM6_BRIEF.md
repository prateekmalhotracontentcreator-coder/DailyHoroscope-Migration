# Codex Brief — Commission I CPath-1 Item 6: Brihat Kundali × Knowledge Engine

> To: Codex  
> From: EverydayHoroscope / Temple Team  
> CPath-1 Item: 6 of 8  
> Priority: HIGH — first live user-facing KE output  
> Depends on: Items 1–5 (all committed ✅)

---

## What This Item Is

Wire the Knowledge Engine into the existing Brihat Kundali Pro report generation.
When a user generates a Brihat Kundali, the backend will now run `scan_chart()` +
`generate_narrative()` **concurrently** with the existing Claude LLM call, then store
the resulting Knowledge Engine narratives in the report. The frontend adds one new
section — "Insights from Classical Texts" — that renders these narratives when present.

No new endpoints. No new pages. Two file edits only.

---

## Files to Edit

| File | Type of change |
|---|---|
| `backend/server.py` | Add KE field to model + helper fn + parallel execution |
| `frontend/src/pages/BrihatKundliPage.jsx` | Add one new section in `ReportDisplay` |

---

## 1. Backend — `backend/server.py`

### Change A — Add `knowledge_narratives` field to `BrihatKundliReport`

Current model (lines 277–287):
```python
class BrihatKundliReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ...
    chart_svg: str = ""
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

Add ONE field before `generated_at`:
```python
    knowledge_narratives: list = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

`model_config = ConfigDict(extra="ignore")` means the field MUST be declared explicitly —
it will not be stored unless it is on the model.

### Change B — Add `_brihat_ke_pipeline()` helper

Add this function anywhere before `generate_brihat_kundli_with_llm()` (i.e. before line 660).

```python
async def _brihat_ke_pipeline(chart_data: dict, engine) -> list:
    """
    Run scan_chart() + generate_narrative() for the Brihat Kundali report.
    Returns a list of plain dicts (one per Arc Angel domain matched).
    Returns [] on any failure — never raises.
    """
    try:
        # vedic_calculator returns sign_vedic; knowledge_engine reads sign — normalise
        raw_planets = chart_data.get("planets") or {}
        ke_planets = {
            pname: {**pdata, "sign": pdata.get("sign") or pdata.get("sign_vedic")}
            for pname, pdata in raw_planets.items()
        }
        ke_chart = {**chart_data, "planets": ke_planets}

        matched_rules = await engine.scan_chart(
            ke_chart,
            categories=["career", "wealth", "relationships", "health"],
            max_rules=30,
        )
        if not matched_rules:
            return []

        narrative_response = await engine.generate_narrative(
            matched_rules=matched_rules,
            chart=ke_chart,
            context={"backbone_science_id": "vedic_astrology"},
        )
        narratives = narrative_response.narratives or []
        # Convert Pydantic models to plain dicts for MongoDB storage
        return [
            n.model_dump() if hasattr(n, "model_dump") else dict(n)
            for n in narratives
        ]
    except Exception as ke_err:
        logging.warning("Knowledge Engine pipeline failed for Brihat Kundali: %s", ke_err)
        return []
```

### Change C — Run KE pipeline concurrently in `generate_brihat_kundli()`

The existing endpoint (around line 699–750) currently does:
```python
report_data = await generate_brihat_kundli_with_llm(request)
```

Replace that single `await` line with a parallel execution block:

```python
engine = getattr(request.app.state, "knowledge_engine", None)
if engine is not None and chart_data is not None:
    report_data, knowledge_narratives = await asyncio.gather(
        generate_brihat_kundli_with_llm(request),
        _brihat_ke_pipeline(chart_data, engine),
    )
else:
    report_data = await generate_brihat_kundli_with_llm(request)
    knowledge_narratives = []
```

Then pass `knowledge_narratives` into the `BrihatKundliReport(...)` constructor.
Find the `BrihatKundliReport(...)` call (line ~746) and add one keyword argument:
```python
knowledge_narratives=knowledge_narratives,
```

#### Why asyncio.gather here?
`generate_brihat_kundli_with_llm()` calls Claude (~8–10s).
`_brihat_ke_pipeline()` does an in-memory index scan (fast) then another Claude call (~8s).
Running both concurrently keeps total time at ~10s instead of ~18–20s sequential.

#### `asyncio` import
`asyncio` is already used in this file (it's a FastAPI app). If for any reason it is not
already imported, add `import asyncio` near the top imports.

---

## 2. Frontend — `frontend/src/pages/BrihatKundliPage.jsx`

### Add one section to `ReportDisplay`

After the Numerology section (currently the last section, ends around line 416) and
before the closing `</div>` of `ReportDisplay`, add:

```jsx
{/* Knowledge Engine — Insights from Classical Texts */}
{report.knowledge_narratives?.length > 0 && (
  <Section
    icon={BookOpen}
    title="Insights from Classical Texts"
    color="bg-gold/10 text-gold"
  >
    <div className="space-y-6">
      {report.knowledge_narratives.map((domain, i) => (
        <div key={i} className="space-y-2 pb-5 border-b border-border last:border-0 last:pb-0">
          <div className="flex items-start justify-between gap-3 flex-wrap">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-gold">
                {domain.domain}
              </p>
              <p className="font-playfair font-semibold text-base mt-0.5">
                {domain.headline}
              </p>
            </div>
            {domain.confidence_tier && (
              <Tag color="bg-gold/10 text-gold">{domain.confidence_tier}</Tag>
            )}
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed">{domain.body}</p>
          {domain.timing_window && (
            <p className="text-xs text-muted-foreground mt-1">
              Active period: {domain.timing_window}
            </p>
          )}
          {domain.lucky_elements &&
            Object.keys(domain.lucky_elements).length > 0 && (
              <div className="flex flex-wrap gap-2 mt-2">
                {Object.entries(domain.lucky_elements).map(([k, v]) => (
                  <Tag key={k} color="bg-gold/10 text-gold">
                    {k}: {Array.isArray(v) ? v.join(', ') : v}
                  </Tag>
                ))}
              </div>
            )}
        </div>
      ))}
    </div>
  </Section>
)}
```

`BookOpen` is already imported at the top of `BrihatKundliPage.jsx`. `Tag` and `Section`
are already defined in the same file. No new imports needed.

---

## 3. Key Constraints

- **Graceful degradation** — if `knowledge_engine` is not on `app.state` (cold start,
  engine init failed, or unit test), the `else` branch runs and `knowledge_narratives = []`.
  The rest of the report is unaffected.
- **No new files** — both changes are edits to existing files.
- **No new npm packages** — no frontend dependency changes.
- **No smart/curly quotes** in JSX.
- **`asyncio.gather()` not `await A; await B`** — sequential would double latency.
- **`model_config = ConfigDict(extra="ignore")`** means the field must be declared
  on the Pydantic model — do not rely on `**kwargs` to pass it through.
- **KnowledgeNarrativeDomain** fields returned by `generate_narrative()`:
  `domain` (str), `headline` (str), `body` (str), `lucky_elements` (dict),
  `timing_window` (str | None), `confidence_tier` ("LOW" | "MEDIUM" | "HIGH" | "VERIFIED")

---

## 4. Validation Checklist (Codex self-check before submitting)

- [ ] `knowledge_narratives: list = Field(default_factory=list)` added to `BrihatKundliReport`
- [ ] `_brihat_ke_pipeline()` is defined before `generate_brihat_kundli_with_llm()`
- [ ] `asyncio.gather()` used — NOT sequential awaits
- [ ] `sign_vedic` → `sign` normalisation present in `_brihat_ke_pipeline()`
- [ ] `knowledge_narratives=knowledge_narratives` passed into `BrihatKundliReport(...)` constructor
- [ ] New JSX section renders only when `report.knowledge_narratives?.length > 0`
- [ ] No new imports needed (BookOpen, Tag, Section already in scope)
- [ ] No curly/smart quotes in JSX

---

## 5. What the Temple Team Will Do After Receiving This Code

1. Review `_brihat_ke_pipeline()` normalisation logic
2. Verify `asyncio.gather()` call is syntactically correct within the existing try/except
3. Verify JSX section renders correctly and `BookOpen` icon is in scope
4. Commit as: `feat(knowledge-engine): CPath-1 item 6 — Brihat Kundali × Knowledge Engine`
