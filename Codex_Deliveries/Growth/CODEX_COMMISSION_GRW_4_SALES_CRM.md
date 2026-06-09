# Codex Commission: GRW-4 -- B2B Sales Lead CRM (Light)
> **Module:** Growth -- Sales Pipeline
> **Issued:** 2026-06-08 | **Priority:** Medium
> **Depends on:** Nothing. Pure admin CRUD.

---

## 1. What This Builds

A lightweight **B2B Sales Pipeline** inside the Admin Console. Manual entry only in Phase 1 -- no scraping, no external APIs. The admin records and tracks potential B2B partners (yoga apps, wellness platforms, matrimony sites, astrology portals) across a 5-stage pipeline.

---

## 2. Files to Create / Modify

```
backend/server.py                          ← 5 new CRUD endpoints
frontend/src/pages/admin/AdminDashboard.jsx ← New "Leads" tab
```

New MongoDB collection: `sales_leads`

---

## 3. `sales_leads` Collection Schema

```python
{
  "lead_id":      str,          # uuid, upsert key
  "created_at":  datetime,
  "updated_at":  datetime,

  # Company details
  "company_name":  str,         # required
  "website":       str,
  "industry":      str,         # "yoga_wellness" | "matrimony" | "astrology_portal" | "news_media" | "app" | "other"
  "country":       str,         # default "India"

  # Contact
  "contact_name":  str,
  "contact_email": str,
  "contact_phone": str,

  # Pipeline
  "stage":         str,         # "discovered" | "contacted" | "qualified" | "proposal_sent" | "closed_won" | "closed_lost"
  "alignment_score": int,       # 1-100, admin-assigned
  "deal_value_inr":  int,       # estimated monthly value ₹
  "partnership_type": str,      # "api_panchang" | "api_birth_chart" | "api_horoscope" | "content_sponsor" | "co_marketing" | "other"

  # Notes
  "notes":         str,         # free text
  "next_action":   str,         # "Send intro email" | "Follow up" | "Demo call" | etc.
  "next_action_date": datetime|None,
}
```

---

## 4. Backend Endpoints -- `server.py`

All under `/api/admin/sales-leads/`. All require `require_admin`.

```python
GET    /api/admin/sales-leads                  # list, filter by stage + industry
POST   /api/admin/sales-leads                  # create
PUT    /api/admin/sales-leads/{lead_id}        # update any field
DELETE /api/admin/sales-leads/{lead_id}        # soft-delete (set active=False)
GET    /api/admin/sales-leads/summary          # counts by stage
```

**Summary endpoint returns:**
```python
{
  "total": int,
  "by_stage": {
    "discovered":     int,
    "contacted":      int,
    "qualified":      int,
    "proposal_sent":  int,
    "closed_won":     int,
    "closed_lost":    int
  },
  "total_pipeline_value_inr": int,   # sum of deal_value_inr for non-closed-lost leads
  "avg_alignment_score": float
}
```

---

## 5. Admin UI -- "Leads" Tab

New top-level tab in Admin Dashboard (between Payments and Messages). Label: "Leads". Icon: `Target` (lucide-react).

### 5a -- Pipeline Summary (top of page)

6 stage cards in a row (or 2-row grid on mobile):
```
[Discovered: 4]  [Contacted: 2]  [Qualified: 1]  [Proposal: 0]  [Won: 0]  [Lost: 1]
Pipeline Value: ₹14,000/month est.
```

### 5b -- Lead Table

Sortable by `alignment_score` desc by default. Columns:

```
Company | Industry | Stage | Score | Deal ₹/mo | Next Action | [Edit] [Delete]
```

Filter bar: All stages dropdown + Industry dropdown + Search by name.

Stage shown as a coloured badge (same pattern as existing StatusBadge component):
- discovered = gray
- contacted = blue
- qualified = amber
- proposal_sent = purple
- closed_won = green
- closed_lost = red

### 5c -- Add/Edit Lead Drawer

Clicking [Add Lead] or [Edit] opens an inline panel (not modal) on the right side. Fields:

```
Company Name *         Website
Industry               Country
Contact Name           Contact Email
Contact Phone          Partnership Type
Stage                  Alignment Score (1-100)
Deal Value ₹/month     Next Action
Next Action Date       Notes (textarea)
```

[Save] and [Cancel] buttons at bottom. Validation: Company Name required.

### 5d -- Quick Stage Update

Clicking the stage badge opens a small inline dropdown to change stage without opening the full edit panel.

---

## 6. Acceptance Gates (6)

| Gate | Test |
|---|---|
| G-01 | `POST /api/admin/sales-leads` creates a document in `sales_leads` collection |
| G-02 | `GET /api/admin/sales-leads/summary` returns correct counts after adding 3 leads |
| G-03 | `PUT /api/admin/sales-leads/{id}` updates `stage` and `updated_at` |
| G-04 | Leads tab renders with summary cards and table |
| G-05 | Add Lead form validates required fields (Company Name empty → error shown, no save) |
| G-06 | Stage badge click → dropdown → stage updates without full page reload |

---

## 7. Constraints

- Phase 1: manual entry only. No SERPER integration (that is GRW-3).
- `alignment_score` is always admin-assigned -- never auto-calculated.
- Soft-delete only (`active: False`) -- no hard deletes.
- Commit: `feat(growth): GRW-4 B2B sales lead CRM`
