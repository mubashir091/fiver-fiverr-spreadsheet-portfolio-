import pandas as pd

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side
)

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo


# ==========================================
# PROFESSIONAL EXCEL FORMATTING
# ==========================================

HEADER_COLOR = "1F4E78"
WHITE = "FFFFFF"
LIGHT_BLUE = "D9EAF7"
DARK_TEXT = "243447"


def format_worksheet(ws):

    # Header formatting
    for cell in ws[1]:

        cell.font = Font(
            bold=True,
            color=WHITE,
            size=11
        )

        cell.fill = PatternFill(
            start_color=HEADER_COLOR,
            end_color=HEADER_COLOR,
            fill_type="solid"
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    ws.row_dimensions[1].height = 25

    # Column widths
    for column_cells in ws.columns:

        max_length = max(
            len(str(cell.value or ""))
            for cell in column_cells
        )

        column_letter = get_column_letter(
            column_cells[0].column
        )

        ws.column_dimensions[column_letter].width = min(
            max_length + 4,
            40
        )

    # Navigation
    ws.freeze_panes = "A2"

    # Filter
    if ws.max_row > 1:
        ws.auto_filter.ref = ws.dimensions

    # General cell alignment
    for row in ws.iter_rows(min_row=2):

        for cell in row:
            cell.alignment = Alignment(
                vertical="center"
            )


def add_excel_table(ws, table_name):

    if ws.max_row < 2 or ws.max_column < 1:
        return

    table = Table(
        displayName=table_name,
        ref=ws.dimensions
    )

    style = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )

    table.tableStyleInfo = style

    ws.add_table(table)


def write_dataframe(writer, dataframe, sheet_name, table_name):

    dataframe = pd.DataFrame(dataframe).copy()

    dataframe.to_excel(
        writer,
        index=False,
        sheet_name=sheet_name
    )

    ws = writer.sheets[sheet_name]

    format_worksheet(ws)

    add_excel_table(ws, table_name)

    # Format dates consistently
    for column in ws.columns:

        header = str(column[0].value).strip().lower()

        if header == "date":

            for cell in column[1:]:
                cell.number_format = "dd-mmm-yyyy"

    return ws


# ==========================================
# SUMMARY WORKSHEET
# ==========================================

def create_summary_sheet(writer, summary):

    ws = writer.book.create_sheet("Summary")

    ws.append([
        "CUSTOMER DATABASE CLEANING REPORT"
    ])

    ws.merge_cells("A1:B1")

    title = ws["A1"]

    title.font = Font(
        bold=True,
        color=WHITE,
        size=15
    )

    title.fill = PatternFill(
        start_color=HEADER_COLOR,
        end_color=HEADER_COLOR,
        fill_type="solid"
    )

    title.alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    ws.row_dimensions[1].height = 35

    ws.append(["Metric", "Result"])

    for cell in ws[2]:

        cell.font = Font(
            bold=True,
            color=WHITE
        )

        cell.fill = PatternFill(
            start_color=HEADER_COLOR,
            end_color=HEADER_COLOR,
            fill_type="solid"
        )

    for label, value in summary.items():

        ws.append([
            label,
            value
        ])

    # Highlight metric rows
    for row in range(3, ws.max_row + 1):

        ws.cell(row, 1).font = Font(
            bold=True,
            color=DARK_TEXT
        )

        ws.cell(row, 2).alignment = Alignment(
            horizontal="center"
        )

        if row % 2 == 0:

            for cell in ws[row]:

                cell.fill = PatternFill(
                    start_color=LIGHT_BLUE,
                    end_color=LIGHT_BLUE,
                    fill_type="solid"
                )

    ws.column_dimensions["A"].width = 35
    ws.column_dimensions["B"].width = 22

    ws.freeze_panes = "A3"


# ==========================================
# MAIN WORKBOOK GENERATOR
# ==========================================

def create_excel_file(
    data,
    output_path,
    raw_data=None,
    validation_report=None,
    summary=None
):

    cleaned_data = pd.DataFrame(data)

    raw_data = (
        pd.DataFrame(raw_data)
        if raw_data is not None
        else cleaned_data.copy()
    )

    validation_report = (
        pd.DataFrame(validation_report)
        if validation_report is not None
        else pd.DataFrame(
            columns=[
                "Row Number",
                "Customer Name",
                "Email",
                "City",
                "Issues"
            ]
        )
    )

    summary = summary or {}

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        # 1. Original records
        write_dataframe(
            writer,
            raw_data,
            "Raw Data",
            "RawCustomerData"
        )

        # 2. Cleaned records
        write_dataframe(
            writer,
            cleaned_data,
            "Cleaned Data",
            "CleanedCustomerData"
        )

        # 3. Validation results
        write_dataframe(
            writer,
            validation_report,
            "Validation Report",
            "ValidationResults"
        )

        # 4. Summary
        create_summary_sheet(
            writer,
            summary
        )

        # Set active sheet
        writer.book.active = 3

    return output_path