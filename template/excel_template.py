import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


def create_excel_file(data, output_path, sheet_name="Cleaned Data"):
    """
    Create a professionally formatted Excel workbook.
    """

    df = pd.DataFrame(data)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)

        worksheet = writer.sheets[sheet_name]

        # Format header row
        for cell in worksheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(
                start_color="1F4E78",
                end_color="1F4E78",
                fill_type="solid"
            )
            cell.alignment = Alignment(horizontal="center")

        # Adjust column widths
        for column_cells in worksheet.columns:
            max_length = max(
                len(str(cell.value or "")) for cell in column_cells
            )
            column_letter = get_column_letter(column_cells[0].column)
            worksheet.column_dimensions[column_letter].width = min(
                max_length + 3, 35
            )

        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

    return output_path