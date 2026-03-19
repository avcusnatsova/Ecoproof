from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import pandas as pd
import io

# ── Color palette ─────────────────────────────────────────────────────────────
BLACK      = colors.HexColor('#060a08')
DARK       = colors.HexColor('#0b1410')
DARK2      = colors.HexColor('#0f1d16')
BORDER     = colors.HexColor('#1a3326')
GREEN      = colors.HexColor('#00e676')
GREEN_DIM  = colors.HexColor('#2e7d52')
GREEN_MID  = colors.HexColor('#4caf80')
WHITE      = colors.HexColor('#e0f2e9')
TEXT_DIM   = colors.HexColor('#7aad8f')
RED        = colors.HexColor('#ff1744')
ORANGE     = colors.HexColor('#ff6d00')
YELLOW     = colors.HexColor('#ffd600')
RED_BG     = colors.HexColor('#2a0008')
ORANGE_BG  = colors.HexColor('#2a1400')
YELLOW_BG  = colors.HexColor('#2a2000')

PW, PH = A4
ML = MR = 2*cm
MT = MB = 2*cm
CW = PW - ML - MR


def sev_colors(sev):
    s = str(sev).lower()
    if 'severe'   in s: return RED,    RED_BG
    if 'high'     in s: return ORANGE, ORANGE_BG
    if 'moderate' in s: return YELLOW, YELLOW_BG
    return GREEN, DARK


def generate_report(df: pd.DataFrame, output_path: str = None) -> bytes:

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=MT, bottomMargin=MB,
        title="EcoProof Anomaly Report"
    )

    # ── Styles ────────────────────────────────────────────────────────────────
    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    sty_logo     = S('logo',     fontName='Helvetica-Bold', fontSize=22, textColor=GREEN,   spaceAfter=2)
    sty_sub      = S('sub',      fontName='Helvetica',      fontSize=9,  textColor=GREEN_DIM, spaceAfter=16, letterSpacing=2)
    sty_h1       = S('h1',       fontName='Helvetica-Bold', fontSize=17, textColor=WHITE,   spaceAfter=6,  spaceBefore=4)
    sty_meta     = S('meta',     fontName='Helvetica',      fontSize=9,  textColor=TEXT_DIM,spaceAfter=2)
    sty_sec      = S('sec',      fontName='Helvetica-Bold', fontSize=11, textColor=GREEN,   spaceAfter=8,  spaceBefore=16)
    sty_body     = S('body',     fontName='Helvetica',      fontSize=9,  textColor=WHITE,   spaceAfter=4,  leading=14)
    sty_footer   = S('footer',   fontName='Helvetica',      fontSize=8,  textColor=TEXT_DIM,alignment=TA_CENTER)
    sty_page_num = S('pgnum',    fontName='Helvetica',      fontSize=8,  textColor=GREEN_DIM,alignment=TA_RIGHT)

    # ── Data prep ─────────────────────────────────────────────────────────────
    ts         = datetime.now().strftime('%B %d, %Y  %I:%M %p')
    total_rows = len(df)
    anom_df    = df[df['anomaly_flag'] == True].copy() if 'anomaly_flag' in df.columns else pd.DataFrame()
    total_a    = len(anom_df)
    severe_n   = len(anom_df[anom_df['anomaly_severity'].str.lower().str.contains('severe',   na=False)]) if not anom_df.empty else 0
    high_n     = len(anom_df[anom_df['anomaly_severity'].str.lower().str.contains('high',     na=False)]) if not anom_df.empty else 0
    mod_n      = len(anom_df[anom_df['anomaly_severity'].str.lower().str.contains('moderate', na=False)]) if not anom_df.empty else 0
    plants     = df[['plant_name','plant_id']].drop_duplicates() if 'plant_name' in df.columns else pd.DataFrame()

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 — COVER
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.8*cm))

    # Logo + brand
    story.append(Paragraph("EcoProof", sty_logo))
    story.append(Paragraph("INDUSTRIAL POLLUTION MONITORING SYSTEM", sty_sub))
    story.append(HRFlowable(width=CW, thickness=1, color=BORDER, spaceAfter=20))

    story.append(Paragraph("Anomaly Detection &amp; Compliance Report", sty_h1))
    story.append(Paragraph(f"Generated: {ts}", sty_meta))
    story.append(Spacer(1, 0.6*cm))

    # Summary table
    col_w = [CW * 0.6, CW * 0.4]
    summary_data = [
        ["METRIC", "VALUE"],
        ["Total Sensor Readings",    f"{total_rows:,}"],
        ["Total Plants Monitored",   f"{len(plants)}"],
        ["Total Anomalies Detected", f"{total_a:,}"],
        ["Severe Anomalies",         f"{severe_n}"],
        ["High Anomalies",           f"{high_n}"],
        ["Moderate Anomalies",       f"{mod_n}"],
    ]

    summary_table = Table(summary_data, colWidths=col_w, hAlign='LEFT')
    summary_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND',   (0, 0), (-1,  0), DARK2),
        ('TEXTCOLOR',    (0, 0), (-1,  0), GREEN_MID),
        ('FONTNAME',     (0, 0), (-1,  0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0, 0), (-1,  0), 8),
        ('LETTERSPACE',  (0, 0), (-1,  0), 1),
        # Data rows
        ('BACKGROUND',   (0, 1), (-1, -1), DARK),
        ('FONTNAME',     (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',     (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',    (0, 1), (0,  -1), TEXT_DIM),
        ('TEXTCOLOR',    (1, 1), (1,  -1), WHITE),
        # Highlight anomaly rows
        ('TEXTCOLOR',    (1, 4), (1,  4),  RED),
        ('TEXTCOLOR',    (1, 5), (1,  5),  ORANGE),
        ('TEXTCOLOR',    (1, 6), (1,  6),  YELLOW),
        # Alternating rows
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [DARK, DARK2]),
        # Borders
        ('LINEBELOW',    (0, 0), (-1,  0), 0.5, GREEN_DIM),
        ('LINEBELOW',    (0, 1), (-1, -1), 0.3, BORDER),
        ('BOX',          (0, 0), (-1, -1), 0.5, BORDER),
        # Padding
        ('TOPPADDING',   (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 8),
        ('LEFTPADDING',  (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.5*cm))

    # Severity bar — visual indicator
    sev_data = [["SEVERE", "HIGH", "MODERATE", "NORMAL"]]
    sev_vals = [[f"{severe_n}", f"{high_n}", f"{mod_n}", f"{total_rows - total_a}"]]
    sev_table = Table(sev_data + sev_vals, colWidths=[CW/4]*4, hAlign='LEFT')
    sev_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, -1), RED_BG),
        ('BACKGROUND',    (1, 0), (1, -1), ORANGE_BG),
        ('BACKGROUND',    (2, 0), (2, -1), YELLOW_BG),
        ('BACKGROUND',    (3, 0), (3, -1), DARK),
        ('TEXTCOLOR',     (0, 0), (0, -1), RED),
        ('TEXTCOLOR',     (1, 0), (1, -1), ORANGE),
        ('TEXTCOLOR',     (2, 0), (2, -1), YELLOW),
        ('TEXTCOLOR',     (3, 0), (3, -1), GREEN),
        ('FONTNAME',      (0, 0), (-1,  0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1,  0), 8),
        ('FONTNAME',      (0, 1), (-1,  1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 1), (-1,  1), 18),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEAFTER',     (0, 0), (2,  -1), 0.5, BORDER),
        ('BOX',           (0, 0), (-1, -1), 0.5, BORDER),
    ]))
    story.append(sev_table)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — PLANT SUMMARY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Plant-wise Anomaly Summary", sty_sec))
    story.append(HRFlowable(width=CW, thickness=0.5, color=BORDER, spaceAfter=12))

    col_widths = [CW*0.32, CW*0.12, CW*0.12, CW*0.12, CW*0.12, CW*0.12, CW*0.08]
    plant_rows = [["PLANT NAME", "ID", "TOTAL", "SEVERE", "HIGH", "MOD", "LOC"]]

    loc_map = {
        'PLT109':'MP','PLT107':'CG','PLT106':'HR','PLT103':'OD',
        'PLT108':'GJ','PLT105':'GJ','PLT102':'GJ','PLT101':'TG',
        'PLT100':'JH','PLT104':'KA'
    }

    for _, p in plants.iterrows():
        pid   = p['plant_id']
        pname = p['plant_name']
        pa    = anom_df[anom_df['plant_id'] == pid] if not anom_df.empty else pd.DataFrame()
        ps    = len(pa[pa['anomaly_severity'].str.lower().str.contains('severe',   na=False)]) if not pa.empty else 0
        ph    = len(pa[pa['anomaly_severity'].str.lower().str.contains('high',     na=False)]) if not pa.empty else 0
        pm    = len(pa[pa['anomaly_severity'].str.lower().str.contains('moderate', na=False)]) if not pa.empty else 0
        plant_rows.append([pname, pid, str(ps+ph+pm), str(ps), str(ph), str(pm), loc_map.get(pid,'')])

    plant_table = Table(plant_rows, colWidths=col_widths, hAlign='LEFT')
    ts_plant = [
        ('BACKGROUND',    (0, 0), (-1,  0), DARK2),
        ('TEXTCOLOR',     (0, 0), (-1,  0), GREEN_MID),
        ('FONTNAME',      (0, 0), (-1,  0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1,  0), 8),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [DARK, DARK2]),
        ('TEXTCOLOR',     (0, 1), (0,  -1), WHITE),
        ('TEXTCOLOR',     (1, 1), (1,  -1), TEXT_DIM),
        ('TEXTCOLOR',     (2, 1), (2,  -1), WHITE),
        ('FONTNAME',      (2, 1), (2,  -1), 'Helvetica-Bold'),
        ('TEXTCOLOR',     (3, 1), (3,  -1), RED),
        ('TEXTCOLOR',     (4, 1), (4,  -1), ORANGE),
        ('TEXTCOLOR',     (5, 1), (5,  -1), YELLOW),
        ('TEXTCOLOR',     (6, 1), (6,  -1), TEXT_DIM),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('ALIGN',         (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN',         (0, 0), (0,  -1), 'LEFT'),
        ('LINEBELOW',     (0, 0), (-1,  0), 0.5, GREEN_DIM),
        ('LINEBELOW',     (0, 1), (-1, -1), 0.3, BORDER),
        ('BOX',           (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (0,  -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (1, 0), (-1, -1), 6),
    ]
    plant_table.setStyle(TableStyle(ts_plant))
    story.append(plant_table)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3 — TOP FLAGGED READINGS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Top Flagged Sensor Readings", sty_sec))
    story.append(HRFlowable(width=CW, thickness=0.5, color=BORDER, spaceAfter=12))

    if not anom_df.empty:
        top = anom_df.sort_values('aqi', ascending=False).head(20)
        col_w3 = [CW*0.10, CW*0.26, CW*0.10, CW*0.09, CW*0.11, CW*0.11, CW*0.11, CW*0.12]
        anom_rows = [["SEV.", "PLANT", "SENSOR", "AQI", "PM2.5", "PM10", "NO2", "SO2"]]

        for _, row in top.iterrows():
            sev = str(row.get('anomaly_severity','?')).upper()[:3]
            anom_rows.append([
                sev,
                str(row.get('plant_name','?')),
                str(row.get('sensor_id','?')),
                str(int(float(row.get('aqi', 0)))),
                str(round(float(row.get('pm2_5',   0)), 1)),
                str(round(float(row.get('pm10',    0)), 1)),
                str(round(float(row.get('no2_level',0)), 1)),
                str(round(float(row.get('so2_level',0)), 1)),
            ])

        anom_table = Table(anom_rows, colWidths=col_w3, hAlign='LEFT')
        ts_anom = [
            ('BACKGROUND',    (0, 0), (-1,  0), DARK2),
            ('TEXTCOLOR',     (0, 0), (-1,  0), GREEN_MID),
            ('FONTNAME',      (0, 0), (-1,  0), 'Helvetica-Bold'),
            ('FONTSIZE',      (0, 0), (-1,  0), 8),
            ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE',      (0, 1), (-1, -1), 8),
            ('TEXTCOLOR',     (1, 1), (1,  -1), WHITE),
            ('TEXTCOLOR',     (2, 1), (-1, -1), TEXT_DIM),
            ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN',         (1, 0), (1,  -1), 'LEFT'),
            ('LINEBELOW',     (0, 0), (-1,  0), 0.5, GREEN_DIM),
            ('LINEBELOW',     (0, 1), (-1, -1), 0.3, BORDER),
            ('BOX',           (0, 0), (-1, -1), 0.5, BORDER),
            ('TOPPADDING',    (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING',   (0, 0), (-1, -1), 6),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
        ]
        # Color severity column per row
        for i, row in enumerate(anom_rows[1:], 1):
            tc, bg = sev_colors(row[0])
            ts_anom.append(('TEXTCOLOR',  (0, i), (0, i), tc))
            ts_anom.append(('BACKGROUND', (0, i), (0, i), bg))
            ts_anom.append(('ROWBACKGROUNDS', (1, i), (-1, i), [DARK if i % 2 == 1 else DARK2]))

        anom_table.setStyle(TableStyle(ts_anom))
        story.append(anom_table)
    else:
        story.append(Paragraph("No anomalies detected.", sty_body))

    # Footer note
    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width=CW, thickness=0.5, color=BORDER, spaceAfter=8))
    story.append(Paragraph(
        "All readings have been logged to the EcoProof blockchain for tamper-proof record keeping. "
        "This report is auto-generated and reflects the latest anomaly detection run.",
        sty_footer
    ))

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story)
    pdf_bytes = buf.getvalue()
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
    return pdf_bytes