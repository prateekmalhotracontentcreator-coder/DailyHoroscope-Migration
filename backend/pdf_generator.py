"""
EverydayHoroscope — Premium PDF Report Generator
Proprietary IP of SkyHound Studios

Features:
- Premium gold/dark branded template
- Page border on every page
- Proper headings — no raw markdown
- Password protection on all PDFs
- North Indian Kundali chart embedding
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics import renderPDF
from io import BytesIO
from datetime import datetime
import re

# ─── Brand Colors ─────────────────────────────────────────────────────────────
GOLD        = colors.HexColor('#C5A059')
GOLD_LIGHT  = colors.HexColor('#F0E0B0')
GOLD_DARK   = colors.HexColor('#8B6914')
DARK_BG     = colors.HexColor('#1A1510')
DARK_TEXT   = colors.HexColor('#2D241E')
CREAM       = colors.HexColor('#FAF6F0')
CREAM_DARK  = colors.HexColor('#F0E8DC')
BORDER_GREY = colors.HexColor('#E0D4C0')
MUTED       = colors.HexColor('#7A6A58')
GREEN_OK    = colors.HexColor('#2E7D32')
AMBER_WARN  = colors.HexColor('#E65100')
RED_WARN    = colors.HexColor('#C62828')

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

# ─── Page Border + Header/Footer ──────────────────────────────────────────────

def draw_page_border(c, doc):
    """Draw gold page border, header and footer on every page."""
    c.saveState()

    # Outer border — double line effect
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.rect(10*mm, 10*mm, PAGE_W - 20*mm, PAGE_H - 20*mm)

    c.setStrokeColor(GOLD_LIGHT)
    c.setLineWidth(0.4)
    c.rect(12*mm, 12*mm, PAGE_W - 24*mm, PAGE_H - 24*mm)

    # Corner ornaments
    for x, y in [(10*mm, 10*mm), (PAGE_W-10*mm, 10*mm),
                 (10*mm, PAGE_H-10*mm), (PAGE_W-10*mm, PAGE_H-10*mm)]:
        c.setFillColor(GOLD)
        c.circle(x, y, 1.5*mm, fill=1, stroke=0)

    # Header line
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(MARGIN, PAGE_H - 22*mm, PAGE_W - MARGIN, PAGE_H - 22*mm)

    # Brand name in header
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(GOLD)
    c.drawString(MARGIN, PAGE_H - 19*mm, 'EVERYDAY HOROSCOPE')
    c.setFont('Helvetica', 7)
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 19*mm, 'everydayhoroscope.in')

    # Footer line
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(MARGIN, 18*mm, PAGE_W - MARGIN, 18*mm)

    # Footer text
    c.setFont('Helvetica', 7)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, 13*mm, 'Ancient Vedic Wisdom · Modern Precision · SkyHound Studios')
    c.drawRightString(PAGE_W - MARGIN, 13*mm, f'Page {doc.page}')

    c.restoreState()


# ─── Style Definitions ────────────────────────────────────────────────────────

def get_styles():
    base = getSampleStyleSheet()

    styles = {
        'report_title': ParagraphStyle(
            'ReportTitle',
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=GOLD,
            alignment=TA_CENTER,
            spaceAfter=4,
            leading=26,
        ),
        'report_subtitle': ParagraphStyle(
            'ReportSubtitle',
            fontName='Helvetica',
            fontSize=11,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        'section_heading': ParagraphStyle(
            'SectionHeading',
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=GOLD_DARK,
            spaceBefore=14,
            spaceAfter=6,
            borderPad=4,
        ),
        'sub_heading': ParagraphStyle(
            'SubHeading',
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=DARK_TEXT,
            spaceBefore=8,
            spaceAfter=4,
        ),
        'body': ParagraphStyle(
            'Body',
            fontName='Helvetica',
            fontSize=10,
            textColor=DARK_TEXT,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        'body_bold': ParagraphStyle(
            'BodyBold',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=DARK_TEXT,
            leading=15,
            spaceAfter=6,
        ),
        'highlight': ParagraphStyle(
            'Highlight',
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=GOLD_DARK,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        'small': ParagraphStyle(
            'Small',
            fontName='Helvetica',
            fontSize=8,
            textColor=MUTED,
            spaceAfter=4,
        ),
        'centered': ParagraphStyle(
            'Centered',
            fontName='Helvetica',
            fontSize=10,
            textColor=DARK_TEXT,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        'score_big': ParagraphStyle(
            'ScoreBig',
            fontName='Helvetica-Bold',
            fontSize=40,
            textColor=GOLD,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        'verdict': ParagraphStyle(
            'Verdict',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=GOLD_DARK,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
    }
    return styles


# ─── Helper: Clean markdown from Claude output ────────────────────────────────

def clean_markdown(text: str) -> str:
    """Strip raw markdown symbols from Claude output."""
    if not text:
        return ''
    # Remove ## headings markers
    text = re.sub(r'^#{1,4}\s+', '', text, flags=re.MULTILINE)
    # Remove **bold** markers (keep the text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove *italic* markers
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove --- dividers
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    # Remove bullet markdown
    text = re.sub(r'^[\*\-]\s+', '• ', text, flags=re.MULTILINE)
    # Clean up multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_sections(text: str, styles: dict) -> list:
    """
    Parse Claude output into formatted Paragraph flowables.
    Detects section headings, sub-headings, bullets, and body text.
    """
    text = clean_markdown(text)
    story = []
    paragraphs = text.split('\n\n')

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        lines = para.split('\n')
        first_line = lines[0].strip()

        # Detect section heading patterns
        if (len(first_line) < 60 and first_line.isupper()) or \
           first_line.endswith(':') and len(first_line) < 50:
            story.append(section_divider(first_line.rstrip(':'), styles))
            # Process remaining lines as body
            if len(lines) > 1:
                body_text = ' '.join(lines[1:]).strip()
                if body_text:
                    story.append(Paragraph(body_text, styles['body']))
        elif first_line.startswith('•'):
            # Bullet list
            for line in lines:
                line = line.strip()
                if line.startswith('•'):
                    story.append(Paragraph(line, styles['body']))
        else:
            # Regular paragraph
            story.append(Paragraph(para, styles['body']))

    return story


def section_divider(title: str, styles: dict) -> Paragraph:
    """Create a gold-accented section heading."""
    return Paragraph(f'<font color="#8B6914">◆</font> &nbsp;{title}', styles['section_heading'])


def gold_rule():
    """Thin gold horizontal rule."""
    return HRFlowable(
        width='100%',
        thickness=0.5,
        color=GOLD,
        spaceAfter=6,
        spaceBefore=6,
    )


def info_table(data: list, styles: dict) -> Table:
    """Create a styled key-value info table."""
    table = Table(data, colWidths=[55*mm, CONTENT_W - 55*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), CREAM_DARK),
        ('BACKGROUND', (1, 0), (1, -1), CREAM),
        ('TEXTCOLOR', (0, 0), (0, -1), GOLD_DARK),
        ('TEXTCOLOR', (1, 0), (1, -1), DARK_TEXT),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.3, BORDER_GREY),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [CREAM_DARK, CREAM]),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD),
    ]))
    return table


def koota_table(kootas: dict, styles: dict) -> Table:
    """Create the Ashtakoot Guna Milan score table."""
    header = [
        Paragraph('<b>Koota</b>', styles['small']),
        Paragraph('<b>Meaning</b>', styles['small']),
        Paragraph('<b>Score</b>', styles['small']),
        Paragraph('<b>Max</b>', styles['small']),
        Paragraph('<b>Result</b>', styles['small']),
    ]
    rows = [header]

    koota_display = {
        'varna': 'Varna', 'vashya': 'Vashya', 'tara': 'Tara',
        'yoni': 'Yoni', 'graha_maitri': 'Graha Maitri',
        'gana': 'Gana', 'bhakoot': 'Bhakoot', 'nadi': 'Nadi',
    }

    for key, display in koota_display.items():
        if key in kootas:
            k = kootas[key]
            score = k['score']
            max_s = k['max']
            ratio = score / max_s if max_s > 0 else 0
            if ratio >= 0.75:
                color = GREEN_OK
                symbol = '✓'
            elif ratio >= 0.4:
                color = AMBER_WARN
                symbol = '~'
            else:
                color = RED_WARN
                symbol = '✗'

            rows.append([
                Paragraph(f'<b>{display}</b>', styles['small']),
                Paragraph(k.get('meaning', ''), styles['small']),
                Paragraph(f'<font color="#{color.hexval()[2:]}">{score}</font>', styles['small']),
                Paragraph(str(max_s), styles['small']),
                Paragraph(
                    f'<font color="#{color.hexval()[2:]}">{symbol} {k.get("label", "")}</font>',
                    styles['small']
                ),
            ])

    col_widths = [28*mm, 60*mm, 18*mm, 14*mm, 38*mm]
    table = Table(rows, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), GOLD),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.3, BORDER_GREY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CREAM, CREAM_DARK]),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
    ]))
    return table


# ─── Cover Page ───────────────────────────────────────────────────────────────

def build_cover(report_title: str, person_name: str, report_date: str,
                styles: dict, story: list, subtitle: str = 'Everyday Horoscope · Ancient Vedic Wisdom'):
    """Build a premium cover section."""
    story.append(Spacer(1, 8*mm))

    # Gold top rule
    story.append(HRFlowable(width='100%', thickness=2, color=GOLD, spaceAfter=8))

    # Report title
    story.append(Paragraph(report_title.upper(), styles['report_title']))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(subtitle, styles['report_subtitle']))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD_LIGHT, spaceAfter=6))

    # Person name
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(person_name, styles['highlight']))

    # Date
    story.append(Paragraph(f'Report Generated: {report_date}', styles['small']))
    story.append(Paragraph('Powered by Vedic Astrology · Parashari · KP · Jaimini Systems', styles['small']))
    story.append(Spacer(1, 6*mm))
    story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=8))


# ─── Birth Chart PDF ──────────────────────────────────────────────────────────

def generate_birth_chart_pdf(profile: dict, report_content: str,
                              chart_data: dict = None,
                              password: str = None) -> BytesIO:
    """
    Generate premium Birth Chart PDF.
    profile: dict with name, date_of_birth, time_of_birth, location
    report_content: Claude-generated text
    chart_data: optional dict from vedic_calculator (for SVG chart + planet table)
    password: optional PDF password
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=26*mm, bottomMargin=24*mm,
        leftMargin=MARGIN, rightMargin=MARGIN,
        title=f"Birth Chart — {profile.get('name', '')}",
        author='Everyday Horoscope',
        subject='Vedic Birth Chart Analysis',
    )

    styles = get_styles()
    story = []
    report_date = datetime.now().strftime('%d %B %Y')

    # Cover
    build_cover('Janma Kundali', profile.get('name', ''), report_date, styles, story)

    # Birth details table
    story.append(section_divider('Birth Details', styles))
    data = [
        ['Name', profile.get('name', '')],
        ['Date of Birth', profile.get('date_of_birth', '')],
        ['Time of Birth', profile.get('time_of_birth', '')],
        ['Place of Birth', profile.get('location', profile.get('place_of_birth', ''))],
    ]
    if chart_data:
        lagna = chart_data.get('lagna', {})
        moon  = chart_data.get('moon_sign', {})
        nak   = chart_data.get('nakshatra', {})
        dasha = chart_data.get('current_dasha', {})
        data += [
            ['Ascendant (Lagna)', lagna.get('sign_vedic', lagna.get('sign', ''))],
            ['Moon Sign (Rashi)', moon.get('sign_vedic', moon.get('sign', ''))],
            ['Nakshatra', f"{nak.get('name', '')} Pada {nak.get('pada', '')} | Lord: {nak.get('lord', '')}"],
            ['Current Dasha', f"{dasha.get('planet', '')} Mahadasha ({dasha.get('start', '')} – {dasha.get('end', '')})"],
        ]
    story.append(info_table(data, styles))
    story.append(Spacer(1, 6*mm))

    # ── North Indian Kundali Chart ────────────────────────────────────────────
    if chart_data and chart_data.get('houses'):
        story.append(section_divider('Janma Kundali — Birth Chart', styles))
        story.append(Paragraph(
            f"North Indian Style · Ascendant: {chart_data['lagna'].get('sign_vedic', chart_data['lagna'].get('sign', ''))}",
            styles['small']
        ))
        story.append(Spacer(1, 3*mm))

        chart_drawing = draw_north_indian_chart(
            chart_data['houses'],
            chart_data['lagna']['sign'],
            size=160
        )
        chart_table = Table([[chart_drawing]], colWidths=[CONTENT_W])
        chart_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        story.append(chart_table)
        story.append(Spacer(1, 5*mm))

    # ── Planetary positions table ─────────────────────────────────────────────
    if chart_data and chart_data.get('planets'):
        story.append(section_divider('Planetary Positions', styles))
        planet_rows = [
            [Paragraph('<b>Planet</b>', styles['small']),
             Paragraph('<b>Sign</b>', styles['small']),
             Paragraph('<b>House</b>', styles['small']),
             Paragraph('<b>Degree</b>', styles['small']),
             Paragraph('<b>Notes</b>', styles['small'])],
        ]
        for pname, pdata in chart_data['planets'].items():
            retro = 'R' if pdata.get('retrograde') else ''
            planet_rows.append([
                Paragraph(pname.split('(')[0].strip(), styles['small']),
                Paragraph(pdata.get('sign', ''), styles['small']),
                Paragraph(str(pdata.get('house', '')), styles['small']),
                Paragraph(f"{pdata.get('degree', '')}° {retro}", styles['small']),
                Paragraph(f"Lord: {pdata.get('lord_of_sign', '')}", styles['small']),
            ])
        col_w = [45*mm, 35*mm, 18*mm, 20*mm, CONTENT_W - 118*mm]
        planet_table = Table(planet_rows, colWidths=col_w)
        planet_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DARK_BG),
            ('TEXTCOLOR',  (0, 0), (-1, 0), GOLD),
            ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0, 0), (-1, -1), 8),
            ('GRID',       (0, 0), (-1, -1), 0.3, BORDER_GREY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CREAM, CREAM_DARK]),
            ('PADDING',    (0, 0), (-1, -1), 5),
            ('BOX',        (0, 0), (-1, -1), 0.8, GOLD),
        ]))
        story.append(planet_table)
        story.append(Spacer(1, 6*mm))

    # ── House map table ───────────────────────────────────────────────────────
    if chart_data and chart_data.get('houses'):
        story.append(section_divider('12-House Analysis', styles))
        house_rows = [
            [Paragraph('<b>House</b>', styles['small']),
             Paragraph('<b>Domain</b>', styles['small']),
             Paragraph('<b>Sign</b>', styles['small']),
             Paragraph('<b>Lord</b>', styles['small']),
             Paragraph('<b>Planets</b>', styles['small'])],
        ]
        for h_num, h_data in chart_data['houses'].items():
            planets_str = ', '.join(p.split('(')[0].strip() for p in h_data['planets']) if h_data['planets'] else '—'
            house_name_short = h_data['name'].split('(')[0].strip() if '(' in h_data['name'] else h_data['name']
            house_rows.append([
                Paragraph(str(h_num), styles['small']),
                Paragraph(house_name_short[:30], styles['small']),
                Paragraph(h_data.get('sign', ''), styles['small']),
                Paragraph(h_data.get('lord', ''), styles['small']),
                Paragraph(planets_str, styles['small']),
            ])
        col_w2 = [12*mm, 55*mm, 28*mm, 20*mm, CONTENT_W - 115*mm]
        house_table = Table(house_rows, colWidths=col_w2)
        house_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DARK_BG),
            ('TEXTCOLOR',  (0, 0), (-1, 0), GOLD),
            ('FONTSIZE',   (0, 0), (-1, -1), 8),
            ('GRID',       (0, 0), (-1, -1), 0.3, BORDER_GREY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CREAM, CREAM_DARK]),
            ('PADDING',    (0, 0), (-1, -1), 5),
            ('BOX',        (0, 0), (-1, -1), 0.8, GOLD),
        ]))
        story.append(house_table)
        story.append(Spacer(1, 6*mm))

    # ── Interpreter's report content ──────────────────────────────────────────
    story.append(section_divider('Detailed Interpretation', styles))
    story.extend(parse_sections(report_content, styles))

    # Footer note
    story.append(Spacer(1, 6*mm))
    story.append(gold_rule())
    story.append(Paragraph(
        'This report is for reflective and informational purposes. '
        'Everyday Horoscope · everydayhoroscope.in · SkyHound Studios',
        styles['small']
    ))

    doc.build(story, onFirstPage=draw_page_border, onLaterPages=draw_page_border)

    buffer.seek(0)
    if password:
        buffer = apply_password(buffer, password)
    else:
        buffer.seek(0)

    return buffer


# ─── Kundali Milan PDF ────────────────────────────────────────────────────────

def generate_kundali_milan_pdf(person1: dict, person2: dict,
                                compatibility_score: int, analysis: str,
                                ashtakoot_data: dict = None,
                                password: str = None) -> BytesIO:
    """
    Generate premium Kundali Milan PDF.
    """
    buffer = BytesIO()
    p1_name = person1.get('name', 'Person 1')
    p2_name = person2.get('name', 'Person 2')
    report_date = datetime.now().strftime('%d %B %Y')

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=26*mm, bottomMargin=24*mm,
        leftMargin=MARGIN, rightMargin=MARGIN,
        title=f"Kundali Milan — {p1_name} & {p2_name}",
        author='Everyday Horoscope',
        subject='Vedic Marriage Compatibility Report',
    )

    styles = get_styles()
    story = []

    # Cover
    build_cover(
        'Kundali Milan',
        f'{p1_name}  &  {p2_name}',
        report_date, styles, story
    )

    # Compatibility score block
    story.append(Spacer(1, 4*mm))

    # Score table
    if compatibility_score >= 28:
        verdict = 'Excellent Match — Highly Recommended'
        score_color = GREEN_OK
    elif compatibility_score >= 24:
        verdict = 'Very Good Match'
        score_color = GREEN_OK
    elif compatibility_score >= 18:
        verdict = 'Acceptable Match — Remedies Advised'
        score_color = AMBER_WARN
    else:
        verdict = 'Below Threshold — Consult Astrologer'
        score_color = RED_WARN

    score_data = [[
        Paragraph(f'{compatibility_score}/36', styles['score_big']),
        Paragraph(verdict, styles['verdict']),
    ]]
    score_table = Table(score_data, colWidths=[40*mm, CONTENT_W - 40*mm])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CREAM),
        ('BOX', (0, 0), (-1, -1), 1.5, GOLD),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBEFORE', (1, 0), (1, -1), 0.5, BORDER_GREY),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 5*mm))

    # Person details side by side
    story.append(section_divider('Birth Details', styles))
    persons_data = [
        [
            Paragraph('<b>Groom</b>', styles['body_bold']),
            Paragraph('<b>Bride</b>', styles['body_bold']),
        ],
        [
            Paragraph(f'<b>Name:</b> {p1_name}', styles['body']),
            Paragraph(f'<b>Name:</b> {p2_name}', styles['body']),
        ],
        [
            Paragraph(f'<b>DOB:</b> {person1.get("date_of_birth", "")}', styles['body']),
            Paragraph(f'<b>DOB:</b> {person2.get("date_of_birth", "")}', styles['body']),
        ],
        [
            Paragraph(f'<b>Time:</b> {person1.get("time_of_birth", "")}', styles['body']),
            Paragraph(f'<b>Time:</b> {person2.get("time_of_birth", "")}', styles['body']),
        ],
        [
            Paragraph(f'<b>Place:</b> {person1.get("location", "")}', styles['body']),
            Paragraph(f'<b>Place:</b> {person2.get("location", "")}', styles['body']),
        ],
    ]
    persons_table = Table(persons_data, colWidths=[CONTENT_W/2, CONTENT_W/2])
    persons_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), GOLD),
        ('BACKGROUND', (0, 1), (-1, -1), CREAM),
        ('GRID', (0, 0), (-1, -1), 0.3, BORDER_GREY),
        ('BOX', (0, 0), (-1, -1), 0.8, GOLD),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('LINEBETWEEN', (0, 0), (-1, -1), 0.5, BORDER_GREY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(persons_table)
    story.append(Spacer(1, 5*mm))

    # Ashtakoot table if available
    if ashtakoot_data and 'kootas' in ashtakoot_data:
        story.append(section_divider('Ashtakoot Guna Milan — 8 Koota Analysis', styles))
        story.append(koota_table(ashtakoot_data['kootas'], styles))
        story.append(Spacer(1, 4*mm))

    # Detailed analysis
    story.append(section_divider('Detailed Compatibility Analysis', styles))
    story.extend(parse_sections(analysis, styles))

    # Footer note
    story.append(Spacer(1, 6*mm))
    story.append(gold_rule())
    story.append(Paragraph(
        f'Kundali Milan Report · {p1_name} & {p2_name} · Generated {report_date} · '
        'Everyday Horoscope · everydayhoroscope.in · SkyHound Studios',
        styles['small']
    ))
    story.append(Paragraph(
        'This report is for reflective and informational purposes. '
        'Vedic astrology is a guidance system, not a guarantee.',
        styles['small']
    ))

    doc.build(story, onFirstPage=draw_page_border, onLaterPages=draw_page_border)

    buffer.seek(0)
    if password:
        buffer = apply_password(buffer, password)
    else:
        buffer.seek(0)

    return buffer


# ─── Password Protection ──────────────────────────────────────────────────────

def apply_password(input_buffer: BytesIO, password: str) -> BytesIO:
    """Apply PDF password protection using pypdf."""
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(input_buffer)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        # User password = provided password, owner password = different
        writer.encrypt(
            user_password=password,
            owner_password=password + '_owner',
            use_128bit=True
        )
        output = BytesIO()
        writer.write(output)
        output.seek(0)
        return output
    except Exception as e:
        # If pypdf not available, return unencrypted
        input_buffer.seek(0)
        return input_buffer


# ─── Password Generator ───────────────────────────────────────────────────────

def generate_report_password(person_name: str, date_of_birth: str) -> str:
    """
    Generate a deterministic, user-friendly password from birth details.
    Format: FirstName + BirthYear + 3-letter birth month
    Example: Prateek1987Oct
    """
    name_part = person_name.split()[0].capitalize() if person_name else 'Report'
    try:
        from datetime import datetime
        dt = datetime.strptime(date_of_birth, '%Y-%m-%d')
        date_part = str(dt.year) + dt.strftime('%b')
    except Exception:
        date_part = date_of_birth[:4] if date_of_birth else '2024'
    return f'{name_part}{date_part}'


# ─── North Indian Kundali Chart (Native ReportLab) ────────────────────────────

def draw_north_indian_chart(houses: dict, lagna_sign: str, size: float = 180) -> Drawing:
    """
    Generate North Indian style Kundali chart as a native ReportLab Drawing.
    No external dependencies — pure ReportLab shapes.
    size: width and height in points (square chart)
    """
    from reportlab.graphics.shapes import (
        Drawing, Rect, Line, String, Group
    )
    from reportlab.lib.colors import HexColor

    CHART_GOLD   = HexColor('#C5A059')
    CHART_BG     = HexColor('#1A1510')
    CHART_TEXT   = HexColor('#F0E0B0')
    CHART_DIM    = HexColor('#7A6A58')

    d = Drawing(size, size)

    # Background
    d.add(Rect(0, 0, size, size, fillColor=CHART_BG, strokeColor=CHART_GOLD, strokeWidth=1.2))

    # Outer border (inset 2pt)
    m = 2
    d.add(Rect(m, m, size - 2*m, size - 2*m, fillColor=None, strokeColor=CHART_GOLD, strokeWidth=0.8))

    cx = size / 2
    cy = size / 2

    # Diagonal lines: corners to centre
    d.add(Line(m, m,         cx, cy, strokeColor=CHART_GOLD, strokeWidth=0.6))
    d.add(Line(size-m, m,    cx, cy, strokeColor=CHART_GOLD, strokeWidth=0.6))
    d.add(Line(m, size-m,    cx, cy, strokeColor=CHART_GOLD, strokeWidth=0.6))
    d.add(Line(size-m, size-m, cx, cy, strokeColor=CHART_GOLD, strokeWidth=0.6))

    # Mid-edge to mid-edge lines
    d.add(Line(cx, size-m,  m,      cy, strokeColor=CHART_GOLD, strokeWidth=0.6))
    d.add(Line(cx, size-m,  size-m, cy, strokeColor=CHART_GOLD, strokeWidth=0.6))
    d.add(Line(cx, m,       m,      cy, strokeColor=CHART_GOLD, strokeWidth=0.6))
    d.add(Line(cx, m,       size-m, cy, strokeColor=CHART_GOLD, strokeWidth=0.6))

    # North Indian house label positions (x, y) — centre of each house cell
    # y is from BOTTOM in ReportLab (inverted from screen)
    s = size
    label_pos = {
        1:  (cx,     s*0.83),   # top centre triangle
        2:  (s*0.79, s*0.79),   # top right
        3:  (s*0.89, cy),       # right upper
        4:  (s*0.79, s*0.21),   # bottom right
        5:  (cx,     s*0.17),   # bottom centre
        6:  (s*0.21, s*0.21),   # bottom left
        7:  (s*0.11, cy),       # left lower
        8:  (s*0.21, s*0.79),   # top left
        9:  (cx,     s*0.95),   # very top
        10: (s*0.95, cy),       # far right
        11: (cx,     s*0.05),   # very bottom
        12: (s*0.05, cy),       # far left
    }

    # Planet abbreviations
    planet_abbr = {
        'Sun (Surya)': 'Su', 'Sun': 'Su',
        'Moon (Chandra)': 'Mo', 'Moon': 'Mo',
        'Mercury (Budha)': 'Me', 'Mercury': 'Me',
        'Venus (Shukra)': 'Ve', 'Venus': 'Ve',
        'Mars (Mangal)': 'Ma', 'Mars': 'Ma',
        'Jupiter (Brihaspati)': 'Ju', 'Jupiter': 'Ju',
        'Saturn (Shani)': 'Sa', 'Saturn': 'Sa',
        'Rahu': 'Ra', 'Ketu': 'Ke',
    }

    font_size = max(5.5, size * 0.038)
    small_size = max(4.5, size * 0.030)

    for house_num, (lx, ly) in label_pos.items():
        h_data = houses.get(house_num, houses.get(str(house_num), {}))

        # House number (dimmed)
        d.add(String(lx, ly + font_size * 1.6, str(house_num),
                     fontSize=small_size, fillColor=CHART_DIM,
                     textAnchor='middle', fontName='Helvetica'))

        # Sign (first 3 letters)
        sign = h_data.get('sign', '') if isinstance(h_data, dict) else ''
        if sign:
            d.add(String(lx, ly + font_size * 0.4, sign[:3],
                         fontSize=font_size, fillColor=CHART_TEXT,
                         textAnchor='middle', fontName='Helvetica'))

        # Planets in this house
        planets = h_data.get('planets', []) if isinstance(h_data, dict) else []
        if planets:
            abbrs = [planet_abbr.get(p, p[:2]) for p in planets[:3]]
            planet_str = ' '.join(abbrs)
            d.add(String(lx, ly - font_size * 0.8, planet_str,
                         fontSize=font_size * 0.9, fillColor=CHART_GOLD,
                         textAnchor='middle', fontName='Helvetica-Bold'))

        # Mark Lagna house
        if house_num == 1:
            d.add(String(lx, ly + font_size * 2.6, 'ASC',
                         fontSize=small_size, fillColor=CHART_GOLD,
                         textAnchor='middle', fontName='Helvetica-Bold'))

    return d


# ─── Brihat Kundli Pro PDF ────────────────────────────────────────────────────

def generate_brihat_kundli_pdf(report: dict, chart_data: dict = None,
                                password: str = None) -> BytesIO:
    """
    Generate premium Brihat Kundli Pro PDF — full structured report.
    report: BrihatKundliReport dict
    chart_data: optional vedic_calculator output for SVG chart
    password: optional PDF password
    """
    from reportlab.platypus import KeepTogether, Flowable
    from reportlab.graphics import renderPDF as rl_renderPDF

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=22*mm, bottomMargin=22*mm,
        leftMargin=MARGIN, rightMargin=MARGIN,
        title=f"Brihat Kundli Pro — {report.get('full_name', '')}",
        author='Everyday Horoscope',
        subject='Comprehensive Vedic Astrology Life Report',
    )

    styles = get_styles()
    story = []
    report_date = datetime.now().strftime('%d %B %Y')
    name = report.get('full_name', '')
    dob  = report.get('date_of_birth', '')

    # ── Cover ─────────────────────────────────────────────────────────────────
    build_cover('BRIHAT KUNDLI PRO', name, report_date, styles, story,
                subtitle='Comprehensive Vedic Astrology Life Report')
    story.append(Spacer(1, 3*mm))

    # Birth details table
    story.append(section_divider('Birth Details', styles))
    asc  = report.get('ascendant', {})
    moon = report.get('moon_sign', {})
    nak_name = moon.get('nakshatra', '')
    cur_d = report.get('current_dasha', {})
    details = [
        ['Name',           name],
        ['Date of Birth',  dob],
        ['Time of Birth',  report.get('time_of_birth', '')],
        ['Place of Birth', report.get('place_of_birth', '')],
        ['Gender',         report.get('gender', '').capitalize()],
        ['Ascendant (Lagna)', f"{asc.get('sign','')} | Lord: {asc.get('lord','')} | Element: {asc.get('element','')}"],
        ['Moon Sign (Rashi)', moon.get('sign', '')],
        ['Nakshatra',      f"{nak_name} Pada {moon.get('nakshatra_pada','')} | Lord: {moon.get('nakshatra_lord','')}"],
        ['Current Dasha',  f"{cur_d.get('mahadasha','')} Mahadasha ({cur_d.get('period','')})"],
    ]
    story.append(info_table(details, styles))
    story.append(Spacer(1, 5*mm))

    # ── North Indian Chart ────────────────────────────────────────────────────
    if chart_data and chart_data.get('houses'):
        story.append(section_divider('Janma Kundali — Birth Chart', styles))
        story.append(Paragraph(
            f"North Indian Style · Ascendant: {asc.get('sign','')} ({asc.get('sign_vedic', asc.get('sign',''))})",
            styles['small']
        ))
        story.append(Spacer(1, 3*mm))

        chart_drawing = draw_north_indian_chart(chart_data['houses'], asc.get('sign', ''), size=160)

        # Centre the chart using a table
        chart_table = Table([[chart_drawing]], colWidths=[CONTENT_W])
        chart_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        story.append(chart_table)
        story.append(Spacer(1, 5*mm))

    # ── Planetary Positions ───────────────────────────────────────────────────
    planets = report.get('planetary_positions', [])
    if planets:
        story.append(section_divider('Planetary Positions', styles))
        rows = [[
            Paragraph('<b>Planet</b>', styles['small']),
            Paragraph('<b>Sign</b>', styles['small']),
            Paragraph('<b>House</b>', styles['small']),
            Paragraph('<b>Status</b>', styles['small']),
            Paragraph('<b>Strength</b>', styles['small']),
            Paragraph('<b>Effects</b>', styles['small']),
        ]]
        for p in planets:
            strength = str(p.get('strength', ''))
            s_color_hex = '2E7D32' if 'Strong' in strength else ('E65100' if 'Good' in strength or 'Moderate' in strength else 'C62828')
            effects_text = ' · '.join(p.get('effects', [])[:2]) if isinstance(p.get('effects'), list) else str(p.get('effects', ''))
            rows.append([
                Paragraph(str(p.get('planet', '')), styles['small']),
                Paragraph(str(p.get('sign', '')), styles['small']),
                Paragraph(f"H{p.get('house', '')}", styles['small']),
                Paragraph(str(p.get('status', '')), styles['small']),
                Paragraph(f'<font color="#{s_color_hex}"><b>{strength}</b></font>', styles['small']),
                Paragraph(effects_text[:80], styles['small']),
            ])
        col_w = [32*mm, 24*mm, 12*mm, 28*mm, 20*mm, CONTENT_W - 116*mm]
        pt = Table(rows, colWidths=col_w)
        pt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), DARK_BG),
            ('TEXTCOLOR',  (0,0), (-1,0), GOLD),
            ('FONTSIZE',   (0,0), (-1,-1), 7.5),
            ('GRID',       (0,0), (-1,-1), 0.3, BORDER_GREY),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, CREAM_DARK]),
            ('PADDING',    (0,0), (-1,-1), 4),
            ('BOX',        (0,0), (-1,-1), 0.8, GOLD),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(pt)
        story.append(Spacer(1, 5*mm))

    story.append(PageBreak())

    # ── Helper: section with two-column bullet lists ───────────────────────────
    def two_col_bullets(left_title, left_items, right_title, right_items):
        left_content = [Paragraph(f'<font color="#7A6A58"><b>{left_title}</b></font>', styles['small'])]
        for item in (left_items or []):
            left_content.append(Paragraph(f'• {item}', styles['body']))
        right_content = [Paragraph(f'<font color="#7A6A58"><b>{right_title}</b></font>', styles['small'])]
        for item in (right_items or []):
            right_content.append(Paragraph(f'• {item}', styles['body']))
        t = Table([[left_content, right_content]], colWidths=[CONTENT_W/2 - 2*mm, CONTENT_W/2 - 2*mm])
        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 4)]))
        story.append(t)

    def bullet_para(item):
        return Paragraph(f'• {item}', styles['body'])

    def rating_para(rating):
        return Paragraph(f'<font color="#C5A059"><b>Rating: {rating}</b></font>', styles['small'])

    # ── Career ────────────────────────────────────────────────────────────────
    career = report.get('career_prediction', {})
    if career:
        story.append(section_divider('Career & Profession', styles))
        if career.get('overall_rating'):
            story.append(rating_para(f"{career.get('overall_rating','')} · Business Potential: {career.get('business_potential','')}"))
            story.append(Spacer(1, 2*mm))
        two_col_bullets(
            'Best Career Fields', career.get('best_career_fields', []),
            'Strengths at Work',  career.get('strengths_at_work', [])
        )
        timeline = career.get('career_timeline', [])
        if timeline:
            story.append(Spacer(1, 3*mm))
            story.append(Paragraph('<font color="#7A6A58"><b>Career Timeline</b></font>', styles['small']))
            for t in timeline:
                period_str = t.get('period', '')
                pred_str   = t.get('prediction', '')
                advice_str = t.get('advice', '')
                tl_row = Table([[
                    Paragraph(f'<b>{period_str}</b>', styles['small']),
                    [Paragraph(pred_str, styles['body']),
                     Paragraph(f'💡 {advice_str}', styles['small'])]
                ]], colWidths=[28*mm, CONTENT_W - 28*mm])
                tl_row.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (0,-1), CREAM_DARK),
                    ('GRID', (0,0), (-1,-1), 0.3, BORDER_GREY),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('PADDING', (0,0), (-1,-1), 5),
                ]))
                story.append(tl_row)
                story.append(Spacer(1, 2*mm))
        story.append(Spacer(1, 4*mm))

    # ── Love & Relationships ──────────────────────────────────────────────────
    love = report.get('love_prediction', {})
    if love:
        story.append(section_divider('Love & Relationships', styles))
        if love.get('overall_rating'):
            story.append(rating_para(love.get('overall_rating', '')))
            story.append(Spacer(1, 2*mm))
        two_col_bullets(
            'Ideal Partner Traits', love.get('ideal_partner_traits', []),
            'Compatible Signs',     love.get('compatibility_signs', [])
        )
        challenging = love.get('challenging_signs', [])
        if challenging:
            story.append(Paragraph('<font color="#7A6A58"><b>Challenging Signs:</b></font> ' + ', '.join(challenging), styles['small']))
        mt = love.get('marriage_timing', {})
        if mt and mt.get('favorable_years'):
            years = ', '.join(str(y) for y in mt['favorable_years'])
            story.append(Paragraph(f'<font color="#C5A059"><b>Favourable Marriage Years:</b></font> {years}', styles['small']))
        story.append(Spacer(1, 4*mm))

    # ── Health ────────────────────────────────────────────────────────────────
    health = report.get('health_prediction', {})
    if health:
        story.append(section_divider('Health & Wellbeing', styles))
        header_parts = []
        if health.get('overall_vitality'): header_parts.append(health['overall_vitality'])
        if health.get('body_constitution'): header_parts.append(health['body_constitution'])
        if header_parts:
            story.append(rating_para(' · '.join(header_parts)))
            story.append(Spacer(1, 2*mm))
        two_col_bullets(
            'Vulnerable Areas',   health.get('vulnerable_areas', []),
            'Preventive Measures', health.get('preventive_measures', [])
        )
        diet = health.get('dietary_recommendations', [])
        if diet:
            story.append(Paragraph('<font color="#7A6A58"><b>Dietary Recommendations:</b></font> ' + ' · '.join(diet), styles['small']))
        story.append(Spacer(1, 4*mm))

    story.append(PageBreak())

    # ── Wealth ────────────────────────────────────────────────────────────────
    wealth = report.get('wealth_prediction', {})
    if wealth:
        story.append(section_divider('Wealth & Finance', styles))
        if wealth.get('overall_rating'):
            story.append(rating_para(wealth.get('overall_rating', '')))
            story.append(Spacer(1, 2*mm))
        two_col_bullets(
            'Primary Income Sources', wealth.get('primary_income_sources', []),
            'Good Investments',       wealth.get('good_investments', [])
        )
        avoid = wealth.get('avoid', [])
        if avoid:
            story.append(Paragraph('<font color="#C62828"><b>Avoid:</b></font> ' + ' · '.join(avoid), styles['small']))
        story.append(Spacer(1, 4*mm))

    # ── Dasha Periods ─────────────────────────────────────────────────────────
    cur_dasha = report.get('current_dasha', {})
    dasha_tl  = report.get('dasha_timeline', [])
    if cur_dasha or dasha_tl:
        story.append(section_divider('Dasha Periods', styles))
        if cur_dasha:
            planet_name = cur_dasha.get('mahadasha', '')
            period      = cur_dasha.get('period', '')
            story.append(Paragraph(f'<font color="#C5A059"><b>Current Mahadasha: {planet_name} ({period})</b></font>', styles['body']))
            for eff in cur_dasha.get('effects', []):
                story.append(bullet_para(eff))
            story.append(Spacer(1, 3*mm))
        if dasha_tl:
            story.append(Paragraph('<font color="#7A6A58"><b>Upcoming Mahadashas</b></font>', styles['small']))
            d_rows = [[
                Paragraph('<b>Period</b>', styles['small']),
                Paragraph('<b>Mahadasha</b>', styles['small']),
                Paragraph('<b>Key Effects</b>', styles['small']),
            ]]
            for d in dasha_tl:
                planet = (d.get('planet','') or '').replace(' Mahadasha','').replace(' Dasha','')
                period = d.get('period', '–')
                effects_list = d.get('effects', [])
                effects_str  = ' · '.join(effects_list[:2]) if effects_list else ''
                d_rows.append([
                    Paragraph(period, styles['small']),
                    Paragraph(f'<b>{planet} Mahadasha</b>', styles['small']),
                    Paragraph(effects_str, styles['small']),
                ])
            dt = Table(d_rows, colWidths=[30*mm, 40*mm, CONTENT_W - 70*mm])
            dt.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), DARK_BG),
                ('TEXTCOLOR',  (0,0), (-1,0), GOLD),
                ('GRID',       (0,0), (-1,-1), 0.3, BORDER_GREY),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, CREAM_DARK]),
                ('PADDING',    (0,0), (-1,-1), 5),
                ('BOX',        (0,0), (-1,-1), 0.8, GOLD),
            ]))
            story.append(dt)
        story.append(Spacer(1, 4*mm))

    # ── Doshas & Yogas ────────────────────────────────────────────────────────
    mangal = report.get('mangal_dosha', {})
    yogas  = report.get('benefic_yogas', [])
    if mangal or yogas:
        story.append(section_divider('Doshas & Yogas', styles))
        if mangal:
            has_dosha = mangal.get('has_dosha') or mangal.get('present', False)
            severity  = mangal.get('severity', '')
            dosha_text = f'⚠ Mangal Dosha PRESENT — Severity: {severity}' if has_dosha else '✓ Mangal Dosha: Not Present'
            dosha_color = '#C62828' if has_dosha else '#2E7D32'
            story.append(Paragraph(f'<font color="{dosha_color}"><b>{dosha_text}</b></font>', styles['body']))
            mars_house = mangal.get('mars_house', '')
            if mars_house:
                story.append(Paragraph(f'Mars placed in House {mars_house}', styles['small']))
            for rem in mangal.get('remedies', []):
                story.append(bullet_para(rem))
            story.append(Spacer(1, 3*mm))
        if yogas:
            story.append(Paragraph('<font color="#2E7D32"><b>Benefic Yogas Present:</b></font>', styles['small']))
            yoga_names = []
            for y in yogas:
                n = y.get('name', y) if isinstance(y, dict) else str(y)
                e = y.get('effect', '') if isinstance(y, dict) else ''
                yoga_names.append(f'{n} — {e}' if e else n)
            for yn in yoga_names:
                story.append(bullet_para(yn))
        story.append(Spacer(1, 4*mm))

    story.append(PageBreak())

    # ── Remedies & Recommendations ────────────────────────────────────────────
    gem_r  = report.get('gemstone_remedies', [])
    man_r  = report.get('mantra_remedies', [])
    life_r = report.get('lifestyle_remedies', [])
    lucky_n = report.get('lucky_numbers', [])
    lucky_c = report.get('lucky_colors', [])
    lucky_d = report.get('lucky_days', [])
    lucky_dir = report.get('lucky_direction', '')
    num     = report.get('numerology', {})

    if gem_r or man_r or life_r:
        story.append(section_divider('Remedies & Recommendations', styles))
        if gem_r:
            story.append(Paragraph('<font color="#7A6A58"><b>Gemstones</b></font>', styles['small']))
            for g in gem_r:
                stone = g.get('stone', g) if isinstance(g, dict) else str(g)
                extra = []
                if isinstance(g, dict):
                    if g.get('planet'):  extra.append(f"Planet: {g['planet']}")
                    if g.get('benefit'): extra.append(g['benefit'])
                text = stone + (' — ' + ' · '.join(extra) if extra else '')
                story.append(bullet_para(text))
            story.append(Spacer(1, 3*mm))

        if man_r:
            story.append(Paragraph('<font color="#7A6A58"><b>Mantras</b></font>', styles['small']))
            for m in man_r:
                mantra = m.get('mantra', m) if isinstance(m, dict) else str(m)
                chant  = m.get('chanting', '') if isinstance(m, dict) else ''
                text   = mantra + (f' — {chant}' if chant else '')
                story.append(bullet_para(text))
            story.append(Spacer(1, 3*mm))

        if life_r:
            story.append(Paragraph('<font color="#7A6A58"><b>Lifestyle Practices</b></font>', styles['small']))
            for l in life_r:
                story.append(bullet_para(l))
            story.append(Spacer(1, 3*mm))

    # ── Lucky Elements ────────────────────────────────────────────────────────
    if lucky_n or lucky_c or lucky_d:
        story.append(section_divider('Lucky Elements', styles))
        lucky_data = []
        if lucky_n: lucky_data.append(['Lucky Numbers', ', '.join(str(x) for x in lucky_n)])
        if lucky_c: lucky_data.append(['Lucky Colours', ', '.join(lucky_c)])
        if lucky_d: lucky_data.append(['Lucky Days',    ', '.join(lucky_d)])
        if lucky_dir: lucky_data.append(['Lucky Direction', lucky_dir])
        story.append(info_table(lucky_data, styles))
        story.append(Spacer(1, 4*mm))

    # ── Numerology ────────────────────────────────────────────────────────────
    if num:
        story.append(section_divider('Numerology', styles))
        num_data = []
        if num.get('life_path'):     num_data.append(['Life Path Number', str(num['life_path'])])
        if num.get('destiny_number'):num_data.append(['Destiny Number', str(num['destiny_number'])])
        if num.get('soul_number'):   num_data.append(['Soul Number', str(num['soul_number'])])
        if num_data:
            story.append(info_table(num_data, styles))
        story.append(Spacer(1, 4*mm))

    # ── Footer note ───────────────────────────────────────────────────────────
    story.append(Spacer(1, 6*mm))
    story.append(gold_rule())
    story.append(Paragraph(
        'This report is for reflective and informational purposes. '
        'Everyday Horoscope · everydayhoroscope.in · SkyHound Studios',
        styles['small']
    ))

    doc.build(story, onFirstPage=draw_page_border, onLaterPages=draw_page_border)

    buffer.seek(0)
    if password:
        buffer = apply_password(buffer, password)
    else:
        buffer.seek(0)

    return buffer
