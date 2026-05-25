# Seed Scripts -- Render Shell Run Guide
> EverydayHoroscope · 2026-05-26

---

## Why the Error Occurred

The seed scripts (`seed_crystals.py`, etc.) were committed in the **c4434ff** commit on 2026-05-26.
If you ran the Render shell before the new Docker image finished building, the scripts were not yet present.

Render rebuilds the Docker image on every push to `main`. The image build takes ~3-5 minutes after push.

**Wait for the Render dashboard to show "Deploy live" before running seed scripts.**

---

## Correct Commands for Render Shell

In Render dashboard → `everydayhoroscope-api` → **Shell tab**, run from the `/app` directory:

```bash
# Crystals (50 crystals + 20 intentions = 70 docs)
python backend/scripts/seed_crystals.py

# Rudraksha (21 mukhis)
python backend/scripts/seed_rudraksha.py

# Lo Shu Grid
python backend/scripts/seed_lo_shu.py

# Zibu Symbols (88 symbols)
python backend/scripts/seed_zibu_symbols.py

# Angel Numbers -- IMPORTANT: run core FIRST, then intents
python backend/scripts/seed_angel_numbers_core.py
python backend/scripts/seed_angel_numbers_intents.py

# SEO-20K M3 seeds
python backend/scripts/seed_transit_profiles.py
python backend/scripts/seed_festival_regions.py
python backend/scripts/seed_character_placements.py
```

**Run one at a time.** Each prints a completion count when done. 

Angel Numbers intents (~9,000 docs) will take the longest -- approximately 2-3 minutes. Do not close the shell tab during this.

---

## If Script Still Says "No such file"

Check the deploy completed:
```bash
ls backend/scripts/seed_crystals.py
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
