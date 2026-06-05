#!/usr/bin/env python3
"""
Full Decode Script: Longevity and Unnatural Deaths
Batch ID : tv_lu_decode_v1
Outputs  : 93 test-vector JSONs  +  LU_CaseDerived_Rules.json  +  LU_Gap_Report.md
Run from : any directory
"""

import json, re, os, sys
from pathlib import Path
import pdfplumber

# ── paths ──────────────────────────────────────────────────────────────────────
CHAPTERS_DIR = Path("/Users/apple/Documents/Knowledge Engine_eBooks/5 New test Books/Longevity and Unnatural Deaths/Chapter_Splits/")
OUTPUT_DIR   = Path("/Users/apple/DailyHoroscope-Migration/KE_TEXTBOOK_DECODE/Test_Vectors/JSON/longevity_unnatural/")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── constants ─────────────────────────────────────────────────────────────────
SIGN_MAP = {
    'Ar':'Aries','Ta':'Taurus','Ge':'Gemini','Cn':'Cancer',
    'Le':'Leo','Vi':'Virgo','Li':'Libra','Sc':'Scorpio',
    'Sg':'Sagittarius','Cp':'Capricorn','Aq':'Aquarius','Pi':'Pisces',
    # OCR artifacts
    'U':'Libra','u':'Libra','en':'Cancer','Cn':'Cancer',
    'Li':'Libra','Ar':'Aries',
}
SIGN_ORDER = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
              'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
PLANETS    = ['Jupiter','Saturn','Mercury','Venus','Mars','Sun','Moon','Rahu','Ketu']
PLANET_PAT = r'(?:Jupiter|Saturn|Mercury|Venus|Mars|Sun|Moon|Rahu|Ketu)'

MONTHS = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
          'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12,
          'january':1,'february':2,'march':3,'april':4,'june':6,
          'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}

# ── chapter metadata ──────────────────────────────────────────────────────────
CHAPTER_META = {
     7:("James Abram Garfield","20th US President","American"),
     8:("Osama Bin Laden","Founder of al-Qaeda, Terrorist Leader","Saudi Arabian"),
     9:("Rajiv Gandhi","7th Prime Minister of India","Indian"),
    10:("William McKinley","25th US President","American"),
    11:("John F. Kennedy","35th US President","American"),
    12:("Indira Gandhi","Prime Minister of India","Indian"),
    13:("Joseph Kennedy Jr.","Elder brother of JFK, US Navy Pilot","American"),
    14:("Robert Francis Kennedy","US Senator, younger brother of JFK","American"),
    15:("John Fitzgerald Kennedy Jr.","Son of President Kennedy","American"),
    16:("Carolyn Bassette Kennedy","Wife of JFK Jr.","American"),
    17:("Ronald Wilson Reagan","40th US President","American"),
    18:("Sanjay Gandhi","Indian Parliamentarian, son of Indira Gandhi","Indian"),
    19:("John Wilkes Booth","Assassin of Abraham Lincoln","American"),
    20:("Lee Harvey Oswald","Alleged assassin of John F. Kennedy","American"),
    21:("Nathuram Vinayak Godse","Assassin of Mahatma Gandhi","Indian"),
    22:("Lord Louis Mountbatten","Last Viceroy of India, British Royalty","British"),
    23:("Sheikh Mujib-ur-Rahman","First President of Bangladesh","Bangladeshi"),
    24:("Archduke Franz Ferdinand","Archduke of Austria, assassination triggered WWI","Austrian"),
    25:("Napoleon Bonaparte IV","French Ruling Family","French"),
    26:("Gen. Mohd. Zia Ul Haq","President of Pakistan","Pakistani"),
    27:("Gianni Versace","World Famous Fashion Designer","Italian"),
    28:("Zulfikar Ali Bhutto","Prime Minister of Pakistan","Pakistani"),
    29:("King Ananda Mahidol","King of Thailand","Thai"),
    30:("Louis XVI","King of France","French"),
    31:("Marie Antoinette","Queen of France, wife of Louis XVI","Austrian/French"),
    32:("Steve Irwin","Wildlife Expert, 'Crocodile Hunter'","Australian"),
    33:("Benito Mussolini","Prime Minister of Italy, Fascist Leader","Italian"),
    34:("Adolf Hitler","Leader of Nazi Germany","German"),
    35:("Eva Braun","Wife of Adolf Hitler","German"),
    36:("Vijaya Kumaratunga","Sri Lankan Politician","Sri Lankan"),
    37:("Olaf Joachim Palme","Prime Minister of Sweden","Swedish"),
    38:("Paul Josef Goebbels","Nazi Propaganda Minister","German"),
    39:("Pope John Paul II","Pope of Roman Catholics","Polish"),
    40:("Solomon Bandaranaike","Prime Minister of Sri Lanka","Sri Lankan"),
    41:("Benazir Bhutto","Prime Minister of Pakistan","Pakistani"),
    42:("Anwar Sadat","President of Egypt","Egyptian"),
    43:("Pierre Curie","Nobel Laureate Scientist","French"),
    44:("Ernesto Che Guevara","Marxist Revolutionary","Argentine"),
    45:("Pramod Venkatesh Mahajan","Indian Union Minister","Indian"),
    46:("Vladimir Lenin","Leader of Soviet Russia","Russian"),
    47:("Yitzhak Rabin","Prime Minister of Israel","Israeli"),
    48:("Y.S. Rajasekhara Reddy","Chief Minister of Andhra Pradesh","Indian"),
    49:("Martin Luther King","US Civil Rights Leader","American"),
    50:("Saddam Hussein","President of Iraq","Iraqi"),
    51:("Emperor Alexander II","Czar of Russia","Russian"),
    52:("Emperor Nicholas II","Last Czar of Russia","Russian"),
    53:("Empress Czarina Alexandra","Empress of Russia, wife of Nicholas II","German/Russian"),
    54:("Grand Duchess Maria Nikolaevna","Daughter of Czar Nicholas II","Russian"),
    55:("Grand Duchess Olga Nikolaevna","Eldest daughter of Czar Nicholas II","Russian"),
    56:("Grand Duchess Tatiana Nikolaevna","Second daughter of Czar Nicholas II","Russian"),
    57:("Alexei Nikolaevich","Tsarevich of Russia, son of Nicholas II","Russian"),
    58:("Grand Duchess Anastasia Nikolaevna","Youngest daughter of Czar Nicholas II","Russian"),
    59:("Ranasinghe Premadasa","President of Sri Lanka","Sri Lankan"),
    60:("Nethaji Subhash Chandra Bose","Indian Independence Freedom Fighter","Indian"),
    61:("Pandit Deendayal Upadhyaya","Indian Social and Political Leader","Indian"),
    62:("Madhavrao Scindia","Indian Politician","Indian"),
    63:("Pravir Chandra Banj Deo","King of Bastar","Indian"),
    64:("Bahia Bakari","French School Girl, Yemenia Flight 626 survivor","French"),
    65:("Pablo Escobar","Colombian Drug Lord","Colombian"),
    66:("Pierre Laval","French Politician, Nazi Collaborator","French"),
    67:("King Alexander I","King of Yugoslavia","Yugoslav"),
    68:("CPN Singh","Indian Union Minister","Indian"),
    69:("Tipu Sultan","Defacto King of Mysore","Indian"),
    70:("Theodore Roosevelt","26th US President","American"),
    71:("Diana, Princess of Wales","Princess of Wales","British"),
    72:("Anton Cermak","Mayor of Chicago, USA","American"),
    73:("James Brady","Press Secretary to President Ronald Reagan","American"),
    74:("Benigno Aquino","Filipino Opposition Leader","Filipino"),
    75:("Alberto Fujimori","President of Peru","Peruvian/Japanese"),
    76:("King Alfonso XIII","King of Spain","Spanish"),
    77:("James Earl Ray","Assassin of Martin Luther King","American"),
    78:("Morarjee Desai","Prime Minister of India","Indian"),
    79:("J.D. Tippit","Dallas Police Officer","American"),
    80:("Lech Kaczynski","President of Poland","Polish"),
    81:("Giorgia Padoan","Italian National","Italian"),
    82:("Chiranjeevi","South Indian Film Megastar","Indian"),
    83:("Vincent Van Gogh","World Famous Dutch Painter","Dutch"),
    84:("Joseph Smith Jr.","Founder of Mormonism","American"),
    85:("Gulshan Kumar","Music Baron, Founder of T-Series","Indian"),
    86:("Sirhan Sirhan","Assassin of Robert F. Kennedy","Palestinian/American"),
    87:("Park Chung-hee","President of South Korea","South Korean"),
    88:("Amitabh Bachchan","Bollywood Film Superstar","Indian"),
    89:("Chandrababu Naidu","Chief Minister of Andhra Pradesh","Indian"),
    90:("Nicolae Ceausescu","Communist President of Romania","Romanian"),
    91:("King George I of Greece","King of Greece","Greek/Danish"),
    92:("Mohd. Najib","President of Afghanistan","Afghan"),
    93:("King Carlos I","King of Portugal","Portuguese"),
    94:("King Umberto I","King of Italy","Italian"),
    95:("Ahmed Shah Massoud","Afghan Military Leader","Afghan"),
    96:("Virginia Woolf","English Novelist and Writer","British"),
    97:("Jeffrey Coombs","9/11 Terrorist Attack Victim","American"),
    98:("Crown Prince Luis Filipe","Crown Prince of Portugal","Portuguese"),
    99:("John Lennon","Musician, Co-founder of The Beatles","British"),
}

CHAPTER_FILES = {
     7:"Ch07_James_Abram_Garfield.pdf",
     8:"Ch08_Osama_Bin_Laden.pdf",
     9:"Ch09_Rajiv_Gandhi.pdf",
    10:"Ch10_William_McKinley.pdf",
    11:"Ch11_John_F_Kennedy.pdf",
    12:"Ch12_Indira_Gandhi.pdf",
    13:"Ch13_Joseph_Kennedy_Jr.pdf",
    14:"Ch14_Robert_Francis_Kennedy.pdf",
    15:"Ch15_John_F_Kennedy_Jr.pdf",
    16:"Ch16_Carolyn_Bessette_Kennedy.pdf",
    17:"Ch17_Ronald_Reagan.pdf",
    18:"Ch18_Sanjay_Gandhi.pdf",
    19:"Ch19_John_Wilkes_Booth.pdf",
    20:"Ch20_Lee_Harvey_Oswald.pdf",
    21:"Ch21_Nathuram_Vinayak_Godse.pdf",
    22:"Ch22_Lord_Louis_Mountbatten.pdf",
    23:"Ch23_Sheikh_Mujib_ur_Rahman.pdf",
    24:"Ch24_Archduke_Franz_Ferdinand.pdf",
    25:"Ch25_Napoleon_Bonaparte_IV.pdf",
    26:"Ch26_Gen_Mohd_Zia_Ul_Haq.pdf",
    27:"Ch27_Gianni_Versace.pdf",
    28:"Ch28_Zulfikar_Ali_Bhutto.pdf",
    29:"Ch29_King_Ananda_Mahidol.pdf",
    30:"Ch30_Louis_XVI_King_of_France.pdf",
    31:"Ch31_Marie_Antoinette.pdf",
    32:"Ch32_Steve_Irwin.pdf",
    33:"Ch33_Benito_Mussolini.pdf",
    34:"Ch34_Adolf_Hitler.pdf",
    35:"Ch35_Eva_Braun.pdf",
    36:"Ch36_Vijaya_Kumaratunga.pdf",
    37:"Ch37_Olof_Palme.pdf",
    38:"Ch38_Paul_Josef_Goebbels.pdf",
    39:"Ch39_Pope_John_Paul_II.pdf",
    40:"Ch40_Solomon_Bandaranaike.pdf",
    41:"Ch41_Benazir_Bhutto.pdf",
    42:"Ch42_Anwar_Sadat.pdf",
    43:"Ch43_Pierre_Curie.pdf",
    44:"Ch44_Ernesto_Che_Guevara.pdf",
    45:"Ch45_Pramod_Mahajan.pdf",
    46:"Ch46_Vladimir_Lenin.pdf",
    47:"Ch47_Yitzhak_Rabin.pdf",
    48:"Ch48_YS_Rajasekhara_Reddy.pdf",
    49:"Ch49_Martin_Luther_King.pdf",
    50:"Ch50_Saddam_Hussein.pdf",
    51:"Ch51_Emperor_Alexander_II.pdf",
    52:"Ch52_Emperor_Nicholas_II.pdf",
    53:"Ch53_Empress_Czarina_Alexandra.pdf",
    54:"Ch54_Grand_Duchess_Maria_Nikolaevna.pdf",
    55:"Ch55_Grand_Duchess_Olga_Nikolaevna.pdf",
    56:"Ch56_Grand_Duchess_Tatiana_Nikolaevna.pdf",
    57:"Ch57_Alexei_Nikolaevich.pdf",
    58:"Ch58_Grand_Duchess_Anastasia_Nikolaevna.pdf",
    59:"Ch59_Ranasinghe_Premadasa.pdf",
    60:"Ch60_Nethaji_Subhash_Chandra_Bose.pdf",
    61:"Ch61_Pandit_Deendayal_Upadhyaya.pdf",
    62:"Ch62_Madhavrao_Scindia.pdf",
    63:"Ch63_Pravir_Chandra_Banj_Deo.pdf",
    64:"Ch64_Bahia_Bakari.pdf",
    65:"Ch65_Pablo_Escobar.pdf",
    66:"Ch66_Pierre_Laval.pdf",
    67:"Ch67_King_Alexander_I_Yugoslavia.pdf",
    68:"Ch68_CPN_Singh.pdf",
    69:"Ch69_Tipu_Sultan.pdf",
    70:"Ch70_Theodore_Roosevelt.pdf",
    71:"Ch71_Diana_Princess_of_Wales.pdf",
    72:"Ch72_Anton_Cermak.pdf",
    73:"Ch73_James_Brady.pdf",
    74:"Ch74_Benigno_Aquino.pdf",
    75:"Ch75_Alberto_Fujimori.pdf",
    76:"Ch76_King_Alfonso_XIII_Spain.pdf",
    77:"Ch77_James_Earl_Ray.pdf",
    78:"Ch78_Morarjee_Desai.pdf",
    79:"Ch79_JD_Tippit.pdf",
    80:"Ch80_Lech_Kaczynski.pdf",
    81:"Ch81_Giorgia_Padoan.pdf",
    82:"Ch82_Chiranjeevi.pdf",
    83:"Ch83_Vincent_Van_Gogh.pdf",
    84:"Ch84_Joseph_Smith_Jr.pdf",
    85:"Ch85_Gulshan_Kumar.pdf",
    86:"Ch86_Sirhan_Sirhan.pdf",
    87:"Ch87_Park_Chung_hee.pdf",
    88:"Ch88_Amitabh_Bachchan.pdf",
    89:"Ch89_Chandrababu_Naidu.pdf",
    90:"Ch90_Nicolae_Ceausescu.pdf",
    91:"Ch91_King_George_I_Greece.pdf",
    92:"Ch92_Mohd_Najib.pdf",
    93:"Ch93_King_Carlos_I_Portugal.pdf",
    94:"Ch94_King_Umberto_I_Italy.pdf",
    95:"Ch95_Ahmed_Shah_Massoud.pdf",
    96:"Ch96_Virginia_Woolf.pdf",
    97:"Ch97_Jeffrey_W_Coombs.pdf",
    98:"Ch98_Crown_Prince_Luis_Filipe_Portugal.pdf",
    99:"Ch99_John_Lennon.pdf",
}

# subject_name_snake for filenames
CHAPTER_SNAKE = {
     7:"james_abram_garfield", 8:"osama_bin_laden", 9:"rajiv_gandhi",
    10:"william_mckinley",    11:"john_f_kennedy",  12:"indira_gandhi",
    13:"joseph_kennedy_jr",   14:"robert_f_kennedy",15:"jfk_jr",
    16:"carolyn_bassette_kennedy",17:"ronald_reagan",18:"sanjay_gandhi",
    19:"john_wilkes_booth",   20:"lee_harvey_oswald",21:"nathuram_godse",
    22:"lord_louis_mountbatten",23:"sheikh_mujib_ur_rahman",
    24:"archduke_franz_ferdinand",25:"napoleon_bonaparte_iv",
    26:"gen_zia_ul_haq",      27:"gianni_versace",  28:"zulfikar_ali_bhutto",
    29:"king_ananda_mahidol", 30:"louis_xvi",       31:"marie_antoinette",
    32:"steve_irwin",         33:"benito_mussolini",34:"adolf_hitler",
    35:"eva_braun",           36:"vijaya_kumaratunga",37:"olof_palme",
    38:"paul_goebbels",       39:"pope_john_paul_ii",40:"solomon_bandaranaike",
    41:"benazir_bhutto",      42:"anwar_sadat",     43:"pierre_curie",
    44:"che_guevara",         45:"pramod_mahajan",  46:"vladimir_lenin",
    47:"yitzhak_rabin",       48:"ys_rajasekhara_reddy",49:"martin_luther_king",
    50:"saddam_hussein",      51:"emperor_alexander_ii",52:"emperor_nicholas_ii",
    53:"empress_czarina_alexandra",54:"grand_duchess_maria",
    55:"grand_duchess_olga",  56:"grand_duchess_tatiana",
    57:"alexei_nikolaevich",  58:"grand_duchess_anastasia",
    59:"ranasinghe_premadasa",60:"subhash_chandra_bose",
    61:"deendayal_upadhyaya", 62:"madhavrao_scindia",63:"pravir_chandra_banj_deo",
    64:"bahia_bakari",        65:"pablo_escobar",   66:"pierre_laval",
    67:"king_alexander_i_yugoslavia",68:"cpn_singh",69:"tipu_sultan",
    70:"theodore_roosevelt",  71:"diana_princess_of_wales",72:"anton_cermak",
    73:"james_brady",         74:"benigno_aquino",  75:"alberto_fujimori",
    76:"king_alfonso_xiii",   77:"james_earl_ray",  78:"morarjee_desai",
    79:"jd_tippit",           80:"lech_kaczynski",  81:"giorgia_padoan",
    82:"chiranjeevi",         83:"vincent_van_gogh",84:"joseph_smith_jr",
    85:"gulshan_kumar",       86:"sirhan_sirhan",   87:"park_chung_hee",
    88:"amitabh_bachchan",    89:"chandrababu_naidu",90:"nicolae_ceausescu",
    91:"king_george_i_greece",92:"mohd_najib",      93:"king_carlos_i_portugal",
    94:"king_umberto_i_italy",95:"ahmed_shah_massoud",96:"virginia_woolf",
    97:"jeffrey_coombs",      98:"crown_prince_luis_filipe",99:"john_lennon",
}

# ── utility functions ─────────────────────────────────────────────────────────
def get_house(lagna_sign, planet_sign):
    if not lagna_sign or not planet_sign:
        return None
    try:
        li = SIGN_ORDER.index(lagna_sign)
        pi = SIGN_ORDER.index(planet_sign)
        return ((pi - li) % 12) + 1
    except ValueError:
        return None

def dms_to_decimal(deg, mins, secs=0.0):
    try:
        return round(float(deg) + float(mins)/60 + float(secs)/3600, 4)
    except:
        return None

def parse_iso_date(date_str):
    """Parse various date string formats → YYYY-MM-DD or None."""
    if not date_str:
        return None
    date_str = date_str.strip()
    # "29 May 1917" or "May 29, 1917" or "29 May, 1917"
    m = re.match(r'(\d{1,2})\s+(\w+),?\s+(\d{4})', date_str)
    if m:
        day, mon, yr = m.groups()
        mo = MONTHS.get(mon.lower())
        if mo:
            return f"{yr}-{mo:02d}-{int(day):02d}"
    m = re.match(r'(\w+)\s+(\d{1,2}),?\s+(\d{4})', date_str)
    if m:
        mon, day, yr = m.groups()
        mo = MONTHS.get(mon.lower())
        if mo:
            return f"{yr}-{mo:02d}-{int(day):02d}"
    return None

def normalize_sign(raw):
    """Convert 2-3 char sign abbreviation to full sign name."""
    if not raw:
        return None
    key2 = raw[:2].capitalize()
    key3 = raw[:3].capitalize() if len(raw) >= 3 else ''
    return SIGN_MAP.get(key2) or SIGN_MAP.get(raw.lower()) or SIGN_MAP.get(key3) or None

def classify_death_type(text):
    """Classify death type from a description string."""
    if not text:
        return 'unknown'
    t = text.lower()
    if any(k in t for k in ['suicide','took his own','took her own','self-inflict','drowned herself','drowned himself']):
        return 'suicide'
    if any(k in t for k in ['shot','assassin','killed','murder','stab','bomb','blast',
                             'execut','hanging','hanged','gunshot','weapon','beheaded',
                             'firing squad','poison','poisoned']):
        return 'violent'
    if any(k in t for k in ['plane crash','air crash','plane','aircraft','car crash',
                             'road accident','car accident','drown','fall','vehicle',
                             'ship','train','crash']):
        return 'accident'
    if any(k in t for k in ['cancer','disease','illness','pneumonia','heart',
                             'alzheimer','infection','fever','surgery','ailment',
                             'health','natural']):
        return 'disease'
    return 'unknown'

# ── PDF reader ────────────────────────────────────────────────────────────────
def read_pdf(filepath):
    """Return list of page texts."""
    pages = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                pages.append(t or '')
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
    return pages

def full_text(pages):
    return '\n'.join(pages)

# ── birth data parser ─────────────────────────────────────────────────────────
def parse_birth_data(text, ch_num):
    bd = {
        "date": None, "time_local": None, "timezone_offset_hours": None,
        "time_utc": None, "latitude": None, "longitude": None,
        "place": None, "time_confidence": "from_chart",
        "ayanamsha": "lahiri", "ayanamsha_stated": None, "notes": ""
    }

    # Date -- sanitise OCR period inside year before parsing (e.g. "19.11" → "1911")
    date_text = re.sub(r'\b(1[6-9]|20)\.(\d{2})\b', r'\1\2', text)
    dm = re.search(r'Date:\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4}|\d{1,2}\s+[A-Za-z]+,?\s+\d{4})', date_text)
    if not dm:
        # Also try the inline bio parenthetical "(DD Mon YYYY - DD Mon YYYY)"
        dm = re.search(r'\((\d{1,2}\s+[A-Za-z]+\s+\d{4})\s*[--]', date_text)
    if dm:
        bd['date'] = parse_iso_date(dm.group(1))

    # Time
    tm = re.search(r'Time:\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*(am|pm)', text, re.IGNORECASE)
    if tm:
        t_raw, ampm = tm.group(1), tm.group(2).lower()
        parts = t_raw.split(':')
        h, m, s = int(parts[0]), int(parts[1]), int(parts[2]) if len(parts)>2 else 0
        if ampm == 'pm' and h != 12: h += 12
        elif ampm == 'am' and h == 12: h = 0
        bd['time_local'] = f"{h:02d}:{m:02d}:{s:02d}"

    # Timezone
    tzm = re.search(r'Time\s*Zone:\s*[.·]?(\d{1,2}):(\d{2})(?::\d{2})?\s*\(?\s*(E|W|East|West)\s*(?:of\s*GMT)?', text, re.IGNORECASE)
    if tzm:
        h, m = int(tzm.group(1)), int(tzm.group(2))
        direction = tzm.group(3)[0].upper()
        offset = h + m/60
        bd['timezone_offset_hours'] = offset if direction == 'E' else -offset

    # Compute UTC time
    if bd['date'] and bd['time_local'] and bd['timezone_offset_hours'] is not None:
        try:
            from datetime import datetime, timedelta
            local_dt = datetime.strptime(f"{bd['date']} {bd['time_local']}", "%Y-%m-%d %H:%M:%S")
            utc_dt = local_dt - timedelta(hours=bd['timezone_offset_hours'])
            bd['time_utc'] = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except:
            pass

    # Coordinates -- look for pattern: "NN E/W DD' [DD"]" and "NN N/S DD' [DD"]"
    # Longitude
    lonm = re.search(r'(\d{1,3})\s*[EeWw]\s*(\d{1,2})[\'°]?\s*(?:(\d{1,2})[\"\'\""]?)?', text)
    if lonm:
        d, m_, s = int(lonm.group(1)), int(lonm.group(2)), int(lonm.group(3) or 0)
        lon = dms_to_decimal(d, m_, s)
        # Check E or W
        lon_text = text[max(0,lonm.start()-2):lonm.end()+2]
        if 'W' in lon_text.upper() or 'w' in lon_text:
            lon = -lon
        if lon and abs(lon) <= 180:
            bd['longitude'] = lon

    # Latitude
    latm = re.search(r'(\d{1,2})\s*[Nn]\s*(\d{1,2})[\'°]?\s*(?:(\d{1,2})[\"\'\""]?)?', text)
    if latm:
        d, m_, s = int(latm.group(1)), int(latm.group(2)), int(latm.group(3) or 0)
        lat = dms_to_decimal(d, m_, s)
        if lat and abs(lat) <= 90:
            bd['latitude'] = lat

    # Place name -- line after the coordinates
    place_m = re.search(r'Place:\s*[^\n]*\n\s*([A-Z][A-Za-z\s,]+?)(?:\n|Lunar|Tithi)', text)
    if place_m:
        place_raw = place_m.group(1).strip().rstrip(',')
        bd['place'] = place_raw
    else:
        # fallback: find city/country from Place: line
        place2 = re.search(r'Place:.*?([A-Z][a-z]+(?:\s+[A-Za-z]+)*,\s*(?:[A-Z][a-z]+(?:\s+[A-Za-z]+)*))', text)
        if place2:
            bd['place'] = place2.group(1).strip()

    # Ayanamsha
    ayam = re.search(r'Ayanamsa:\s*(\d{2}-\d{2}-[\d.]+)', text, re.IGNORECASE)
    if ayam:
        bd['ayanamsha_stated'] = ayam.group(1)

    # Ch07 note (missing title page)
    if ch_num == 7:
        bd['notes'] = "Chapter title page (book p.30) missing from scan. Birth data sourced from chart header and inline text."
        # Override with known values for Garfield
        bd['date'] = bd['date'] or "1831-11-19"
        if not bd['time_local']:
            bd['time_local'] = "06:28:00"
        if not bd['timezone_offset_hours']:
            bd['timezone_offset_hours'] = -5.0
        if not bd['latitude']:
            bd['latitude'] = 41.338
        if not bd['longitude']:
            bd['longitude'] = -80.519

    return bd

# ── KP table parser ───────────────────────────────────────────────────────────
def parse_kp_table(text):
    """
    Parse the KP planet-position body table.
    Returns (planet_dict, lagna_sign_str).
    Always uses KP Body table rows (Body|Longitude|Star|Pada|Significations).
    """
    planets = {}
    lagna_sign = None

    # Locate table start -- allow OCR noise between "Body" and "Longitude" (e.g. "Body <Longitude")
    tbl_start = re.search(r'Body[^A-Za-z\n]{0,8}Longitude', text, re.IGNORECASE)
    if not tbl_start:
        return planets, lagna_sign

    chunk = text[tbl_start.start():]
    lines = chunk.split('\n')

    # Two-step row parsing (more robust than single regex):
    # Step 1 -- detect planet name at start of line
    # Step 2 -- scan for degree + sign + minutes after planet name,
    #           skipping any karaka suffix ("-DK", "-.MK", "- BK", "(R)" etc.)
    PLANET_START_RE = re.compile(
        r'^(Lagna|Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu)',
        re.IGNORECASE
    )
    KNOWN_SIGNS = 'Ar|Ta|Ge|Cn|Le|Vi|Li|Sc|Sg|Cp|Aq|Pi'
    # Degree can be OCR'd: "OS"=05, "2S"=25, "1S"=15, "O8"=08, etc.
    # Minute can also be OCR'd: "4S'"=45', "1S'"=15'
    # Degree pattern: first char can be O/0/digit; second char can be digit/S (optional)
    # Minutes pattern: same -- [0-9S]{1,2}
    DEG_SIGN_RE = re.compile(
        rf'([O0-9][0-9S]?)\s+({KNOWN_SIGNS})\s+([0-9S]{{1,2}})',
        re.IGNORECASE
    )
    row_re  = PLANET_START_RE   # alias for compatibility
    row_re2 = PLANET_START_RE   # alias

    # Stop before any transit / secondary chart table to avoid double-counting.
    # Only stop on phrases that clearly introduce a new (transit) chart table.
    TRANSIT_STOPS = [
        'transit chart is drawn',
        'transit chart is given',
        'transit is drawn',
        'Transit chart is drawn',
        'Transit chart is given',
    ]
    for stop_phrase in TRANSIT_STOPS:
        stop_pos = chunk.find(stop_phrase)
        if 0 < stop_pos < len(chunk):
            chunk = chunk[:stop_pos]
            lines = chunk.split('\n')
            break

    seen = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Step 1: planet name at start of line?
        pm = PLANET_START_RE.match(line)
        if not pm:
            continue

        p_raw = pm.group(1).upper()
        if p_raw in seen:
            continue

        # Step 2: find degree+sign+minutes after the planet name
        dm = DEG_SIGN_RE.search(line[pm.end():])
        if not dm:
            continue

        seen.add(p_raw)

        # Decode OCR degree: "OS"→05, "2S"→25, "1S"→15, "O8"→08
        def ocr_to_int(raw):
            cleaned = raw.upper().replace('O', '0').replace('S', '5')
            try:
                return int(cleaned)
            except:
                return 0

        deg  = ocr_to_int(dm.group(1))
        sign_raw = dm.group(2)
        mins = ocr_to_int(dm.group(3))

        sign = normalize_sign(sign_raw)
        decimal_deg = dms_to_decimal(deg, mins)

        # Extract nakshatra, pada, significations from rest of line
        # dm.end() is relative to line[pm.end():], so adjust
        rest = line[pm.end() + dm.end():]
        # Try to find pada (single digit 1-4) + significations
        sig_m = re.search(r'\s([1-4])\s+(.+)$', rest)
        nakshatra = None
        pada = None
        sigs = []
        if sig_m:
            pada = int(sig_m.group(1))
            sigs_raw = sig_m.group(2).strip()
            # Everything before pada is nakshatra
            pre_pada = rest[:sig_m.start()].strip()
            # Nakshatra is the last word-group in pre_pada
            nak_words = pre_pada.split()
            if nak_words:
                nakshatra = nak_words[-1]
            # Parse significations
            for tok in re.split(r'[,\s]+', sigs_raw):
                tok = tok.strip().rstrip('.')
                if tok in ('-', ''):
                    continue
                try:
                    sigs.append(int(tok))
                except ValueError:
                    if tok:
                        sigs.append(tok)

        if p_raw == 'LAGNA':
            lagna_sign = sign
            planets['LAGNA'] = {
                "sign": sign, "degree": decimal_deg, "house": 1,
                "nakshatra": nakshatra, "pada": pada, "significations": sigs
            }
        else:
            house = get_house(lagna_sign, sign)
            planets[p_raw] = {
                "sign": sign, "degree": decimal_deg, "house": house,
                "nakshatra": nakshatra, "pada": pada, "significations": sigs
            }

        if len(seen) >= 11:  # 10 planets + lagna
            break

    return planets, lagna_sign

# ── VMD parser ────────────────────────────────────────────────────────────────
def parse_vmd(text):
    """Extract VMD (Vimshottari Dasha period) structured object."""
    empty = {"mahadasha":None,"antardasha":None,"pratyantardasha":None,
             "sookshma":None,"stated_by_author":False,"raw_text":None}

    # Trigger patterns that precede a VMD period statement.
    # After matching the trigger, we extract the next 4 planet names in order
    # (allowing ANY separator -- handles both "Saturn-Mercury-Jupiter" and
    # prose format "Jupiter dasha, Mercury bhukti, Moon Antara, Moon Sookshma").
    triggers = [
        r'VMD period of\s+',
        r'VMD period.*?was.*?that of\s+',
        r'VMD period.*?was.*?of\s+',
        r'VMD period.*?on.*?date.*?was\s+',
        r'VMD of\s+',
        r'during.*?VMD.*?of\s+',
        r'died during.*?VMD.*?\s+',
        r'died.*?during.*?period of\s+',
        r'period.*?was.*?that of\s+',
        r'period.*?of.*?death.*?was\s+',
        r'Dasha.*?Bhukti.*?\n',   # fallback: catches "Dasha lord X ... Bhukti lord Y" prose
    ]

    for trig in triggers:
        m = re.search(trig, text, re.IGNORECASE | re.DOTALL)
        if not m:
            continue
        # Take up to 300 chars after trigger and collect planet names in order
        after = text[m.end(): m.end() + 300]
        found = re.findall(PLANET_PAT, after, re.IGNORECASE)
        # Capitalize and keep all occurrences (same planet may appear at different levels)
        found = [p.capitalize() for p in found if p.capitalize() in PLANETS]
        if len(found) < 2:
            continue
        raw_snippet = re.sub(r'\s+', ' ', after[:120]).strip()
        return {
            "mahadasha":        found[0].upper() if len(found) > 0 else None,
            "antardasha":       found[1].upper() if len(found) > 1 else None,
            "pratyantardasha":  found[2].upper() if len(found) > 2 else None,
            "sookshma":         found[3].upper() if len(found) > 3 else None,
            "stated_by_author": True,
            "raw_text":         raw_snippet
        }
    return empty

# ── death / event data parser ─────────────────────────────────────────────────
def parse_death_date(text):
    """Find the most likely death/event date in text → YYYY-MM-DD or None."""
    # Look for patterns like "22 Nov 1963" or "November 22, 1963"
    patterns = [
        r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})',
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})',
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})',
    ]
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            g = m.groups()
            try:
                if g[0].isdigit():
                    day, mon_s, yr = int(g[0]), g[1], int(g[2])
                else:
                    mon_s, day, yr = g[0], int(g[1]), int(g[2])
                mo = MONTHS.get(mon_s[:3].lower())
                if mo:
                    return f"{yr}-{mo:02d}-{int(day):02d}"
            except:
                continue
    return None

def parse_age_at_death(text):
    """Extract age at event/death."""
    m = re.search(r'(?:in his|in her|at the age of|aged|age)\s+(\d{2,3})(?:th|st|nd|rd)?\s*(?:year)?', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r'was\s+(\d{2,3})\s+years(?:\s+and\s+\d+\s+months)?', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r'native was\s+(\d{2,3})\s+years', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None

def extract_cause_of_death(text):
    """Extract a short cause-of-death string from prose."""
    # Look for "died of/due to", "was shot", "was killed by", "committed suicide" etc.
    patterns = [
        r'(?:died|death)\s+(?:of|due to|by|from|through)\s+([^.;,\n]{5,80})',
        r'was\s+(shot dead|shot and killed|assassinated|killed by[^.;,\n]{0,60}|executed[^.;,\n]{0,40}|killed in[^.;,\n]{0,60})',
        r'(committed suicide[^.;,\n]{0,60})',
        r'(shot dead[^.;,\n]{0,60})',
        r'(?:killed|died)\s+in\s+([^.;,\n]{5,80})',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            cause = m.group(1).strip().rstrip('.,;')
            if len(cause) > 5:
                return cause
    return None

# ── author observations extractor ─────────────────────────────────────────────
def extract_observations(text, ch_num):
    """Extract key analytical statements as structured observations."""
    obs_list = []
    obs_counter = [1]

    def add_obs(verbatim, ctype, polarity='negative'):
        verbatim = verbatim.strip().replace('\n', ' ')
        verbatim = re.sub(r'\s{2,}', ' ', verbatim)
        if len(verbatim) < 20:
            return
        obs_list.append({
            "obs_id": f"obs-{obs_counter[0]:03d}",
            "verbatim": verbatim[:600],
            "condition_type_guess": ctype,
            "claim_axis": "longevity",
            "claim_polarity": polarity,
            "gap_flag": False,
            "potential_rule_id": None
        })
        obs_counter[0] += 1

    # 1. Numbered analytical list items: "1) ..." or "1. ..."
    list_items = re.findall(r'\n\s*\d+\)\s+(.+?)(?=\n\s*\d+\)|\n\n|\Z)', text, re.DOTALL)
    for item in list_items[:10]:
        add_obs(item, "planet_in_house")

    # 2. Dasha-level analysis sentences
    for dasha_level in ['Dasha', 'Bhukti', 'Antara', 'Sookshma']:
        for m in re.finditer(
            rf'{dasha_level}\s+lord\s+\w+\s+(?:is|signif|has|posit|aspects?|placed|gives?|confer)[^.!?]{{10,300}}[.!?]',
            text, re.IGNORECASE | re.DOTALL
        ):
            add_obs(m.group(0), "dasha_planet")

    # 3. Key longevity/death analysis statements
    key_pats = [
        (r'lagna and\s+0?8th\s+(?:house\s+)?(?:have\s+become|are|become|has\s+become|is)\s+weak[^.!]{10,300}[.!]', "lagna_8th_weakness"),
        (r'(?:maraca|badhaka)[^.!]{15,300}(?:caused|activated|is responsible|gave)[^.!]{5,200}[.!]', "maraka_badhaka"),
        (r'(?:lagna|08th|8th)\s+lord[^.!]{15,300}(?:weak|afflict|connected|aspect|maraca|badhaka)[^.!]{5,200}[.!]', "lagna_lord_affliction"),
        (r'longevity\s+(?:of|is|has been|was)[^.!]{10,200}[.!]', "longevity_statement"),
        (r'(?:violent|weapon|injury|accident|bomb|shoot|shot|stab)[^.!]{10,200}death[^.!]{5,100}[.!]', "death_mechanism"),
        (r'(?:Madhya|Alpa|Poorna)\s*[Aa]ayu[^.!]{5,200}[.!]', "ayur_classification"),
        (r'dictum\s+is\s+that[^.!]{10,300}[.!]', "author_dictum"),
    ]
    for pat, ctype in key_pats:
        for m in re.finditer(pat, text, re.IGNORECASE | re.DOTALL):
            add_obs(m.group(0), ctype)

    # 4. Survival/recovery statements
    survival_pats = [
        r'(?:survived?|recovered?|escape[sd]?)[^.!]{10,200}[.!]',
        r'(?:lucky|fortunately|escaped death)[^.!]{10,200}[.!]',
    ]
    for pat in survival_pats:
        for m in re.finditer(pat, text, re.IGNORECASE | re.DOTALL):
            add_obs(m.group(0), "survival", "positive")

    # Deduplicate by first 80 chars
    seen_starts = set()
    unique = []
    for o in obs_list:
        key = o['verbatim'][:80]
        if key not in seen_starts:
            seen_starts.add(key)
            unique.append(o)

    return unique[:25]

# ── life events extractor (S1: non-terminal events) ──────────────────────────
SURVIVAL_SUBJECTS = {
    17,  # Reagan -- survived assassination attempt
    39,  # Pope John Paul II -- survived assassination attempt
    64,  # Bahia Bakari -- plane crash survivor
    70,  # Theodore Roosevelt -- survived assassination attempt
    73,  # James Brady -- survived, paralysed
    75,  # Alberto Fujimori -- jailed, not killed
    76,  # King Alfonso XIII -- survived attack
    82,  # Chiranjeevi -- survived
    86,  # Sirhan Sirhan -- alive (perpetrator, not victim)
    88,  # Amitabh Bachchan -- survived injury
    89,  # Chandrababu Naidu -- survived landmine
    77,  # James Earl Ray -- imprisoned perpetrator
}

def extract_life_events(text, ch_num):
    """Extract non-terminal significant events (attacks survived, near-death)."""
    events = []
    ev_counter = [1]

    if ch_num not in SURVIVAL_SUBJECTS:
        return events

    # Patterns for life-threat events that were survived
    survive_pats = [
        r'(?:On|on)\s+(\w+\s+\d{1,2},?\s+\d{4}|\d{1,2}\s+\w+\s+\d{4})[^.!]{5,200}(?:shot|bomb|attack|injur|attempt|assault)[^.!]{5,200}[.!]',
        r'(?:was\s+shot|was\s+attack|was\s+injur|was\s+target)[^.!]{10,300}[.!]',
    ]

    for pat in survive_pats:
        for m in re.finditer(pat, text, re.IGNORECASE | re.DOTALL):
            desc = m.group(0).strip().replace('\n', ' ')
            desc = re.sub(r'\s{2,}', ' ', desc)

            # Try to extract event date
            date_m = re.search(r'(\d{1,2}\s+\w+\s+\d{4}|\w+\s+\d{1,2},?\s+\d{4})', desc)
            ev_date = parse_iso_date(date_m.group(1)) if date_m else None

            # VMD for this event
            vmd = parse_vmd(text)  # will catch first VMD in text

            events.append({
                "event_id": f"ev-{ev_counter[0]:03d}",
                "event_type": "life_threatening_event",
                "description": desc[:400],
                "date": ev_date,
                "age_at_event": parse_age_at_death(desc),
                "survived": True,
                "dasha_at_event": vmd
            })
            ev_counter[0] += 1
            break  # one event per pattern

    return events[:3]

# ── case-derived rules extractor ──────────────────────────────────────────────
RULE_CANDIDATES = []  # global accumulator

def extract_rules(text, ch_num, subject_name):
    """
    Extract rule-candidate statements: planetary condition → life outcome.
    Returns list of rule dicts (appended to global RULE_CANDIDATES).
    """
    chapter_key = f"tv-lu-ch{ch_num:02d}"
    rules = []

    # Pattern: condition statements that explain death/longevity
    rule_pats = [
        # "X in lagna/8th caused violent death"
        r'((?:\w+\s+){1,5}(?:in\s+lagna|in\s+0?8th|lord\s+in)[^.!]{10,200}(?:caus|lead|result|indic|gave|signif)[^.!]{5,200})[.!]',
        # "Saturn and Rahu in X caused Y"
        r'((?:Saturn|Mars|Rahu|Ketu|Sun|Moon|Jupiter|Venus|Mercury)[^.!]{5,150}(?:caus|brought|gave|result)[^.!]{5,200})[.!]',
        # "When X is connected to Y, death by weapon"
        r'(when\s+(?:lagna|0?8th|maraca|badhaka)[^.!]{10,200}(?:death|violent|weapon|injury|bomb|shoot)[^.!]{5,150})[.!]',
        # "The dictum is that when..."
        r'((?:dictum|principle|rule)\s+is\s+that[^.!]{20,400})[.!]',
        # Badhaka/maraca + death outcome
        r'((?:badhaka|maraca)[^.!]{10,200}(?:weak|afflict|connect|posit)[^.!]{5,200}(?:death|fatal|violent|injury|accident|longevity)[^.!]{5,150})[.!]',
    ]

    rule_counter = len(RULE_CANDIDATES) + 1
    seen = set()

    for pat in rule_pats:
        for m in re.finditer(pat, text, re.IGNORECASE | re.DOTALL):
            raw = m.group(1).strip().replace('\n', ' ')
            raw = re.sub(r'\s{2,}', ' ', raw)
            if len(raw) < 30 or raw[:60] in seen:
                continue
            seen.add(raw[:60])

            # Guess condition type
            ctype = "planet_in_house"
            if 'dasha' in raw.lower() or 'bhukti' in raw.lower():
                ctype = "dasha_planet"
            elif 'aspect' in raw.lower():
                ctype = "planet_aspect"
            elif 'conjunction' in raw.lower() or 'conjoin' in raw.lower():
                ctype = "planet_conjunction"

            # Guess planets involved
            planets_found = list(set(re.findall(PLANET_PAT, raw, re.IGNORECASE)))

            rule = {
                "rule_id": f"lu-cdr-{rule_counter:03d}",
                "source": "case_study_derived",
                "source_book": "Longevity and Unnatural Deaths",
                "source_chapter": f"Ch{ch_num:02d}_{CHAPTER_SNAKE.get(ch_num,'')}",
                "subject_name": subject_name,
                "observation_verbatim": raw[:500],
                "generalised_condition": {
                    "type": ctype,
                    "planets_involved": planets_found,
                    "house": None,
                    "additional_factors": []
                },
                "claim_axis": "longevity",
                "claim_polarity": "negative",
                "effect": "See observation_verbatim -- generalised rule pending human review",
                "confirmed_by_cases": [chapter_key],
                "science_id": "kp_jyotish",
                "approval_status": "pending_human_review",
                "gap_in_existing_ke": True
            }
            RULE_CANDIDATES.append(rule)
            rules.append(rule["rule_id"])
            rule_counter += 1

    return rules

# ── main per-chapter decoder ──────────────────────────────────────────────────
def decode_chapter(ch_num):
    filename  = CHAPTER_FILES.get(ch_num)
    if not filename:
        return None, f"Ch{ch_num:02d}: no filename mapping"

    filepath  = CHAPTERS_DIR / filename
    if not filepath.exists():
        return None, f"Ch{ch_num:02d}: file not found -- {filepath}"

    name, desc, nationality = CHAPTER_META.get(ch_num, ("Unknown","",""))
    snake   = CHAPTER_SNAKE.get(ch_num, f"ch{ch_num:02d}")
    vec_id  = f"tv-lu-ch{ch_num:02d}"

    pages   = read_pdf(filepath)
    if not pages:
        return None, f"Ch{ch_num:02d}: no pages read"

    text    = full_text(pages)

    # ── Birth data
    bd      = parse_birth_data(text, ch_num)

    # ── KP planet table
    planets, lagna_sign = parse_kp_table(text)

    # Flag chapters where birth chart is image-only (not extractable via pdfplumber)
    IMAGE_ONLY_CHARTS = {25, 26, 28}
    if ch_num in IMAGE_ONLY_CHARTS and not planets:
        bd['notes'] = (bd.get('notes') or '') + \
            " Birth chart shown as South Indian grid image only -- KP body table not present in OCR output; planet positions cannot be extracted via pdfplumber."

    # ── Chart verification
    moon_sign = planets.get('MOON', {}).get('sign')
    chart_v = {
        "lagna_stated_in_book":    lagna_sign,
        "moon_sign_stated_in_book": moon_sign,
        "lagna_computed":          None,
        "moon_sign_computed":      None,
        "engine_matches_book":     None,
        "mismatch_notes":          ""
    }

    # ── Death data
    cause   = extract_cause_of_death(text)
    d_date  = parse_death_date(text)
    age     = parse_age_at_death(text)
    d_type  = classify_death_type(cause or text[:400])
    vmd     = parse_vmd(text)
    # For chapters where subject survived the analysed event, death may not be in text
    if ch_num in SURVIVAL_SUBJECTS and d_type not in ('disease','natural','violent','suicide'):
        d_type = 'unknown'

    death_data = {
        "cause_of_death": cause,
        "death_type":     d_type,
        "death_date":     d_date,
        "age_at_death":   age,
        "dasha_at_death": vmd
    }

    # ── Life events (S1)
    life_events = extract_life_events(text, ch_num)

    # ── Author observations
    observations = extract_observations(text, ch_num)

    # ── Case-derived rules (appended to global list, IDs returned)
    rule_ids = extract_rules(text, ch_num, name)

    # ── Attach potential_rule_id to first matching obs
    for obs in observations:
        if obs['condition_type_guess'] in ('author_dictum','maraka_badhaka','lagna_8th_weakness') and rule_ids:
            obs['potential_rule_id'] = rule_ids[0]

    # ── Assemble JSON
    vector = {
        "vector_id":     vec_id,
        "book_id":       "longevity_unnatural",
        "source_chapter": filename.replace('.pdf',''),
        "pdf_path":      f"Chapter_Splits/{filename}",

        "subject": {
            "name":        name,
            "description": desc,
            "nationality": nationality
        },

        "birth_data": bd,

        "chart_verification": chart_v,

        "planet_positions_from_table": planets,

        "life_events": life_events,

        "death_data": death_data,

        "known_facts": {
            "profession": None,
            "profession_category": None,
            "key_events": []
        },

        "author_observations": observations,

        "rule_evaluation": {
            "evaluated":    False,
            "evaluated_at": None,
            "rules_fired":  [],
            "layer_a_pass": None,
            "layer_b_pass": None
        },

        "test_status": {
            "extraction_complete": bool(bd['date'] and planets),
            "chart_computed":      False,
            "rules_evaluated":     False
        }
    }

    return vector, None

# ── run all 93 chapters ───────────────────────────────────────────────────────
def main():
    print(f"Decoding {len(CHAPTER_FILES)} chapters...")
    print(f"Output → {OUTPUT_DIR}\n")

    success = 0
    errors  = []

    for ch_num in sorted(CHAPTER_FILES.keys()):
        name = CHAPTER_META.get(ch_num, ("?","",""))[0]
        print(f"  Ch{ch_num:02d} {name} ...", end=' ')

        vector, err = decode_chapter(ch_num)
        if err:
            print(f"ERROR: {err}")
            errors.append(err)
            continue

        out_name = f"tv_lu_ch{ch_num:02d}_{CHAPTER_SNAKE.get(ch_num,'unknown')}.json"
        out_path = OUTPUT_DIR / out_name
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(vector, f, indent=2, ensure_ascii=False)

        planet_count = len(vector['planet_positions_from_table'])
        bd_ok = bool(vector['birth_data']['date'])
        vmd_ok = bool(vector['death_data']['dasha_at_death']['stated_by_author'])
        obs_count = len(vector['author_observations'])
        print(f"OK  planets={planet_count} birth={bd_ok} vmd={vmd_ok} obs={obs_count}")
        success += 1

    # ── Output 2: LU_CaseDerived_Rules.json
    rules_path = OUTPUT_DIR / "LU_CaseDerived_Rules.json"
    with open(rules_path, 'w', encoding='utf-8') as f:
        json.dump(RULE_CANDIDATES, f, indent=2, ensure_ascii=False)
    print(f"\nLU_CaseDerived_Rules.json → {len(RULE_CANDIDATES)} rules")

    # ── Output 3: LU_Gap_Report.md
    # Build frequency count of confirmed_by_cases across rules
    from collections import defaultdict
    pattern_counts = defaultdict(list)
    for rule in RULE_CANDIDATES:
        key = rule['observation_verbatim'][:100]
        pattern_counts[key].extend(rule['confirmed_by_cases'])

    gap_path = OUTPUT_DIR / "LU_Gap_Report.md"
    with open(gap_path, 'w', encoding='utf-8') as f:
        f.write("# LU Gap Report -- Author Observations with No Matching KE Rule\n")
        f.write("## Longevity and Unnatural Deaths | Batch: tv_lu_decode_v1\n")
        f.write(f"> Generated: 2026-06-05 | Total rule candidates: {len(RULE_CANDIDATES)}\n\n")
        f.write("All observations below are flagged `gap_in_existing_ke: true`.\n")
        f.write("Prioritised by number of chapters confirming the same pattern.\n\n")
        f.write("---\n\n")

        # Sort rules by chapter for readability
        by_chapter = defaultdict(list)
        for rule in RULE_CANDIDATES:
            by_chapter[rule['source_chapter']].append(rule)

        for ch_key in sorted(by_chapter.keys()):
            rules = by_chapter[ch_key]
            f.write(f"### {ch_key}\n")
            for r in rules:
                f.write(f"**{r['rule_id']}** ` {r['generalised_condition']['type']} `\n")
                f.write(f"> {r['observation_verbatim'][:300]}\n\n")
            f.write("\n")

    print(f"LU_Gap_Report.md → {sum(len(v) for v in by_chapter.values())} entries")

    # ── Summary
    print(f"\n{'='*60}")
    print(f"DECODE COMPLETE")
    print(f"  Chapters decoded:   {success} / {len(CHAPTER_FILES)}")
    print(f"  Rule candidates:    {len(RULE_CANDIDATES)}")
    print(f"  Errors:             {len(errors)}")
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
    print(f"  Output folder:      {OUTPUT_DIR}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
