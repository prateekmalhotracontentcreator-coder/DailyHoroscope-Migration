#!/usr/bin/env python3
"""
300H2 Full Decode -- Thread 4 · Step 2
Decodes Ch004-Ch153 (150 horoscope chapters) from
"A Book of 300 Important Horoscopes Vol-1 Part-2"
and outputs test vector JSONs + gap report + case-derived rules skeleton.

Schema version: tv_300h2_decode_v1 (post Pre-Decode review, 2026-06-05)
"""

import pdfplumber
import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta

# ── Paths ──────────────────────────────────────────────────────────────────────
CHAPTERS_DIR = "/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/300 Horoscope Vol2/Chapters"
OUTPUT_DIR   = "/Users/apple/DailyHoroscope-Migration/KE_TEXTBOOK_DECODE/Test_Vectors/JSON/300h2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Constants ──────────────────────────────────────────────────────────────────
SKIP_CHAPTERS = {1, 2, 3}   # Front Matter, Page Index, Introduction & Rules

SIGN_MAP = {
    'Ar': 'Aries',    'Ta': 'Taurus',      'Ge': 'Gemini',      'Cn': 'Cancer',
    'Le': 'Leo',      'Vi': 'Virgo',       'Li': 'Libra',       'Sc': 'Scorpio',
    'Sg': 'Sagittarius', 'Cp': 'Capricorn','Aq': 'Aquarius',    'Pi': 'Pisces',
}

MONTH_MAP = {
    'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
    'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12,
}

PLANET_NAMES = ['SUN','MOON','MARS','MERCURY','JUPITER','VENUS','SATURN','RAHU','KETU']

# ── Helpers: text cleaning ─────────────────────────────────────────────────────
def extract_raw_text(pdf_path):
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            pages.append(p.extract_text() or "")
    return "\n".join(pages)

def clean_lines(raw):
    """Remove header/footer noise, return list of cleaned non-empty lines."""
    out = []
    for line in raw.split('\n'):
        line = line.strip()
        if not line:
            continue
        if 'NAIRS PUBLISHING HOUSE' in line:
            continue
        if re.match(r'^BOOK OF 300 IMPORTANT', line, re.IGNORECASE):
            continue
        # OCR renders "BOOK" as "00" / "Bo" / garbage on some pages
        if re.search(r'\bof 300 [Ii]mportant [Hh]oro', line, re.IGNORECASE):
            continue
        if re.match(r'^Page#\s*\d', line, re.IGNORECASE):
            continue
        out.append(line)
    return out

# ── Helpers: date / time / coords ─────────────────────────────────────────────
def parse_date(s):
    if not s:
        return None
    s = re.sub(r'(\d{3})-(\d\b)', lambda m: m.group(1)+m.group(2), s)  # "194-4" → "1944"
    s = re.sub(r'\b(\d)-(\d{3})', lambda m: m.group(1)+m.group(2), s)  # "1-956" → "1956"

    # "Oct-11-1942" / "Oct 11, 1942" / "October 11, 1942"
    m = re.search(
        r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[,.\s\-]+(\d{1,2})[,.\s\-]+(\d{3,4})',
        s, re.IGNORECASE)
    if m:
        mo = MONTH_MAP.get(m.group(1).lower()[:3])
        return f"{int(m.group(3)):04d}-{mo:02d}-{int(m.group(2)):02d}" if mo else None

    # "24 December 1845" / "24, December, 1845"
    m = re.search(
        r'(\d{1,2})[,.\s]+([a-z]{3,9})[,.\s]+(\d{3,4})',
        s, re.IGNORECASE)
    if m:
        mo = MONTH_MAP.get(m.group(2).lower()[:3])
        return f"{int(m.group(3)):04d}-{mo:02d}-{int(m.group(1)):02d}" if mo else None

    # "December, 24, 1845"
    m = re.search(
        r'([a-z]{3,9})[,.\s]+(\d{1,2})[,.\s]+(\d{3,4})',
        s, re.IGNORECASE)
    if m:
        mo = MONTH_MAP.get(m.group(1).lower()[:3])
        return f"{int(m.group(3)):04d}-{mo:02d}-{int(m.group(2)):02d}" if mo else None

    return None

def parse_time_tz(s):
    """Return (time_local_str, tz_offset_float) from OCR time block."""
    if not s:
        return None, None
    m = re.search(r'(\d{1,2}):(\d{2})(?::(\d{2}))?', s)
    time_local = None
    if m:
        h, mn = int(m.group(1)), int(m.group(2))
        sc = int(m.group(3)) if m.group(3) else 0
        time_local = f"{h:02d}:{mn:02d}:{sc:02d}"

    # "(5:30 east)" / "(5.30)" / "(2:00)" / "(0:00 west)" / "(0:00 wost)" [OCR variant]
    tz_match = re.search(r'\(\s*(\d+)[:.]\s*(\d+)\s*([a-zA-Z]+)?\s*\)', s, re.IGNORECASE)
    tz_offset = None
    if tz_match:
        try:
            tz_offset = int(tz_match.group(1)) + int(tz_match.group(2)) / 60.0
            direction = (tz_match.group(3) or '').lower()
            # starts-with 'w' covers: west, w, wost (OCR artifact for west)
            if direction.startswith('w'):
                tz_offset = -tz_offset
            # starts-with 'e' covers: east, e, eas -- positive (default, no-op)
        except:
            pass
    # Simple integer: "(5)" alone
    if tz_offset is None:
        m2 = re.search(r'\(\s*(\d+)\s*([a-zA-Z]+)?\s*\)', s, re.IGNORECASE)
        if m2:
            try:
                tz_offset = float(m2.group(1))
                direction2 = (m2.group(2) or '').lower()
                if direction2.startswith('w'):
                    tz_offset = -tz_offset
            except:
                pass

    return time_local, tz_offset

def parse_coords(s):
    """Return (lat, lon) floats from OCR coordinate string."""
    if not s:
        return None, None

    # "81 E 56, 26 N 26" or "81E56,26N26"
    m = re.search(
        r'(\d{1,3})\s*([EeWw])\s*(\d{1,2})[,\s]+(\d{1,2})\s*([NnSs])\s*(\d{1,2})',
        s)
    if m:
        lon = int(m.group(1)) + int(m.group(3))/60.0
        if m.group(2).upper() == 'W': lon = -lon
        lat = int(m.group(4)) + int(m.group(6))/60.0
        if m.group(5).upper() == 'S': lat = -lat
        return round(lat,4), round(lon,4)

    # "0W7, 51N30"
    m = re.search(
        r'(\d{1,3})([EeWw])(\d{1,2})[,\s]+(\d{1,2})([NnSs])(\d{1,2})',
        s)
    if m:
        lon = int(m.group(1)) + int(m.group(3))/60.0
        if m.group(2).upper() == 'W': lon = -lon
        lat = int(m.group(4)) + int(m.group(6))/60.0
        if m.group(5).upper() == 'S': lat = -lat
        return round(lat,4), round(lon,4)

    return None, None

# ── Helpers: chart parsing ─────────────────────────────────────────────────────
def parse_body_table(lines):
    """Parse Body Longitude table rows. Returns dict keyed by planet/LAGNA."""
    positions = {}
    # Matches both spaced ("18 Ta 19' 23") and compact ("18Ta19'23") formats.
    # Signification tail extended to handle OCR artifacts: ·, ~
    row_re = re.compile(
        r'^(Lagna|Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)'
        r'(?:\s*\(R\))?\s+'
        r'(\d{1,2})\s*([A-Z][a-z])\s*(\d{1,2})\'?\s*(\d{1,2})?\s+'
        r'([A-Za-z]+)\s+'
        r'([1-4])\s+'
        r'([\d,A-Za-z\s.\-·~]+)',
        re.IGNORECASE
    )
    for line in lines:
        m = row_re.match(line)
        if not m:
            continue
        planet   = m.group(1).upper()
        deg_int  = int(m.group(2))
        sign_key = m.group(3)
        deg_min  = int(m.group(4))
        deg_sec  = int(m.group(5)) if m.group(5) else 0
        naksh    = m.group(6).strip()
        pada     = int(m.group(7))
        sigs_raw = m.group(8).strip().rstrip(',').strip()
        retrograde = bool(re.search(r'\(R\)', line, re.IGNORECASE))

        degree = round(deg_int + deg_min/60.0 + deg_sec/3600.0, 3)
        sign   = SIGN_MAP.get(sign_key)

        # Parse significations -- house numbers only (ignore Ra/Ke/Mo planet refs)
        sig_parts = [s.strip() for s in re.split(r'[,\s]+', sigs_raw) if s.strip()]
        sig_houses = []
        for sp in sig_parts:
            try:
                sig_houses.append(int(sp))
            except ValueError:
                pass   # planet-name refs (Ra, Ke, etc.) -- skip for now

        positions[planet] = {
            "sign":             sign,
            "degree":           degree,
            "house":            None,   # Phase 4 CC computation
            "nakshatra":        naksh,
            "pada":             pada,
            "retrograde":       retrograde,
            "significations":   sig_houses,
            "significations_raw": sigs_raw,
        }
    return positions

def parse_kp_special_points(raw_text):
    """Extract HL and GL degree/sign from chart header OCR.

    Handles variants:
      "HL.: 25 G. 13"   -- OCR "G." for Gemini, spaces between components
      "HL: 22 Ta 55"    -- spaces between sign and minutes
      "GL: 7 Sg33"      -- no space between sign and minutes
      "HL=25Ge13"       -- no spaces at all
    """
    # Single-char OCR expansions for sign abbreviations
    _SINGLE = {'G': 'Ge', 'C': 'Cn', 'L': 'Le', 'V': 'Vi',
               'P': 'Pi', 'A': 'Ar', 'S': 'Sc', 'T': 'Ta'}

    def extract_point(label, text):
        # Degree: 1-2 digits; sign: 1-2 letters optionally followed by '.'; minutes: 1-2 digits
        m = re.search(
            label + r'\.?\s*[=:]\s*(\d{1,2})\s*([A-Z][a-zA-Z]?\.?)\s*(\d{1,2})',
            text)
        if m:
            deg_d = int(m.group(1))
            deg_m = int(m.group(3))
            deg   = round(deg_d + deg_m / 60.0, 2)
            raw_sign = m.group(2).rstrip('.')   # strip trailing period from "G."
            if len(raw_sign) == 1:
                raw_sign = _SINGLE.get(raw_sign.upper(), raw_sign)
            sign = SIGN_MAP.get(raw_sign[:2])
            return {"sign": sign, "degree": deg}
        return {"sign": None, "degree": None}

    return {
        "hora_lagna":  extract_point(r'HL', raw_text),
        "ghati_lagna": extract_point(r'GL', raw_text),
    }

def parse_lagna_from_header(raw_text):
    """Extract As:/Ae:/Aa: lagna from abbreviated chart header."""
    m = re.search(r'A[sea][.:]\s*(\d{1,2})\s*([A-Z][a-z])\s*(\d{1,2})', raw_text)
    if m:
        deg = round(int(m.group(1)) + int(m.group(3))/60.0, 2)
        sign = SIGN_MAP.get(m.group(2))
        return sign, deg
    return None, None

# ── Helpers: text extraction ───────────────────────────────────────────────────
def get_chapter_title(lines):
    return lines[0] if lines else None

def get_bio_intro(lines, title):
    """Return bio intro text: lines after title, before birth data block."""
    bio = []
    past_title = False
    for line in lines:
        if not past_title:
            if line == title:
                past_title = True
            continue
        # Stop at birth data, chart header, or body table
        if re.search(r'Date\s*[/I]\s*time|Nakshatra\s*:|Ayanam[sb]a\s*:|Body\s+Longitude',
                     line, re.IGNORECASE):
            break
        if re.match(r'^A[sea][.:]\s*\d', line, re.IGNORECASE):
            break
        if re.match(r'^(Lagna|Sun|Moon|Mars)\s+\d', line, re.IGNORECASE):
            break
        bio.append(line)
        if len(bio) >= 6:
            break
    return ' '.join(bio).strip() or None

def get_birth_data_block(lines):
    """Find and return the multi-line birth data block as one string."""
    block_lines = []
    in_block = False
    for line in lines:
        if re.search(r'Date\s*[/I]\s*time|Nakshatra\s*:|Ayanam[sb]a\s*:', line, re.IGNORECASE):
            in_block = True
        if in_block:
            block_lines.append(line)
            if re.search(r'Ayanam[sb]a\s*:', line, re.IGNORECASE):
                break  # end of block
            if len(block_lines) > 12:
                break
    return '\n'.join(block_lines)

def get_analysis_text(lines):
    """Extract author's analysis -- text after the last planet row (Ketu)."""
    last_planet_idx = None
    for i, line in enumerate(lines):
        if re.match(
            r'^(Lagna|Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)(?:\s*\(R\))?\s+\d',
            line, re.IGNORECASE
        ):
            last_planet_idx = i

    if last_planet_idx is None:
        return None

    analysis = []
    for line in lines[last_planet_idx + 1:]:
        line = line.strip()
        if not line:
            continue
        # Skip leftover table artefacts (single numbers, stray chars)
        if re.match(r'^[\d,\s.]{1,10}$', line):
            continue
        analysis.append(line)

    return ' '.join(analysis).strip() or None

# ── Helpers: death detection ───────────────────────────────────────────────────
DEATH_KEYWORDS = {
    'violent':   ['assassinat','shot','killed','murder','stabbed','gunned','lynched'],
    'execution': ['execut','hanged','guillot','firing squad'],
    'suicide':   ['suicide','took her own life','took his own life','drowned herself',
                  'drowned himself','self-inflict'],
    'accident':  ['accident','crash','wreck','drowned','fire'],
    'disease':   ['cancer','heart attack','illness','disease','died of','natural causes'],
}

def infer_death_type(text):
    t = text.lower()
    for dtype, keywords in DEATH_KEYWORDS.items():
        if any(k in t for k in keywords):
            return dtype
    if re.search(r'\bdied\b|\bdeath\b', t):
        return 'unknown'
    return None

def extract_death_date_from_bio(bio):
    """Look for (DOB - DEATH) date range in bio."""
    # Pattern: "(25 Jan 1882 - 28 Mar 1941)" or "(1845 - 1913)"
    m = re.search(
        r'\(([^)]+?\d{4})\s*[-\-]\s*([^)]+?\d{4})\)',
        bio or ''
    )
    if not m:
        return None
    return parse_date(m.group(2).strip())

def build_death_data(bio, analysis):
    """Construct death_data dict from bio intro + analysis text.

    IMPORTANT: death_type is inferred from bio ONLY.
    The analysis text uses KP house labels like "06th lord (disease)" and
    "8th house" in a purely technical context -- those must not trigger
    false death-type classifications for living subjects.
    We still check analysis for the PRESENCE of a death signal (e.g.
    "sudden exit") but the TYPE comes from bio alone.
    """
    # Type from bio only
    death_type = infer_death_type(bio or '')

    # Extract death date early -- a confirmed date range (DOB-death) is itself a signal
    death_date = extract_death_date_from_bio(bio or '')

    # Presence check uses both bio and analysis, plus the existence of a parsed death date
    combined = (bio or '') + ' ' + (analysis or '')
    has_death_signal = (
        death_type is not None
        or death_date is not None
        or bool(re.search(
            r'sudden exit|exit|killed|assassinat|execut|died\b|death\b|longevity|8[rt][ht]\s*house',
            combined.lower()))
    )

    if not has_death_signal:
        return None

    # Refine cause from bio sentences
    cause = None
    bio_l = (bio or '').lower()
    if 'assassination' in bio_l or 'assassinated' in bio_l:
        cause = "Assassination"
    elif 'executed' in bio_l or 'execution' in bio_l:
        cause = "Execution -- state-ordered"
    elif 'suicide' in bio_l:
        cause = "Suicide"
    elif 'accident' in bio_l:
        cause = "Accident"
    elif death_type == 'violent':
        cause = "Violent death"
    elif death_type == 'unknown' and 'sudden exit' in (analysis or '').lower():
        cause = None   # Implied astrologically only

    return {
        "cause_of_death":  cause,
        "death_type":      death_type,
        "death_date":      death_date,
        "age_at_death":    None,       # Phase 4
        "dasha_at_death": {
            "mahadasha":        None,
            "antardasha":       None,
            "pratyantardasha":  None,
            "sookshma":         None,
            "kp_significations": [],
            "stated_by_author": False,
            "cc_computed":      False,
            "raw_text":         None,
        },
        "additional_context": None,
    }

# ── Helpers: observations ──────────────────────────────────────────────────────
CAREER_KWS   = ['profession','job','career','president','minister','king','actor','singer',
                 'business','magnate','industry','politician','head of','became','join',
                 'film','high level']
LONGEVITY_KWS= ['death','exit','killed','murder','assassin','execut','longevity','maraka',
                 '8th','12th','8h','12h','sudden','violent','life span','short life']
MARRIAGE_KWS = ['marriage','wife','husband','marital','divorce','partner','love affair']
WEALTH_KWS   = ['wealth','rich','money','billionaire','business','fortune','salary']
HEALTH_KWS   = ['depress','disease','illness','mental','pain','disorder','deaf','dumb',
                 'blind','insane','disturbed']

def classify_axis(sentence):
    s = sentence.lower()
    if any(k in s for k in LONGEVITY_KWS):  return 'longevity'
    if any(k in s for k in MARRIAGE_KWS):   return 'marriage'
    if any(k in s for k in WEALTH_KWS):     return 'wealth'
    if any(k in s for k in HEALTH_KWS):     return 'health'
    if any(k in s for k in CAREER_KWS):     return 'career'
    return 'career'   # default

def classify_condition(sentence):
    s = sentence.lower()
    if re.search(r'is in star of', s):                     return 'kp_star_lord'
    if re.search(r'offers result of .+? through', s):      return 'kp_signification_chain'
    if re.search(r'all these combinations', s):            return 'kp_signification_chain'
    if re.search(r'signif\w+ \d+', s):                     return 'kp_planet_signification'
    if re.search(r'is in \d+[snrt][htd]\s*(house)?', s):   return 'planet_in_house'
    if re.search(r'aspects?\s+(lagna|\d)', s):             return 'kp_aspect'
    return 'kp_planet_signification'

def classify_polarity(sentence):
    s = sentence.lower()
    pos = ['helped','benefit','high level','fame','success','become','strong','rich',
           'prosper','auspicious','achieve','champion','known']
    neg = ['death','murder','killed','depress','disease','problem','humili','discord',
           'sudden exit','violence','fail','imprisonment','accident','corrupt','friction',
           'agony','suffer']
    if any(k in s for k in neg): return 'negative'
    if any(k in s for k in pos): return 'positive'
    return 'neutral'

GAP_TRIGGER_KWS = ['sudden exit','violent death','assassination','execution','shooting',
                   'shot','killed','murdered','maraka','badhaka','8th lord','12th lord',
                   'death axis','rahu ketu axis']

def extract_observations(analysis_text, subject_name=""):
    if not analysis_text:
        return []
    obs_list = []
    ctr = 1
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', analysis_text.strip())
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 20:
            continue
        # Skip artefact lines
        if re.match(r'^[\d,\s.~$%@#]{1,15}$', sent):
            continue
        axis      = classify_axis(sent)
        cond_type = classify_condition(sent)
        polarity  = classify_polarity(sent)
        gap_flag  = any(k in sent.lower() for k in GAP_TRIGGER_KWS)
        # Also flag death-axis observations that use unusual KP chains
        if axis == 'longevity' and cond_type == 'kp_star_lord':
            gap_flag = True

        obs_list.append({
            "obs_id":              f"obs-{ctr:03d}",
            "verbatim":            sent,
            "condition_type_guess": cond_type,
            "science_id":          "kp_jyotish",
            "claim_axis":          axis,
            "claim_polarity":      polarity,
            "gap_flag":            gap_flag,
            "potential_rule_id":   None,
        })
        ctr += 1
    return obs_list

# ── Helpers: subject metadata ──────────────────────────────────────────────────
SUBJECT_PREFIXES = [
    r'^SADIST[--\s]+',
    r'^AUTO MAGNATE\s+',
    r'^ASSASSIN[--\s]+',
    r'^FILM ICON\s*[.•\-]+\s*',
    r'^FILM ACTOR\s+(?:AND\s+POLITICIAN[--\s]+)?',
    r'^FILM ACTRESS\s+',
    r'^BOLLYWOOD ACTOR\s+',
    r'^BOLLYWOOD ACTRESS\s+',
    r'^ACTOR\s+',
    r'^ACTRESS\s+',
    r'^BRITISH WRITER[--\s]+',
    r'^US FIRST LADY[--\s]+',
    r'^FIRST LADY[--\s]+',
    r'^PRESIDENT\s+(?:#\d+\s*[--\s]+)?',
    r'^PRIME MINISTER[--\s]+',
    r'^PRIME MINISTER\s+',
    r'^CHIEF MINISTER[--\s]+',
    r'^CHIEF MINISTER\s+',
    r'^CHIEF MINSTER\s+',
    r'^ROMANIAN LEADER[--\s]+',
    r'^PAKISTAN PRIME MINISTER[--\s]+',
    r'^SERIAL KILLER\s+',
    r'^KING\s+',
    r'^QUEEN\s+',
    r'^EMPEROR\s+',
    r'^EMPRESS\s+',
    r'^PRINCE\s+',
    r'^PRINCESS\s+',
    r'^POPE\s+',
    r'^SCIENTIST\s+',
    r'^NOVELIST\s+',
    r'^WORLD FAMOUS DUTCH PAINTER[--\s]+',
    r'^POLITICIAN\s+',
    r'^MINISTER\s+',
    r'^VICE PRESIDENT\s+',
    r'^DY\.\s+PRIME MINISTER\s+',
    r'^DIWAN\s+(?:SIR\s+)?',
    r'^GENERAL\s+',
    r'^TENNIS LEGEND\s+',
    r'^MUGHAL EMPEROR\s+',
    r'^REVOLUTIONARY\s+',
    r'^INDUSTRIALIST\s+',
    r'^BILLIONAIRE\s+',
    r'^BUSINESSMAN\s+',
    r'^PLAY\s*BACK SINGER\s+',
    r'^SINGER[--\s]+',
    r'^GURU\s+',
    r'^SWAMI\s+',
    r'^CIVIL RIGHTS ACTIVIST\s+',
    r'^GEORGE I,\s+',
    r'^PLAY BACK SINGER\s+',
    r'^POLICE OFFICER\s+',
    r'^CAPT\.\s+',
    r'^SIR\s+',
    r'^DR\.\s+',
]

OCR_FIXES = {
    'Ceau~Escu': 'Ceausescu', 'Ceau?Escu': 'Ceausescu',
    'Ceau!?Escu': 'Ceausescu',
    'Sl Rhan': 'Sirhan', 'S1Rhan': 'Sirhan',
    'Bachchan Nee Srivastava': 'Bachchan',
}

def clean_subject_name(title_raw):
    """Strip role prefix from chapter title to get subject name."""
    if not title_raw:
        return None
    name = title_raw.strip()
    for prefix in SUBJECT_PREFIXES:
        stripped = re.sub(prefix, '', name, count=1, flags=re.IGNORECASE).strip()
        if stripped != name:
            name = stripped
            break
    # Title-case
    name = name.title()
    # Apply OCR fixes
    for bad, good in OCR_FIXES.items():
        name = re.sub(bad, good, name, flags=re.IGNORECASE)
    # Remove trailing punctuation
    name = name.strip('.--')
    return name or None

PROFESSION_RULES = [
    (['president','prime minister','chief minister','secretary general','governor',
      'senator','minister of','minister sahib','vice president','politician',
      'diwan','billionaire donald trump'],
     'Politician', 'Politics'),
    (['king','queen','emperor','empress','prince','princess','royalt'],
     'Royalty', 'Royalty'),
    (['actor','actress','film','bollywood','singer','musician','playback',
      'tv personality'],
     'Entertainer', 'Entertainment'),
    (['assassin','sadist','serial killer'],
     'Criminal', 'Crime'),
    (['general','army','military','air force','capt.','captain'],
     'Military', 'Military'),
    (['pope','bishop','swami','guru','spiritual','yogananda','saraswati'],
     'Religious Leader', 'Religion'),
    (['scientist','physicist','mathematician','bhabha','ramanujan'],
     'Scientist', 'Science'),
    (['novelist','writer','author'],
     'Writer', 'Literature'),
    (['billionaire','businessman','industrialist','magnate','tycoon',
      'ford motor','microsoft','ambani','ratan tata','bloomberg','buffet',
      'rockefeller','murdoch','trump','armani','perot','griffin','mafatlal',
      'bajaj'],
     'Businessman', 'Business'),
    (['tennis','cricket','sport','borg'],
     'Sportsperson', 'Sports'),
    (['chief justice','judge'],
     'Jurist', 'Judiciary'),
    (['police officer','police','tippit'],
     'Law Enforcement', 'Law Enforcement'),
    (['medical doctor','transfer in job','salary','baby','child shall',
      'dumbness','deafness','richness'],
     'Anonymous Case', 'Special_Case'),
]

def infer_profession(title, bio):
    combined = (title + ' ' + bio).lower()
    for keywords, prof, cat in PROFESSION_RULES:
        if any(k in combined for k in keywords):
            return prof, cat
    return None, 'Unknown'

def infer_public_figure(name, bio):
    anon = ['medical doctor','transfer in job','baby girl','dumbness','salary',
            'finance director','police service','railway','engineer','predicted']
    return not any(k in (name+' '+bio).lower() for k in anon)

def infer_nationality(bio, title):
    combined = (bio + ' ' + title).lower()
    NAT = [
        ('Indian',      ['india','indian','bollywood','allahabad','delhi','mumbai','calcutta']),
        ('American',    ['american','usa','united states',' u.s.']),
        ('British',     ['british','england','english','uk ','united kingdom','london']),
        ('Pakistani',   ['pakistan','karachi']),
        ('Romanian',    ['romanian','romania','bucharest']),
        ('Russian',     ['russian','russia','soviet','ussr','moscow']),
        ('German',      ['german','germany']),
        ('Italian',     ['italian','italy','rome']),
        ('French',      ['french','france','paris']),
        ('Portuguese',  ['portuguese','portugal','lisbon']),
        ('Greek',       ['greek','greece','hellenes','athens']),
        ('Spanish',     ['spanish','spain','madrid']),
        ('Japanese',    ['japanese','japan','tokyo','emperor of japan']),
        ('Dutch',       ['dutch','netherlands','holland','amsterdam']),
        ('Israeli',     ['israel','jerusalem','tel aviv']),
    ]
    for nat, hints in NAT:
        if any(h in combined for h in hints):
            return nat
    return None

def extract_key_events_from_bio(bio):
    if not bio:
        return []
    events = []
    # Birth-death range "(25 Jan 1882 - 28 Mar 1941)"
    m = re.search(
        r'\([^)]*?(\d{4})\s*[-\-]\s*[^)]*?(\d{4})\)',
        bio)
    if m:
        events.append({"event": "Born",  "year": int(m.group(1))})
        events.append({"event": "Died",  "year": int(m.group(2))})
    # Tenure years e.g. "(1988-1990)"
    for m2 in re.finditer(r'\((\d{4})[-\-](\d{4})\)', bio):
        events.append({"event": "Tenure", "year": int(m2.group(1))})
    return events

# ── Main decoder ───────────────────────────────────────────────────────────────
def decode_chapter(pdf_path, chapter_num, filename):
    """Return (json_dict, error_str)."""
    try:
        raw   = extract_raw_text(pdf_path)
    except Exception as e:
        return None, str(e)

    lines = clean_lines(raw)
    if not lines:
        return None, "Empty text after cleaning"

    title        = get_chapter_title(lines)
    subject_name = clean_subject_name(title or "")
    bio          = get_bio_intro(lines, title or "")
    birth_block  = get_birth_data_block(lines)
    analysis     = get_analysis_text(lines)

    # Birth data
    # Use full raw text for date search (sometimes date is spread across lines near chart)
    combined_block = birth_block + ' ' + raw[:2000]
    date_m   = re.search(
        r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[,.\s\-]+\d{1,2}[,.\s\-]+\d{3,4}'
        r'|\d{1,2}[,.\s]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[,.\s]+\d{3,4}'
        r'|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[,.\s\-]*\d{1,2}[,.\s\-]*\d{3,4})',
        combined_block, re.IGNORECASE)
    birth_date = parse_date(date_m.group(0) if date_m else None)

    time_m = re.search(r'\d{1,2}:\d{2}:\d{2}(?:\s*\([^)]+\))?', combined_block)
    time_local, tz_offset = parse_time_tz(time_m.group(0) if time_m else None)

    coord_m = re.search(
        r'\d{1,3}\s*[EeWw]\s*\d{1,2}[,\s]+\d{1,2}\s*[NnSs]\s*\d{1,2}'
        r'|\d{1,3}[EeWw]\d{1,2}[,\s]+\d{1,2}[NnSs]\d{1,2}',
        combined_block)
    lat, lon = parse_coords(coord_m.group(0) if coord_m else None)

    nak_m = re.search(r'Nakshatra[:\s]+([A-Za-z]+)', combined_block, re.IGNORECASE)
    nakshatra = nak_m.group(1).strip() if nak_m else None

    ayan_m = re.search(r'Ayanam[sb]a[:\s]+(\d{2}[\--]\d{2}[\--]\d{2}\.\d+)', combined_block, re.IGNORECASE)
    ayanamsha_stated = ayan_m.group(1).strip() if ayan_m else None

    # Time confidence
    is_pre1900 = False
    if birth_date:
        try:
            if int(birth_date[:4]) < 1900:
                is_pre1900 = True
        except:
            pass
    time_confidence = "rectified" if is_pre1900 else ("from_chart" if time_local else "unknown")

    # UTC time
    time_utc = None
    if birth_date and time_local and tz_offset is not None:
        try:
            dt_local = datetime.fromisoformat(f"{birth_date}T{time_local}")
            dt_utc   = dt_local - timedelta(hours=tz_offset)
            time_utc = dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        except:
            pass

    # Planet positions
    pos = parse_body_table(lines)
    lagna_entry = pos.pop('LAGNA', None)
    lagna_sign_table = lagna_entry["sign"]   if lagna_entry else None
    lagna_deg_table  = lagna_entry["degree"] if lagna_entry else None

    lagna_sign_hdr, lagna_deg_hdr = parse_lagna_from_header(raw)
    lagna_sign = lagna_sign_table or lagna_sign_hdr
    lagna_deg  = lagna_deg_table  or lagna_deg_hdr

    # Build planet_positions_from_table (all 9 planets)
    planet_positions = {}
    for p in PLANET_NAMES:
        entry = pos.get(p)
        if entry:
            planet_positions[p] = entry
        else:
            planet_positions[p] = {
                "sign": None, "degree": None, "house": None,
                "nakshatra": None, "pada": None, "retrograde": False,
                "significations": [], "significations_raw": "",
            }

    # KP special points
    kp_pts = parse_kp_special_points(raw)

    # Death data
    death_data = build_death_data(bio, analysis)

    # Observations
    observations = extract_observations(analysis or "", subject_name or "")

    # Profession / life outcomes
    profession, profession_category = infer_profession(title or "", bio or "")
    key_events = extract_key_events_from_bio(bio or "")

    # claim axes summary
    claim_axes = list({o["claim_axis"] for o in observations}) or ["career"]

    # IDs
    vector_id  = f"tv-300h2-ch{chapter_num:03d}"
    snake_name = re.sub(r'[^\w]', '_', (subject_name or 'unknown').lower())
    snake_name = re.sub(r'_+', '_', snake_name).strip('_')[:40]

    return {
        "vector_id":      vector_id,
        "book_id":        "300_horoscopes_vol1_part2",
        "source_chapter": filename.replace('.pdf',''),
        "pdf_path":       f"Chapters/{filename}",
        "public_figure":  infer_public_figure(subject_name or "", bio or ""),

        "subject": {
            "name":        subject_name,
            "description": ((bio or "")[:220] or None),
            "nationality": infer_nationality(bio or "", title or ""),
        },

        "birth_data": {
            "date":                 birth_date,
            "time_local":           time_local,
            "timezone_offset_hours": tz_offset,
            "time_utc":             time_utc,
            "latitude":             lat,
            "longitude":            lon,
            "place":                None,   # lat/lon only in book -- needs reverse geocoding
            "time_confidence":      time_confidence,
            "ayanamsha":            "lahiri",
            "ayanamsha_stated":     ayanamsha_stated,
            "nakshatra_stated":     nakshatra,
            "ocr_corrected":        False,
            "notes": (
                "Pre-1900 birth -- round time may indicate author rectification"
                if is_pre1900 else ""
            ),
        },

        "chart_verification": {
            "lagna_stated_in_book": lagna_sign,
            "lagna_degree_stated":  lagna_deg,
            "moon_sign_stated_in_book": None,
            "lagna_computed":       None,
            "moon_sign_computed":   None,
            "engine_matches_book":  None,
            "mismatch_notes":       "",
        },

        "planet_positions_from_table": planet_positions,

        "kp_special_points": kp_pts,

        "life_outcomes": {
            "profession":          profession,
            "profession_category": profession_category,
            "key_events":          key_events,
        },

        "death_data": death_data,
        "cross_reference": None,

        "layer_b_expected": {
            "profession_category": profession_category,
            "key_claim_axes":      claim_axes,
            "note": "",
        },

        "author_observations": observations,

        "rule_evaluation": {
            "evaluated":    False,
            "evaluated_at": None,
            "rules_fired":  [],
            "layer_a_pass": None,
            "layer_b_pass": None,
            "notes": "",
        },

        "test_status": {
            "extraction_complete": True,
            "chart_computed":      False,
            "rules_evaluated":     False,
        },
    }, None

# ── Combined-page handler (Ch069: Biden + Yoshihito) ──────────────────────────
def split_combined_chapter(json_obj, chapter_num, filename):
    """
    Ch069 contains Biden AND Yoshihito on one page.
    Return two JSON objects -- one per subject.
    """
    # Parse raw to find both subjects
    raw = extract_raw_text(os.path.join(CHAPTERS_DIR, filename))
    lines = clean_lines(raw)

    # Heuristic: find lines that look like titles for both subjects.
    # Deduplicate by tag so a repeated "Emperor Yoshihito" header line doesn't
    # fill both slots and crowd out Biden's fallback entry.
    subjects_found = []
    seen_tags = set()
    for i, line in enumerate(lines):
        if re.search(r'BIDEN|JOE BIDEN', line, re.IGNORECASE) and 'Biden' not in seen_tags:
            subjects_found.append(('Biden', i,
                                   "Joe Biden",
                                   "American politician; 47th Vice President / 46th President of the United States",
                                   "American"))
            seen_tags.add('Biden')
        elif re.search(r'YOSHIHITO|EMPEROR YOSHIHITO', line, re.IGNORECASE) and 'Yoshihito' not in seen_tags:
            subjects_found.append(('Yoshihito', i,
                                   "Emperor Yoshihito",
                                   "Emperor of Japan (Taisho era, 1912-1926)",
                                   "Japanese"))
            seen_tags.add('Yoshihito')

    # Require exactly 2 distinct subjects; otherwise use hard-coded fallback
    if len({s[0] for s in subjects_found}) < 2:
        subjects_found = [
            ('Biden',     0, "Joe Biden",
             "American politician; 47th Vice President / 46th President of the United States",
             "American"),
            ('Yoshihito', 1, "Emperor Yoshihito",
             "Emperor of Japan (Taisho era, 1912-1926)",
             "Japanese"),
        ]

    results = []
    for idx, (tag, _, name, desc, nationality) in enumerate(subjects_found[:2]):
        obj = dict(json_obj)
        obj = json.loads(json.dumps(obj))  # deep copy
        suffix = 'a' if idx == 0 else 'b'
        obj["vector_id"]      = f"tv-300h2-ch{chapter_num:03d}{suffix}"
        obj["combined_page"]  = True
        obj["combined_with"]  = subjects_found[1-idx][2] if len(subjects_found) == 2 else None
        obj["subject"]["name"]        = name
        obj["subject"]["description"] = desc
        obj["subject"]["nationality"] = nationality
        results.append(obj)
    return results

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    chapters = sorted(Path(CHAPTERS_DIR).glob("Ch*.pdf"))

    all_gap_obs   = []
    processed_map = {}   # chapter_num → vector_id
    errors        = []
    written       = 0

    print(f"Found {len(chapters)} chapter PDFs")
    print(f"Output: {OUTPUT_DIR}\n")

    for chapter_path in chapters:
        m = re.match(r'Ch(\d+)_(.+)\.pdf', chapter_path.name)
        if not m:
            continue
        chapter_num = int(m.group(1))
        slug        = m.group(2)

        if chapter_num in SKIP_CHAPTERS:
            print(f"  SKIP  Ch{chapter_num:03d}  (non-horoscope)")
            continue

        result, err = decode_chapter(str(chapter_path), chapter_num, chapter_path.name)

        if err:
            errors.append((chapter_path.name, err))
            print(f"  ERROR Ch{chapter_num:03d}  {err}")
            continue
        if not result:
            continue

        # Special handling: combined page (Ch069)
        if chapter_num == 69:
            sub_results = split_combined_chapter(result, chapter_num, chapter_path.name)
            for sr in sub_results:
                vid = sr["vector_id"]
                sname = re.sub(r'[^\w]','_',
                               (sr["subject"]["name"] or "unknown").lower())
                sname = re.sub(r'_+','_', sname).strip('_')[:40]
                out_fn = f"{vid.replace('-','_')}_{sname}.json"
                with open(os.path.join(OUTPUT_DIR, out_fn), 'w', encoding='utf-8') as f:
                    json.dump(sr, f, indent=2, ensure_ascii=False)
                written += 1
                print(f"  ✓ Ch{chapter_num:03d}  {sr['subject']['name']} (combined)")
            continue

        # Write normal chapter JSON
        sname = result["subject"]["name"] or "unknown"
        snake = re.sub(r'[^\w]','_', sname.lower())
        snake = re.sub(r'_+','_', snake).strip('_')[:40]
        out_fn = f"tv_300h2_ch{chapter_num:03d}_{snake}.json"
        out_path = os.path.join(OUTPUT_DIR, out_fn)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        processed_map[chapter_num] = result["vector_id"]
        written += 1

        # Collect gap observations
        for obs in result.get("author_observations", []):
            if obs.get("gap_flag"):
                all_gap_obs.append({
                    "chapter":   chapter_path.name,
                    "subject":   sname,
                    "vector_id": result["vector_id"],
                    "profession_category": result["life_outcomes"]["profession_category"],
                    **obs,
                })

        print(f"  ✓ Ch{chapter_num:03d}  {sname[:45]}")

    # ── Output 2: Gap Report ───────────────────────────────────────────────────
    gap_path = os.path.join(OUTPUT_DIR, "300H2_Gap_Report.md")
    with open(gap_path, 'w', encoding='utf-8') as f:
        f.write("# 300H2 Gap Report -- Thread 4\n\n")
        f.write(f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"> Chapters decoded: {written}\n")
        f.write(f"> Gap observations flagged (gap_flag: true): {len(all_gap_obs)}\n\n")
        f.write("**Note:** Full gap-vs-KE-rules evaluation deferred to Phase 4. "
                "Observations below are CANDIDATE gaps based on keyword heuristics "
                "(violent death indicators, Rahu/Ketu death-axis chains). "
                "Cross-reference with `LU_Gap_Report.md` (Thread 1) for two-book confirmation.\n\n")
        f.write("---\n\n")
        f.write("## Flagged Observations by Category\n\n")

        # Group by claim_axis
        from collections import defaultdict
        by_axis = defaultdict(list)
        for g in all_gap_obs:
            by_axis[g.get("claim_axis","unknown")].append(g)

        for axis, obs_list in sorted(by_axis.items()):
            f.write(f"### Axis: {axis.upper()} ({len(obs_list)} observations)\n\n")
            for g in obs_list:
                f.write(f"**{g['subject']}** (`{g['vector_id']}`) "
                        f"[{g.get('condition_type_guess','')}]\n")
                f.write(f"> {g['verbatim'][:160]}\n\n")

        f.write("---\n\n")
        f.write("## Next Steps\n")
        f.write("1. Phase 4: CC runs `vedic_calculator.py` to compute charts\n")
        f.write("2. Phase 4: Compare `lagna_stated_in_book` vs `lagna_computed` "
                "→ populate `engine_matches_book`\n")
        f.write("3. Phase 4: Run KP rule evaluation → set `rules_fired[]` + `layer_b_pass`\n")
        f.write("4. Phase 4: Compute `dasha_at_death` for all death cases → "
                "set `cc_computed: true`\n")
        f.write("5. Review gap observations against existing KE rules → "
                "promote confirmed gaps to `300H2_CaseDerived_Rules.json`\n")

    # ── Output 3: Case-Derived Rules skeleton ──────────────────────────────────
    rules_path = os.path.join(OUTPUT_DIR, "300H2_CaseDerived_Rules.json")
    rule_ctr = 1
    rules = []

    # Group gap observations by verbatim pattern to find cross-case patterns
    from collections import Counter
    pattern_counts = Counter()
    pattern_examples = {}
    for g in all_gap_obs:
        # Normalise: strip subject-specific details, keep structural pattern
        pattern_key = re.sub(
            r'\b(john|henry|amitabh|virginia|george|benazir|sirhan|nicolae|[A-Z][a-z]+\s[A-Z][a-z]+)\b',
            'SUBJECT', g['verbatim'], flags=re.IGNORECASE
        )[:80]
        pattern_counts[pattern_key] += 1
        if pattern_key not in pattern_examples:
            pattern_examples[pattern_key] = g

    for pattern, count in pattern_counts.most_common(30):
        ex = pattern_examples[pattern]
        rule = {
            "rule_id":                f"300h2-cdr-{rule_ctr:03d}",
            "source":                 "case_study_derived",
            "source_book":            "300 Important Horoscopes Vol 1 Part 2",
            "source_chapter":         ex["chapter"].replace('.pdf',''),
            "subject_name":           ex["subject"],
            "observation_verbatim":   ex["verbatim"],
            "generalised_condition": {
                "type":               ex.get("condition_type_guess",""),
                "planet":             None,
                "house":              None,
                "additional_factors": [],
            },
            "claim_axis":             ex.get("claim_axis",""),
            "claim_polarity":         ex.get("claim_polarity",""),
            "effect":                 "Rule generalisation -- pending TT/CC review",
            "confirmed_by_cases":     [ex["vector_id"]],
            "case_count":             count,
            "science_id":             "kp_jyotish",
            "approval_status":        "pending_human_review",
            "gap_in_existing_ke":     True,
        }
        rules.append(rule)
        rule_ctr += 1

    with open(rules_path, 'w', encoding='utf-8') as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)

    # ── Summary ────────────────────────────────────────────────────────────────
    print(f"\n{'─'*55}")
    print(f"  JSONs written  : {written}")
    print(f"  Errors         : {len(errors)}")
    print(f"  Gap obs flagged: {len(all_gap_obs)}")
    print(f"  Rule candidates: {len(rules)}")
    if errors:
        print("\n  Errors:")
        for fn, e in errors:
            print(f"    {fn}: {e}")
    print(f"\n  Gap Report   → {gap_path}")
    print(f"  Rules JSON   → {rules_path}")
    print(f"\nDone. All output in:\n  {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
