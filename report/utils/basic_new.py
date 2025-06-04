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

def calculate_timeframe(timeframe_str, generated_date_str):
    """Convert timeframe like '6 months' to '01-01-2025 - 05-19-2025 (6 months)'"""
    try:
        # Parse generated_on date (now handling MM-DD-YYYY format)
        generated_date = datetime.strptime(generated_date_str, '%m-%d-%Y')
        original_timeframe = timeframe_str  # Save for suffix
        
        if "month" in timeframe_str.lower():
            months = int(timeframe_str.split()[0])
            start_date = generated_date - relativedelta(months=months)
        elif "year" in timeframe_str.lower():
            years = int(timeframe_str.split()[0])
            start_date = generated_date - relativedelta(years=years)
        else:
            return original_timeframe  # Return original if format is invalid
        
        date_range = f"{start_date.strftime('%m-%d-%Y')} - {generated_date.strftime('%m-%d-%Y')}"
        return f"{date_range} ({original_timeframe})"
    
    except (ValueError, IndexError, AttributeError):
        return timeframe_str  # Fallback to original text if parsing fails

class ProgressBar(Flowable):
    def __init__(self, width=400, height=10, progress=0, **kwargs):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.progress = max(0, min(100, progress))  # Ensure progress is between 0-100
        self.fill_color = kwargs.get('fill_color', HexColor("#014421"))
        self.empty_color = kwargs.get('empty_color', colors.lightgrey)
        self.text_color = kwargs.get('text_color', colors.black)
        self.border_color = kwargs.get('border_color', colors.black)
        self.border_width = kwargs.get('border_width', 1)
        self.rounded = kwargs.get('rounded', True)
    
    def draw(self):
        self.canv.saveState()
        
        x_offset = 50

        # Draw empty background
        self.canv.setFillColor(self.empty_color)
        self.canv.setStrokeColor(self.border_color)
        self.canv.setLineWidth(self.border_width)
        
        if self.rounded:
            # Draw rounded rectangle background
            self.canv.roundRect(x_offset, 0, self.width, self.height, 
                              self.height/2, fill=1, stroke=1)
        else:
            # Draw simple rectangle background
            self.canv.rect(x_offset, 0, self.width, self.height, fill=1, stroke=1)
        
        # Draw filled progress
        progress_width = (self.width - self.border_width) * (self.progress / 100)
        self.canv.setFillColor(self.fill_color)
        
        if self.rounded and self.progress > 0:
            # Draw rounded progress - need to handle partial fills carefully
            if progress_width >= self.height/2:  # Enough to show rounded end
                self.canv.roundRect(x_offset, 0, progress_width, self.height, 
                                  self.height/2, fill=1, stroke=0)
            else:  # Too small for rounded end, just draw rectangle
                self.canv.rect(x_offset, 0, progress_width, self.height, fill=1, stroke=0)
        else:
            # Draw simple rectangle progress
            self.canv.rect(x_offset, 0, progress_width, self.height, fill=1, stroke=0)
        
        # Draw percentage text
        self.canv.setFillColor(self.text_color)
        self.canv.setFont("Helvetica", 9)
        text = f"{int(self.progress)}%"
        text_width = self.canv.stringWidth(text, "Helvetica", 10)
        self.canv.drawString(50 + self.width + 10, (self.height-10)/2, text)
        
        self.canv.restoreState()
    
    def wrap(self, *args):
        # Add extra space for the percentage text
        return (self.width + 50 + 50, self.height)

class LineChart(_DrawingEditorMixin, Drawing):
    def __init__(self, width=400, height=200, context=None, *args, **kw):
        Drawing.__init__(self, width, height, *args, **kw)
        
        # Get submission data from context
        submissions = context.get("submissions", [])
        if not submissions:
            return
            
        # Process submission data to group by month
        from collections import defaultdict
        import calendar
        
        monthly_data = defaultdict(int)
        for date_str, count in submissions:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            month_year = f"{date.year}-{date.month:02d}"
            monthly_data[month_year] += count
        
        # Sort by month
        sorted_months = sorted(monthly_data.keys())
        month_labels = []
        month_data = []
        
        for i, month_year in enumerate(sorted_months):
            year, month = map(int, month_year.split('-'))
            month_name = calendar.month_abbr[month]
            month_labels.append(f"{month_name}")
            month_data.append((i, monthly_data[month_year]))

        # Create LinePlot
        self._add(self, LinePlot(), name='chart', validate=None, desc='the main chart')
        self.width = 18.5*cm
        self.height = 5.4*cm
        self.chart.x = 50
        self.chart.y = 80
        self.chart.width = 14.3*cm
        self.chart.height = 3.4*cm
        self.chart.background = None
        
        # Set the processed data
        self.chart.data = [month_data]
        
        # Line styling
        self.chart.lines[0].strokeColor = HexColor("#014421")
        self.chart.lines[0].strokeWidth = 2
        self.chart.lines.symbol = makeMarker('Circle')
        self.chart.lines[0].symbol.strokeColor = HexColor("#014421")
        self.chart.lines[0].symbol.fillColor = HexColor("#014421")
        self.chart.lines[0].symbol.size = 6
        
        # X-axis configuration
        self.chart.xValueAxis.labels.fontName = 'Helvetica'
        self.chart.xValueAxis.labels.fontSize = 7
        self.chart.xValueAxis.tickDown = 0.1*cm
        self.chart.xValueAxis.strokeWidth = 0.75
        self.chart.xValueAxis.labelTextFormat = month_labels  # Use month labels
        self.chart.xValueAxis.valueMin = 0
        self.chart.xValueAxis.valueMax = len(month_labels) - 1
        self.chart.xValueAxis.forceZero = 1
        
        # Y-axis configuration
        self.chart.yValueAxis.labels.fontName = 'Helvetica'
        self.chart.yValueAxis.labels.fontSize = 7
        self.chart.yValueAxis.strokeWidth = 0.75
        self.chart.yValueAxis.tickLeft = 0.1*cm
        self.chart.yValueAxis.labelTextFormat = '%d'  # Integer format
        self.chart.yValueAxis.valueMin = 0
        max_value = max(count for _, count in month_data)
        self.chart.yValueAxis.valueMax = max_value + (1 if max_value < 5 else max_value * 0.2)  # Add some padding
        self.chart.yValueAxis.forceZero = 1

        # Add grid lines
        self.chart.xValueAxis.visibleGrid = 0
        self.chart.yValueAxis.visibleGrid = 1
        self.chart.xValueAxis.gridStrokeColor = colors.lightgrey
        self.chart.yValueAxis.gridStrokeColor = colors.lightgrey

def generate_report(context, filename="basic_new.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    # Logo
    logo = Image("HEADER.png", width=86, height=26)  # Adjust size as needed
    logo.hAlign = 'CENTER'  # or 'CENTER' or 'RIGHT'
    elements.append(logo)
    elements.append(Spacer(1, 12))

    # Header
    # First row table
    first_row_data = [
        ["Generated by", context['generated_by'], "Scope", context['scope']]
    ]

    first_row_table = Table(
        first_row_data,
        colWidths=[70, 160, 60, 160],  # Same column widths
        rowHeights=[12],
        style=TableStyle([
            # White borders for all cells
            ('GRID', (0, 0), (-1, -1), 5, colors.white),
            ('LINEBEFORE', (0, 0), (0, -1), 1, HexColor("#751113")),
            ('LINEBEFORE', (2, 0), (2, -1), 1, HexColor("#751113")),
            
            # Left align all content
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Set base font first (for all cells)
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            
            # Override to italic for columns 0 and 2
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Oblique'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Oblique'),
            
            # Consistent font size
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            
            # Padding for better spacing
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            
            # Text color for label cells
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor("#751113")),
            ('TEXTCOLOR', (2, 0), (2, -1), HexColor("#751113")),
        ])
    )

    generated_date = datetime.strptime(context['generated_on'], '%m-%d-%Y')
    context['timeframe'] = calculate_timeframe(context['timeframe'], context['generated_on'])

    # Second row table
    second_row_data = [
        ["Generated on", context['generated_on'], "Timeframe", context['timeframe']]
    ]

    second_row_table = Table(
        second_row_data,
        colWidths=[70, 160, 60, 160],  # Same column widths
        rowHeights=[12],
        style=TableStyle([
            # White borders for all cells
            ('GRID', (0, 0), (-1, -1), 5, colors.white),
            ('LINEBEFORE', (0, 0), (0, -1), 1, HexColor("#751113")),
            ('LINEBEFORE', (2, 0), (2, -1), 1, HexColor("#751113")),
            
            # Left align all content
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Set base font first (for all cells)
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            
            # Override to italic for columns 0 and 2
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Oblique'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Oblique'),
            
            # Consistent font size
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            
            # Padding for better spacing
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            
            # Text color for label cells
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor("#751113")),
            ('TEXTCOLOR', (2, 0), (2, -1), HexColor("#751113")),
        ])
    )

    # Add both tables to elements
    elements.append(first_row_table)
    elements.append(Spacer(1, 6))  # Smaller space between tables (adjust as needed)
    elements.append(second_row_table)
    elements.append(Spacer(1, 12))  # Space after the last table

    # Separator
    separator = HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey)
    elements.append(separator)
    elements.append(Spacer(1, 12))

    # Title
    title = Paragraph("<font size = 14><b>General Overview</b></font>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, -12))

    # Subtitle - Only show for Department scope
    if context['scope'].lower() == 'department':
        # Display the specific department name
        dept_name = context.get('department', 'Department')
        subtitle = Paragraph(f"<font size='10' color='#751113'>{dept_name}</font>", styles["Title"])
        elements.append(subtitle)
        elements.append(Spacer(1, -12))
    elif context['scope'].lower() == 'college':
        # For college, you might want to specify which college
        college_name = context.get('college', 'College')  # Add 'college' to context if needed
        subtitle = Paragraph(f"<font size='10' color='#751113'>{college_name}</font>", styles["Title"])
        elements.append(subtitle)
        elements.append(Spacer(1, -12))
    elif context['scope'].lower() == 'university':
        subtitle = Paragraph(f"<font size='10' color='#751113'>UP Cebu</font>", styles["Title"])
        elements.append(subtitle)
        elements.append(Spacer(1, -12))

    elements.append(Spacer(1, 24))

    # 1. Set your fixed target (adjust this number as needed)
    TARGET_SUBMISSIONS = 100  # 100 submissions = 100% progress
    
    # 2. Calculate current progress from context data
    current_submissions = sum(item["number_of_submissions"] for item in context["items"])
    
    # 3. Calculate percentage (capped at 100%)
    progress_percent = min(100, (current_submissions / TARGET_SUBMISSIONS) * 100)
    
    # Add progress bars section title
    # elements.append(Paragraph(
    #     """<font color="#800000"><b>Report Completion Progress</b></font>""",
    #     styles["Normal"]
    # ))
    # elements.append(Spacer(1, 12))

    # Define targets for each report type
    REPORT_TARGETS = {
        "Research": 15,
        "Publication as a Research Output": 10,
        "Paper Presentation as a Research Output": 20,
        "Patent as a Research Output": 10,
        "Other Research Output": 5,
        "Training Course and/or Advisory Service": 10,
        "Extension Program": 10,
        "Partnership with Stakeholder": 10,
        "Others": 7
    }

    # Create progress bars for each report type
    for item in context["items"]:
        # Calculate progress
        target = REPORT_TARGETS.get(item["type"], 1)  # Default to 1 if type not found
        progress = min(100, (item["number_of_submissions"] / target) * 100)
        
        # Create a modified style with left indent
        indented_style = styles["Normal"]
        indented_style.leftIndent = 50  # Adjust this value (in points) to move right
        # Create label and progress bar
        label = f"{item['type']} ({item['number_of_submissions']}/{target})"
        elements.append(Paragraph(
            f'<font size="8">{item["type"]} ({item["number_of_submissions"]}/{target})</font>',
            indented_style
        ))
        elements.append(Spacer(1, 2))  # Small space between label and bar
        
        progress_bar = ProgressBar(
            width=400,
            height=4,
            progress=progress,
            fill_color=HexColor("#014421"),
            text_color=colors.black,
            border_color=colors.white,
            rounded=True
        )
        elements.append(progress_bar)
        elements.append(Spacer(1, 8))  # Space between progress bars

    elements.append(Spacer(1, 48))  # Additional space before line chart

    # elements.append(Paragraph(
    #     """<font color="#800000"><b>Timeline</b></font>""",
    #     styles["Normal"]
    # ))
    # elements.append(Spacer(1, 28))

    # Line Chart
    elements.append(LineChart(context=context))
    elements.append(Spacer(1, -40))

    # Report Table
    report_data = [["Report Type", "# of Submissions"]]
    for item in context["items"]:
        report_data.append([item["type"], item["number_of_submissions"]])

    total = sum(item["number_of_submissions"] for item in context["items"])
    report_data.append(["Total", total])

    row_heights = [15] * len(report_data) 
    row_heights[0] = 15  # Slightly taller header row

    report_table = Table(report_data, hAlign="CENTER", colWidths=[200, 200], rowHeights=row_heights)

    table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#751113")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e1edd6")), 
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
    ])

    # Alternating row colors (start from row 1 since row 0 is the header)
    for i in range(1, len(report_data)-1):
        bg_color = colors.whitesmoke if i % 2 == 0 else colors.white
        table_style.add("BACKGROUND", (0, i), (-1, i), bg_color)

    report_table.setStyle(table_style)

    elements.append(report_table)
    elements.append(Spacer(1, 24))

    # Summary Stats - only show for Department/College/University scope
    # if context['scope'].lower() in ['department', 'college', 'university']:
    #     population = context.get("faculty_population", 0)
    #     reports_per_faculty = round(total / population, 2) if population else "N/A"
    #     summary_data = [
    #         ["Total Faculty Population", "Reports per Faculty Member"],
    #         [str(population), str(reports_per_faculty)]
    #     ]
    #     summary_table = Table(summary_data, colWidths=[210, 210], rowHeights=[15, 15])
    #     summary_table.setStyle(TableStyle([
    #         ("GRID", (0, 0), (-1, -1), 1, colors.white),
    #         ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    #         ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#751113")),
    #         ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    #         ("ALIGN", (1, 1), (-1, -1), "LEFT"),
    #         ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    #         ("FONTSIZE", (0, 0), (-1, -1), 8),
    #         ("FONTSIZE", (0, 0), (-1, 0), 8),
    #     ]))
    #     elements.append(summary_table)

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
    "faculty_population": 38,
    "items": [
        {"type": "Research", "number_of_submissions": 8},
        {"type": "Publication as a Research Output", "number_of_submissions": 4},
        {"type": "Paper Presentation as a Research Output", "number_of_submissions": 12},
        {"type": "Patent as a Research Output", "number_of_submissions": 10},
        {"type": "Other Research Output", "number_of_submissions": 5},
        {"type": "Training Course and/or Advisory Service", "number_of_submissions": 6},
        {"type": "Extension Program", "number_of_submissions": 7},
        {"type": "Partnership with Stakeholder", "number_of_submissions": 9},
        {"type": "Others", "number_of_submissions": 6}
    ],
    "submissions": [
        #format: (date, count)
        ("2025-01-12", 10),
        ("2025-02-03", 2),
        ("2025-03-14", 22),
        ("2025-04-20", 4),
        ("2025-05-05", 3),
        ("2025-06-15", 28),
    ]
}

generate_report(context)

