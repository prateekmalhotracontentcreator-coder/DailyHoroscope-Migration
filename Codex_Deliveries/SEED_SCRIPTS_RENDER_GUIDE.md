# Seed Scripts -- Render Shell Run Guide
> EverydayHoroscope · 2026-05-26

---

## Why the Error Occurred

**Root cause:** `render.yaml` sets `dockerContext: ./backend`. This means Docker's build context
is the `backend/` folder -- so `COPY . .` copies backend contents directly into `/app/`.

Result:
- `backend/scripts/seed_crystals.py` in the repo → `/app/scripts/seed_crystals.py` on Render
- Running `python backend/scripts/seed_crystals.py` looks for `/app/backend/scripts/seed_crystals.py` ← does NOT exist
- **Correct path is `python scripts/seed_crystals.py`** (no `backend/` prefix)

Render rebuilds the Docker image on every push to `main`. The image build takes ~3-5 minutes after push.
**Wait for the Render dashboard to show "Deploy live" before running seed scripts.**

---

## Correct Commands for Render Shell

In Render dashboard → `everydayhoroscope-api` → **Shell tab**, run from the `/app` directory:

```bash
# Crystals (50 crystals + 20 intentions = 70 docs)
python scripts/seed_crystals.py

# Rudraksha (21 mukhis)
python scripts/seed_rudraksha.py

# Lo Shu Grid
python scripts/seed_lo_shu.py

# Zibu Symbols (88 symbols)
python scripts/seed_zibu_symbols.py

# Angel Numbers -- IMPORTANT: run core FIRST, then intents
python scripts/seed_angel_numbers_core.py
python scripts/seed_angel_numbers_intents.py

# SEO-20K M3 seeds
python scripts/seed_transit_profiles_v1.py
python scripts/seed_festival_region_pages_v1.py
python scripts/seed_character_placements_v1.py
```

**Run one at a time.** Each prints a completion count when done. 

Angel Numbers intents (~9,000 docs) will take the longest -- approximately 2-3 minutes. Do not close the shell tab during this.

---

## If Script Still Says "No such file"

Check the deploy completed and confirm the correct path:
```bash
ls scripts/seed_crystals.py
```

If missing, the deploy image hasn't rebuilt yet. Trigger a manual redeploy in Render dashboard → Manual Deploy.

---

## Verify a Seed Ran Correctly

After each seed, verify in Render shell:

```bash
# Crystals
python -c "import asyncio; from motor.motor_asyncio import AsyncIOMotorClient; import os; c=AsyncIOMotorClient(os.environ['MONGO_URL']); db=c[os.environ['DB_NAME']]; print(asyncio.run(db.crystals.count_documents({})))"

# Or simpler: hit the API directly after deploy
curl https://everydayhoroscope-api.onrender.com/api/crystals/amethyst | python3 -m json.tool | head -20
```
