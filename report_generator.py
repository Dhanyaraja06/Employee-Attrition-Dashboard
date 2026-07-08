
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from datetime import datetime
import os


def generate_report(
    filename,
    prediction,
    stay_probability,
    leave_probability,
    employee_details,
    reasons,
    logo_path="assets/logo for HR.png"
):
    doc = SimpleDocTemplate(
        filename,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#1565C0")

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#1565C0")

    normal = styles["BodyText"]

    story = []

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=1.0*inch, height=1.0*inch)
        logo.hAlign = "CENTER"
        story.append(logo)

    story.append(Paragraph("<b>Employee Attrition Prediction Report</b>", title_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(
        Paragraph(
            f"<b>Generated On:</b> {datetime.now().strftime('%d %B %Y | %I:%M %p')}",
            normal,
        )
    )

    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Prediction Result</b>", heading_style))

    pred_color = "#2E7D32" if "Stay" in prediction else "#C62828"

    story.append(
        Paragraph(
            f'<font color="{pred_color}"><b>{prediction}</b></font>',
            normal,
        )
    )

    story.append(Paragraph(f"Stay Probability : {stay_probability:.2f}%", normal))
    story.append(Paragraph(f"Leave Probability : {leave_probability:.2f}%", normal))

    story.append(Spacer(1, 0.25*inch))

    story.append(Paragraph("<b>Employee Details</b>", heading_style))

    data = [["Field", "Value"]]

    for k, v in employee_details.items():
        data.append([k, str(v)])

    table = Table(data, colWidths=[2.5*inch, 3.2*inch])

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1976D2")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BOTTOMPADDING",(0,0),(-1,0),5),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),
    ]))

    story.append(table)

    story.append(Spacer(1,0.3*inch))

    story.append(Paragraph("<b>Risk Factors</b>", heading_style))

    if reasons:
        for r in reasons:
            story.append(Paragraph(r.replace("•","&#8226;"), normal))
    else:
        story.append(Paragraph("No major risk factors identified.", normal))

    story.append(Spacer(1, 0.10 * inch))
    story.append(Paragraph("<b>Recommendations</b>", heading_style))

    if "Stay" in prediction:
        recs = [
            "Continue employee engagement practices.",
            "Encourage continuous learning and development.",
            "Maintain healthy work-life balance.",
            "Recognize employee achievements regularly."
        ]
    else:
        recs = [
            "Conduct a one-to-one discussion with the employee.",
            "Review compensation and career growth opportunities.",
            "Reduce overtime and improve work-life balance.",
            "Increase recognition and employee engagement."
        ]

    for r in recs:
        story.append(Paragraph(f"&#8226; {r}", normal))

    # Space before footer
    story.append(Spacer(1, 0.25 * inch))

    # Horizontal line
    line = Table([[""]], colWidths=[6.4 * inch])
    line.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, -1), 1, colors.HexColor("#1976D2"))
    ]))
    story.append(line)

    story.append(Spacer(1, 0.12 * inch))

    story.append(Paragraph("<b>Dashboard Information</b>", heading_style))
    story.append(Spacer(1, 0.1 * inch))

    story.append(
        Paragraph(
            "<b>HR INSIGHTS - Employee Attrition Prediction Dashboard</b>",
            normal
        )
    )

    story.append(
        Paragraph(
            "Developed by <b>Dhanya R</b>",
            normal
        )
    )

    story.append(
        Paragraph(
            "<font color='grey'>Powered by Python • Streamlit • Scikit-Learn • Plotly</font>",
            normal
        )
    )

    doc.build(story)
