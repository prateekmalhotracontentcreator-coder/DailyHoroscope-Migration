# Codex Brief -- Commission I CPath-1 Item 8: Tranche Filter UI Feedback

> To: Codex  
> From: EverydayHoroscope / Temple Team  
> CPath-1 Item: 8 of 8 -- FINAL ITEM  
> Priority: HIGH -- completes CPath-1  
> Depends on: Items 1-7 (all committed ✅)

---

## What This Item Is

Item 7 added the Tranche Filter. It marks dampened rules with `_tranche_adjusted = True`
but that signal currently stops there -- it never reaches the frontend.

Item 8 wires the signal all the way to the UI:

1. `KnowledgeNarrativeDomain` gets a new `tranche_adjusted: bool` field.
2. `generate_narrative()` computes which domains had adjusted rules and stamps the flag
   onto the correct narrative objects.
3. `BrihatKundliPage.jsx` renders a "Context-calibrated" badge on those domains and a
   one-line footnote explaining what it means.

Three small edits. No new files.

---

## Files to Edit

| File | Change |
|---|---|
| `backend/knowledge_schema.py` | Add `tranche_adjusted` field to `KnowledgeNarrativeDomain` |
| `backend/knowledge_engine.py` | Compute adjusted domains + stamp flag post-narrative |
| `frontend/src/pages/BrihatKundliPage.jsx` | Badge + footnote in Insights section |

---

## 1. `backend/knowledge_schema.py`

### Change -- add one field to `KnowledgeNarrativeDomain`

Current (lines 378-385):
```python
class KnowledgeNarrativeDomain(StrictDocument):
    domain: str
    headline: str
    body: list[str] = Field(default_factory=list)
    lucky_elements: dict[str, Any] = Field(default_factory=dict)
    timing_window: str
    confidence_tier: ConfidenceBand
```

Add `tranche_adjusted` as the last field:
```python
class KnowledgeNarrativeDomain(StrictDocument):
    domain: str
    headline: str
    body: list[str] = Field(default_factory=list)
    lucky_elements: dict[str, Any] = Field(default_factory=dict)
    timing_window: str
    confidence_tier: ConfidenceBand
    tranche_adjusted: bool = False
```

---

## 2. `backend/knowledge_engine.py`

Two small changes inside `generate_narrative()`.

### Change A -- Compute tranche-adjusted domains after the filter call

The filter call currently sits at around line 832:
```python
matched_rules = apply_tranche_filter(matched_rules, user_context or {})
```

Immediately after that line, add:
```python
tranche_adjusted_domains: set[str] = set()
for _rule in matched_rules:
    if _rule.get("_tranche_adjusted"):
        for _cat in (_rule.get("categories") or []):
            tranche_adjusted_domains.add(_category_to_domain(_cat))
```

`_category_to_domain()` is already defined in this module -- no new import needed.

### Change B -- Stamp the flag onto narratives after `_coerce_narratives()`

`_coerce_narratives()` is called inside `generate_narrative()` after the Claude response
is parsed. Find the line:
```python
narratives = _coerce_narratives(parsed["narratives"], matched_domains)
```

Immediately after it, add:
```python
if tranche_adjusted_domains:
    narratives = [
        n.model_copy(update={"tranche_adjusted": True})
        if n.domain in tranche_adjusted_domains
        else n
        for n in narratives
    ]
```

`model_copy(update={...})` is the correct Pydantic v2 pattern for producing a modified
copy of a model instance. It works on `StrictDocument` subclasses as long as the field
exists on the model.

### Also update `_coerce_narratives()`

`_coerce_narratives()` constructs each domain via `KnowledgeNarrativeDomain(**item)`.
Add a default so the model receives the field explicitly even before the post-process step:

In `_coerce_narratives()` (around line 682), after the existing `item.setdefault(...)` calls, add:
```python
item.setdefault("tranche_adjusted", False)
```

---

## 3. `frontend/src/pages/BrihatKundliPage.jsx`

The "Insights from Classical Texts" section is already rendered when
`report.knowledge_narratives?.length > 0` (added in item 6, around line 419).

### Change A -- "Context-calibrated" badge on adjusted domains

Inside the `.map()` loop for each domain, the header row currently looks like:
```jsx
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
```

Replace the badge group `<div>` (the right-side wrapper that currently holds
`confidence_tier`) with one that also conditionally renders the tranche badge:

```jsx
<div className="flex flex-wrap gap-2 items-center">
  {domain.tranche_adjusted && (
    <Tag color="bg-indigo-500/10 text-indigo-400">Context-calibrated</Tag>
  )}
  {domain.confidence_tier && (
    <Tag color="bg-gold/10 text-gold">{domain.confidence_tier}</Tag>
  )}
</div>
```

### Change B -- Footnote at the bottom of the section

After the closing `</div>` of the `.map()` container (after the last domain card),
and before the closing `</Section>`, add:

```jsx
{report.knowledge_narratives.some((d) => d.tranche_adjusted) && (
  <p className="text-xs text-muted-foreground mt-4 border-t border-border pt-3">
    * Context-calibrated domains have been adjusted based on your personal
    circumstances to reduce false negatives. Complete your profile to refine
    these insights further.
  </p>
)}
```

`Array.prototype.some()` is standard JS -- no new imports needed.

---

## 4. Constraints

- **No new files** -- three edits only.
- **`model_copy(update={...})`** -- Pydantic v2 only. Do not use `.copy(update=...)` (Pydantic v1 pattern).
- **`_category_to_domain()` is already in scope** in `knowledge_engine.py` -- do not re-import.
- **No new npm packages**.
- **No smart/curly quotes** in JSX.
- **`tranche_adjusted_domains` computation loop** must use the `matched_rules` list
  *after* `apply_tranche_filter()` has run -- not the original list.
- The footnote renders **only when at least one domain** has `tranche_adjusted=True`.
  When the questionnaire isn't filled in yet, `user_context={}` means the filter
  passes through unchanged and `tranche_adjusted` stays `False` on all domains --
  so neither badge nor footnote will appear for current users. This is correct behaviour.

---

## 5. Validation Checklist (Codex self-check)

- [ ] `tranche_adjusted: bool = False` present on `KnowledgeNarrativeDomain`
- [ ] `item.setdefault("tranche_adjusted", False)` added in `_coerce_narratives()`
- [ ] `tranche_adjusted_domains` set is computed immediately after `apply_tranche_filter()`
- [ ] `model_copy(update={"tranche_adjusted": True})` called only when `tranche_adjusted_domains` is non-empty
- [ ] Narratives whose `n.domain` is NOT in `tranche_adjusted_domains` are passed through unchanged (`else n`)
- [ ] Frontend badge renders only when `domain.tranche_adjusted` is truthy
- [ ] Footnote renders only when `some(d => d.tranche_adjusted)` is true
- [ ] No curly/smart quotes in JSX

---

## 6. What the Temple Team Will Do

1. Verify `model_copy(update=...)` syntax is Pydantic v2 correct
2. Verify domain name matching: `_category_to_domain(category)` in the engine must
   produce the same strings as `n.domain` in the narrative response
3. Check JSX section renders cleanly -- no import gaps
4. Commit as: `feat(knowledge-engine): CPath-1 item 8 -- Tranche Filter UI feedback`

---

## 7. After Item 8 -- CPath-1 Complete

Once item 8 is merged, CPath-1 (all 8 items) is complete and Phase 1.2 begins:
- Arc Angel backend (UserArcAngelProfileDocument, domain snapshot generation)
- Case Study backend (CaseStudyDocument CRUD, validation pipeline seed)
- Science Registry seed data
