import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ─── CONFIGURE THESE ──────────────────────────────────────────────────────────
SMTP_EMAIL    = "avcusnatsova@gmail.com"       # Gmail you send FROM
SMTP_PASSWORD = "yfmy vgae youw dpvr"     # Gmail App Password (not your login password)
ALERT_TO      = "avcusnatsova@gmail.com"       # Email to receive alerts (can be same)
# ──────────────────────────────────────────────────────────────────────────────


def send_alert_email(anomaly_summary: list[dict]):
    """
    anomaly_summary: list of dicts with keys:
        plant_name, plant_id, severity, aqi, pm2_5, sensor_id
    """
    if not anomaly_summary:
        return False, "No anomalies to report"

    severe   = [a for a in anomaly_summary if 'severe'   in str(a.get('severity','')).lower()]
    high     = [a for a in anomaly_summary if 'high'     in str(a.get('severity','')).lower()]
    moderate = [a for a in anomaly_summary if 'moderate' in str(a.get('severity','')).lower()]

    timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    total     = len(anomaly_summary)

    # ── Subject ────────────────────────────────────────────────────────────────
    if severe:
        subject = f"🚨 CRITICAL — EcoProof: {len(severe)} Severe Anomalies Detected"
    elif high:
        subject = f"⚠️ ALERT — EcoProof: {len(high)} High Anomalies Detected"
    else:
        subject = f"📊 NOTICE — EcoProof: {total} Anomalies Detected"

    # ── HTML Body ──────────────────────────────────────────────────────────────
    def row_color(sev):
        s = str(sev).lower()
        if 'severe'   in s: return '#4a0000', '#ff5252'
        if 'high'     in s: return '#3a1a00', '#ff9800'
        if 'moderate' in s: return '#2a2a00', '#ffeb3b'
        return '#003a10', '#4caf50'

    rows_html = ""
    for a in anomaly_summary[:15]:  # cap at 15 in email
        bg, color = row_color(a.get('severity', ''))
        rows_html += f"""
        <tr style="background:{bg};">
            <td style="padding:10px;color:{color};font-weight:bold;">{a.get('severity','?').upper()}</td>
            <td style="padding:10px;color:#e8f5e9;">{a.get('plant_name','?')}</td>
            <td style="padding:10px;color:#e8f5e9;">{a.get('plant_id','?')}</td>
            <td style="padding:10px;color:#e8f5e9;">{a.get('sensor_id','?')}</td>
            <td style="padding:10px;color:#e8f5e9;">{a.get('aqi','?')}</td>
            <td style="padding:10px;color:#e8f5e9;">{round(float(a.get('pm2_5', 0)), 1)}</td>
        </tr>"""

    html = f"""
    <html><body style="margin:0;padding:0;background:#0a0f0d;font-family:Arial,sans-serif;">
    <div style="max-width:700px;margin:0 auto;padding:30px;">

        <!-- Header -->
        <div style="background:linear-gradient(135deg,#0d1f17,#112318);border:1px solid #1e4d30;border-radius:12px;padding:30px;margin-bottom:20px;">
            <div style="font-size:28px;font-weight:bold;color:#4caf50;">🌿 EcoProof</div>
            <div style="font-size:13px;color:#4caf80;letter-spacing:2px;margin-top:4px;">INDUSTRIAL POLLUTION MONITORING</div>
            <hr style="border-color:#1e3a2a;margin:20px 0;">
            <div style="font-size:22px;color:#e8f5e9;font-weight:bold;">Anomaly Detection Report</div>
            <div style="font-size:13px;color:#81c784;margin-top:6px;">{timestamp}</div>
        </div>

        <!-- Summary pills -->
        <div style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap;">
            <div style="background:#1a0000;border:1px solid #f44336;border-radius:8px;padding:12px 20px;text-align:center;">
                <div style="font-size:28px;font-weight:bold;color:#f44336;">{len(severe)}</div>
                <div style="font-size:11px;color:#ff5252;letter-spacing:1px;">SEVERE</div>
            </div>
            <div style="background:#1a0d00;border:1px solid #ff9800;border-radius:8px;padding:12px 20px;text-align:center;">
                <div style="font-size:28px;font-weight:bold;color:#ff9800;">{len(high)}</div>
                <div style="font-size:11px;color:#ffb74d;letter-spacing:1px;">HIGH</div>
            </div>
            <div style="background:#1a1a00;border:1px solid #ffeb3b;border-radius:8px;padding:12px 20px;text-align:center;">
                <div style="font-size:28px;font-weight:bold;color:#ffeb3b;">{len(moderate)}</div>
                <div style="font-size:11px;color:#fff176;letter-spacing:1px;">MODERATE</div>
            </div>
            <div style="background:#0d1f17;border:1px solid #4caf50;border-radius:8px;padding:12px 20px;text-align:center;">
                <div style="font-size:28px;font-weight:bold;color:#4caf50;">{total}</div>
                <div style="font-size:11px;color:#81c784;letter-spacing:1px;">TOTAL</div>
            </div>
        </div>

        <!-- Table -->
        <div style="background:#0d1f17;border:1px solid #1e3a2a;border-radius:12px;overflow:hidden;margin-bottom:20px;">
            <div style="padding:16px 20px;border-bottom:1px solid #1e3a2a;">
                <span style="color:#4caf80;font-size:12px;letter-spacing:2px;text-transform:uppercase;">Flagged Readings</span>
            </div>
            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
                <thead>
                    <tr style="background:#112318;">
                        <th style="padding:10px;color:#4caf80;font-size:11px;text-align:left;">SEVERITY</th>
                        <th style="padding:10px;color:#4caf80;font-size:11px;text-align:left;">PLANT</th>
                        <th style="padding:10px;color:#4caf80;font-size:11px;text-align:left;">ID</th>
                        <th style="padding:10px;color:#4caf80;font-size:11px;text-align:left;">SENSOR</th>
                        <th style="padding:10px;color:#4caf80;font-size:11px;text-align:left;">AQI</th>
                        <th style="padding:10px;color:#4caf80;font-size:11px;text-align:left;">PM2.5</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>

        <!-- Footer -->
        <div style="text-align:center;color:#4caf60;font-size:12px;padding:10px;">
            This is an automated alert from EcoProof Monitoring System.<br>
            All anomalies have been logged to the blockchain for tamper-proof record keeping.
        </div>

    </div></body></html>
    """

    # ── Send ───────────────────────────────────────────────────────────────────
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = SMTP_EMAIL
        msg["To"]      = ALERT_TO
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, ALERT_TO, msg.as_string())

        return True, f"Alert sent to {ALERT_TO}"

    except Exception as e:
        return False, str(e)


def build_anomaly_summary(df):
    """Build anomaly summary list from a dataframe."""
    import pandas as pd
    anom = df[df['anomaly_flag'] == True].copy() if 'anomaly_flag' in df.columns else pd.DataFrame()
    if anom.empty:
        return []

    summary = []
    for _, row in anom.head(50).iterrows():
        summary.append({
            "plant_name": row.get("plant_name", "Unknown"),
            "plant_id":   row.get("plant_id",   "?"),
            "sensor_id":  row.get("sensor_id",  "?"),
            "severity":   row.get("anomaly_severity", "Unknown"),
            "aqi":        row.get("aqi",    "?"),
            "pm2_5":      row.get("pm2_5",  0),
        })
    return summary