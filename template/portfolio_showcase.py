
import os
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
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


# ==========================================
# DESIGN COLORS
# ==========================================

NAVY = colors.HexColor("#1F4E78")
BLUE = colors.HexColor("#D9EAF7")
LIGHT = colors.HexColor("#F2F6FA")
DARK = colors.HexColor("#243447")
GREY = colors.HexColor("#64748B")
WHITE = colors.white


def safe(value):
    """Escape text before inserting it into PDF paragraphs."""
    return escape(str(value if value is not None else ""))


# ==========================================
# PORTFOLIO SHOWCASE GENERATOR
# ==========================================

def create_portfolio_showcase(summary, output_path):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    # --------------------------------------
    # CUSTOM TEXT STYLES
    # --------------------------------------

    styles.add(ParagraphStyle(
        name="MainTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=27,
        leading=33,
        textColor=NAVY,
        alignment=1,
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name="Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=9
    ))

    styles.add(ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=16,
        textColor=DARK
    ))

    styles.add(ParagraphStyle(
        name="SmallCustom",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
        textColor=DARK
    ))

    styles.add(ParagraphStyle(
        name="Subtitle",
        parent=styles["BodyCustom"],
        alignment=1,
        textColor=GREY,
        fontSize=11
    ))

    styles.add(ParagraphStyle(
        name="CoverText",
        parent=styles["BodyCustom"],
        alignment=1,
        fontSize=12,
        leading=19
    ))

    elements = []

    # ======================================
    # PAGE 1: COVER
    # ======================================

    elements.append(Spacer(1, 35 * mm))

    elements.append(Paragraph(
        "CUSTOMER DATABASE<br/>CLEANING",
        styles["MainTitle"]
    ))

    elements.append(Paragraph(
        "DATA CLEANING &amp; SPREADSHEET MANAGEMENT",
        styles["Subtitle"]
    ))

    elements.append(Spacer(1, 15 * mm))

    elements.append(Paragraph(
        "A sample project demonstrating how inconsistent "
        "customer information can be organized, standardized, "
        "validated and prepared for business use.",
        styles["CoverText"]
    ))

    elements.append(Spacer(1, 25 * mm))

    cover_box = Table(
        [[Paragraph(
            "<b>PROJECT PORTFOLIO SAMPLE</b><br/>"
            "Excel Workbook | PDF Report | Data Validation",
            styles["BodyCustom"]
        )]],
        colWidths=[155 * mm]
    )

    cover_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLUE),
        ("BOX", (0, 0), (-1, -1), 1, NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18)
    ]))

    elements.append(cover_box)

    elements.append(PageBreak())

    # ======================================
    # PAGE 2: PROJECT OVERVIEW
    # ======================================

    elements.append(Paragraph(
        "Project Overview",
        styles["Section"]
    ))

    elements.append(Paragraph(
        "This sample demonstrates a structured customer database "
        "cleaning workflow. The dataset contains deliberately "
        "introduced formatting inconsistencies, missing values, "
        "invalid entries and duplicate records.",
        styles["BodyCustom"]
    ))

    elements.append(Paragraph(
        "Key Services Demonstrated",
        styles["Section"]
    ))

    services = [
        "Customer data cleaning and formatting",
        "Removal of exact duplicate records",
        "Email format validation",
        "Date standardization",
        "Identification of missing information",
        "Data quality reporting"
    ]

    for service in services:
        elements.append(Paragraph(
            "• " + safe(service),
            styles["BodyCustom"]
        ))

        elements.append(Spacer(1, 4))

    # ======================================
    # PROJECT STATISTICS
    # ======================================

    elements.append(Paragraph(
        "Project Statistics",
        styles["Section"]
    ))

    metrics = [
        ["Metric", "Result"],
        [
            "Original Records",
            safe(summary.get("Original records", 0))
        ],
        [
            "Duplicates Detected",
            safe(summary.get("Duplicate records detected", 0))
        ],
        [
            "Final Records",
            safe(summary.get("Final records", 0))
        ],
        [
            "Records Flagged for Review",
            safe(summary.get("Records flagged for review", 0))
        ]
    ]

    table = Table(
        metrics,
        colWidths=[95 * mm, 55 * mm]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9)
    ]))

    elements.append(table)

    elements.append(PageBreak())

    # ======================================
    # PAGE 3: BEFORE AND AFTER
    # ======================================

    elements.append(Paragraph(
        "Before and After Cleaning",
        styles["Section"]
    ))

    elements.append(Paragraph(
        "Examples of the standardization demonstrated in this project:",
        styles["BodyCustom"]
    ))

    comparison = [
        ["Field", "Before", "After"],
        ["Name", " JOHN smith ", "John Smith"],
        ["Email", "JOHN@EXAMPLE.COM", "john@example.com"],
        ["City", " lahore ", "Lahore"],
        ["Date", "05/01/2026", "05-Jan-2026"]
    ]

    comparison_table = Table(
        comparison,
        colWidths=[35 * mm, 60 * mm, 60 * mm]
    )

    comparison_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#CBD5E1")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))

    elements.append(Spacer(1, 8))
    elements.append(comparison_table)

    # ======================================
    # PROJECT DELIVERABLES
    # ======================================

    elements.append(Paragraph(
        "Project Deliverables",
        styles["Section"]
    ))

    deliverables = [
        "Excel workbook with Raw Data, Cleaned Data, "
        "Validation Report and Summary sheets.",
        "PDF report presenting cleaning statistics "
        "and validation findings.",
        "CSV file containing records flagged for review."
    ]

    for item in deliverables:
        elements.append(Paragraph(
            "• " + safe(item),
            styles["BodyCustom"]
        ))

        elements.append(Spacer(1, 6))

    # ======================================
    # IMPORTANT NOTE
    # ======================================

    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        "Important Note",
        styles["Section"]
    ))

    elements.append(Paragraph(
        "This is a demonstration project using fictional sample "
        "customer data. The examples illustrate the workflow and "
        "do not represent a real client engagement.",
        styles["SmallCustom"]
    ))

    # ======================================
    # GENERATE PDF
    # ======================================

    doc.build(elements)

    return output_path
