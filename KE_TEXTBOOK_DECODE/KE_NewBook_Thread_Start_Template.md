# NEW BOOK DECODE -- Thread Start Message Template
> Fill in all [PLACEHOLDERS] before issuing to the thread.
> Do not change anything else.

---

**NEW BOOK DECODE -- [BOOK NAME]**

Read this message fully before doing anything else.

**Book:** [BOOK NAME]
**Full decode guide:** [GUIDE FILE PATH e.g. /Users/apple/DailyHoroscope-Migration/KE_XYZ_Decode_Guide.md]
**PDF folder:** [PDF FOLDER PATH e.g. /Users/apple/Documents/Knowledge Engine_eBooks/BookName/Chapters/]
**Output folder:** [OUTPUT FOLDER PATH e.g. /Users/apple/Documents/Knowledge Engine_eBooks/BookName_CC_Decode/]

---

**🔴 MANDATORY FIRST ACTION -- Execute before reading the guide**

Use the Write tool to create these 4 files now. One Write call per file:

| # | File path | Initial content |
|---|---|---|
| 1 | [OUTPUT FOLDER]/[FIRST_SECTION_ID]_Rules.json | `[]` |
| 2 | [OUTPUT FOLDER]/[FIRST_SECTION_ID]_DataTables.md | `# [Section Name] Data Tables\n\n[Writing in progress]` |
| 3 | [OUTPUT FOLDER]/[FIRST_SECTION_ID]_Summary.md | `# [Section Name] Technical Summary\n\n[Writing in progress]` |
| 4 | [OUTPUT FOLDER]/[FIRST_SECTION_ID]_Diagnostic.md | `# [Section Name] Diagnostic\n\n[Writing in progress]` |

**[FIRST_SECTION_ID]** = e.g. `Combo_Intro`, `LU_S01_FundamentalRules`, `H300_S01_FundamentalRules`

Then post one line in the context window:
> "4 files created for [Section Name]. Reading guide now."

---

**Then:** Read the full decode guide at the path above. Follow the Batch / Section Start Protocol in the guide for every subsequent section. Do not begin decoding until the guide is fully read.

**Output rule (non-negotiable):**
- Every section = 4 separate files, created before reading begins
- JSON rules = ≤25 per Write call; use Part files (`_Part1.json`, `_Part2.json`) for sections with >25 rules
- Context window = two lines per section maximum. Nothing else. Ever.

---

## Filling In This Template -- Quick Reference

| Placeholder | Where to find it |
|---|---|
| `[BOOK NAME]` | Book title |
| `[GUIDE FILE PATH]` | Path to the decode guide `.md` file in `/Users/apple/DailyHoroscope-Migration/` |
| `[PDF FOLDER PATH]` | Folder containing the source PDFs |
| `[OUTPUT FOLDER PATH]` | Folder for decoded output files (create it first if it doesn't exist) |
| `[FIRST_SECTION_ID]` | The file-naming prefix for the first section (from the guide's chapter/section map) |
| `[Section Name]` | Human-readable name of the first section to decode |
