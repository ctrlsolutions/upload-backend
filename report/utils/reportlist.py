from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import PCMYKColor, HexColor
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from reportlab.lib.validators import Auto
from reportlab.lib.formatters import DecimalFormatter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.corp import cm

from reportlab.platypus import HRFlowable
from reportlab.platypus import Image

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def generate_report(context, filename="report-list.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    # Logo
    # logo = Image("HEADER.png", width=86, height=26)  # Adjust size as needed
    # logo.hAlign = 'CENTER'  # or 'CENTER' or 'RIGHT'
    # elements.append(logo)
    # elements.append(Spacer(1, 32))

    # Title
    title = Paragraph("""<font color="#800000" size="12"><b>Comprehensive List of Submitted Reports</b></font>""", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Report Table
    report_data = [
        ["Type", "Title", "Submitted by", "Date Submitted"]
    ]
    
    # Sample data - replace with your actual submission data
    for item in context.get("detailed_submissions", []):
        report_data.append([
            item.get("type", ""),
            item.get("title", ""),
            item.get("submitted_by", ""),
            datetime.strptime(item.get("date_submitted"), "%Y-%m-%d").strftime("%m-%d-%Y")
        ])

    # Column widths (adjust as needed)
    col_widths = [80, 180, 120, 100]
    
    report_table = Table(
        report_data, 
        colWidths=col_widths,
        hAlign="CENTER"
    )

    table_style = TableStyle([
        # Header styling
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#751113")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        
        # Grid and alignment
        ("GRID", (0, 0), (-1, -1), 1, colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        
        # Font settings
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        
        # Column-specific alignment
        ("ALIGN", (3, 1), (3, -1), "LEFT"),  # Center-align dates
    ])

    # Alternating row colors
    for i in range(1, len(report_data)):
        bg_color = colors.whitesmoke if i % 2 == 0 else colors.white
        table_style.add("BACKGROUND", (0, i), (-1, i), bg_color)

    report_table.setStyle(table_style)
    elements.append(report_table)
    elements.append(Spacer(1, 24))

    doc.build(elements)
    print(f"✅ PDF generated: {filename}")


context = {
    "scope": "Department",
    "department": "Department of Biology and Ecological Systems",
    "college": "College of Social Sciences",
    "university": "UP Cebu",
    "timeframe": "6 months",
    "generated_by": "Caleb Josh S. Berandoy",
    "generated_on": datetime.now().strftime('%m-%d-%Y'),
    "detailed_submissions": [
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
        {
            "type": "Research", 
            "title": "Machine Learning in Healthcare", 
            "submitted_by": "Dr. Smith", 
            "date_submitted": "2025-01-15"
        },
        {
            "type": "Publication", 
            "title": "Climate Change Patterns", 
            "submitted_by": "Prof. Johnson", 
            "date_submitted": "2025-02-20"
        },
    ]
}

generate_report(context)

