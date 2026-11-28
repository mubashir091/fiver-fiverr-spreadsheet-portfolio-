
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


NAVY = colors.HexColor("#1F4E78")
BLUE = colors.HexColor("#D9EAF7")
LIGHT = colors.HexColor("#F2F6FA")
DARK = colors.HexColor("#243447")
GREY = colors.HexColor("#64748B")
WHITE = colors.white


def safe_text(value):
    """Convert values into safe text for PDF paragraphs."""
    if value is None:
        return ""
    return escape(str(value))


def make_table(data, widths=None, font_size=8):
    """Create a consistently styled professional table."""
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("LEADING", (0, 0), (-1, -1), font_size + 2),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT])
    ]))

    return table


def add_page_number(canvas, document):
    """Add a consistent header and footer to every page."""
    canvas.saveState()

    page_width, page_height = landscape(A4)

    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, page_height - 14 * mm,
                page_width - 18 * mm, page_height - 14 * mm)

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(18 * mm, 9 * mm, "CUSTOMER DATABASE CLEANING REPORT")
    canvas.drawRightString(
        page_width - 18 * mm, 9 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()


def create_pdf_report(
    title,
    description,
    data,
    output_path,
    summary=None,
    validation_report=None
):
    """Generate a professional customer data cleaning PDF report."""

    summary = summary or {}
    validation_report = validation_report

    document = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=17 * mm
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        textColor=DARK
    ))

    styles.add(ParagraphStyle(
        name="SmallCell",
        parent=styles["BodyText"],
        fontSize=7,
        leading=9,
        alignment=TA_LEFT
    ))

    elements = []

    # 1. Report introduction
    elements.append(Paragraph(safe_text(title), styles["ReportTitle"]))
    elements.append(Paragraph(safe_text(description), styles["ReportBody"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "Project Overview",
        styles["SectionHeading"]
    ))

    elements.append(Paragraph(
        "This report documents the customer database cleaning process. "
        "It presents the processing statistics, data-quality findings, "
        "and final cleaned records.",
        styles["ReportBody"]
    ))

    # 2. Summary statistics
    elements.append(Paragraph(
        "Data Cleaning Summary",
        styles["SectionHeading"]
    ))

    if summary:
        summary_data = [
            [
                Paragraph("<b>Metric</b>", styles["SmallCell"]),
                Paragraph("<b>Result</b>", styles["SmallCell"])
            ]
        ]

        for key, value in summary.items():
            summary_data.append([
                Paragraph(safe_text(key), styles["SmallCell"]),
                Paragraph(safe_text(value), styles["SmallCell"])
            ])

        elements.append(make_table(
            summary_data,
            widths=[95 * mm, 65 * mm],
            font_size=8
        ))
    else:
        elements.append(Paragraph(
            "No summary statistics were supplied.",
            styles["ReportBody"]
        ))

    # 3. Validation findings
    elements.append(Paragraph(
        "Validation Report",
        styles["SectionHeading"]
    ))

    if validation_report is not None and not validation_report.empty:
        validation_data = [
            [
                Paragraph(f"<b>{safe_text(col)}</b>", styles["SmallCell"])
                for col in validation_report.columns
            ]
        ]

        for row in validation_report.astype(str).values.tolist():
            validation_data.append([
                Paragraph(safe_text(value), styles["SmallCell"])
                for value in row
            ])

        elements.append(make_table(
            validation_data,
            font_size=7
        ))
    else:
        elements.append(Paragraph(
            "No records were flagged for review.",
            styles["ReportBody"]
        ))

    # 4. Cleaned database
    elements.append(PageBreak())

    elements.append(Paragraph(
        "Cleaned Customer Database",
        styles["SectionHeading"]
    ))

    elements.append(Paragraph(
        f"Final dataset contains {len(data)} cleaned records.",
        styles["ReportBody"]
    ))

    elements.append(Spacer(1, 8))

    if not data.empty:
        table_data = [
            [
                Paragraph(f"<b>{safe_text(col)}</b>", styles["SmallCell"])
                for col in data.columns
            ]
        ]

        for row in data.astype(str).values.tolist():
            table_data.append([
                Paragraph(safe_text(value), styles["SmallCell"])
                for value in row
            ])

        elements.append(make_table(
            table_data,
            font_size=7
        ))
    else:
        elements.append(Paragraph(
            "No cleaned records are available.",
            styles["ReportBody"]
        ))

    # 5. Final note
    elements.append(Spacer(1, 14))
    elements.append(Paragraph(
        "Quality Note",
        styles["SectionHeading"]
    ))
    elements.append(Paragraph(
        "Records identified by the validation process should be reviewed "
        "before the database is used for business operations. Automated "
        "cleaning does not guarantee that every original customer detail "
        "is accurate.",
        styles["ReportBody"]
    ))

    document.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return output_path
