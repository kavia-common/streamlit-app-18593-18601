from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from typing import Dict, List
from datetime import datetime

def generate_pdf(buffer, branding_title: str, profile: Dict, kpis: Dict, allocation: Dict[str, float], goal_table: List[Dict]):
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Cover
    c.setFillColor(colors.HexColor('#1f4b99'))
    c.rect(0, height-120, width, 120, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(72, height-80, branding_title)
    c.setFont("Helvetica", 12)
    c.drawString(72, height-100, f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}" )
    c.showPage()

    # Profile & KPIs
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height-72, "Profile Summary")
    c.setFont("Helvetica", 11)
    y = height-100
    for k in ["income","monthly_expenses","city","risk_tolerance","existing_savings","debts","savings_rate_target"]:
        c.drawString(72, y, f"{k.replace('_',' ').title()}: {profile.get(k)}")
        y -= 16

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y-16, "KPIs")
    c.setFont("Helvetica", 11)
    y -= 44
    for k, v in kpis.items():
        c.drawString(72, y, f"{k}: {v}")
        y -= 16
    c.showPage()

    # Allocation
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height-72, "Recommended Allocation")
    c.setFont("Helvetica", 11)
    y = height-100
    for asset, pct in allocation.items():
        c.drawString(72, y, f"{asset}: {pct}%")
        y -= 16

    # Goals table
    y -= 16
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, "Goals")
    c.setFont("Helvetica", 11)
    y -= 24
    for g in goal_table:
        line = f"{g.get('name')} | Target: ${g.get('target_amount')} | Current: ${g.get('current_amount')} | Horizon: {g.get('horizon_years')}y | Priority: {g.get('priority')}"
        c.drawString(72, y, line)
        y -= 16
        if y < 72:
            c.showPage()
            y = A4[1]-72

    c.showPage()
    c.save()
