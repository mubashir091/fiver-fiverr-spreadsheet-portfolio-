import json
import os
import pandas as pd

from excel_template import create_excel_file
from pdf_template import create_pdf_report


def generate_project(config_path, input_path, output_dir):
    # Load project configuration
    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    # Read source spreadsheet
    data = pd.read_excel(input_path)

    # Prepare output folder
    os.makedirs(output_dir, exist_ok=True)

    project_name = config["project_slug"]

    # Generate Excel file
    excel_path = os.path.join(
        output_dir, f"{project_name}_cleaned.xlsx"
    )

    create_excel_file(data, excel_path)

    # Generate PDF report
    pdf_path = os.path.join(
        output_dir, f"{project_name}_report.pdf"
    )

    create_pdf_report(
        config["project_name"],
        config["description"],
        data,
        pdf_path
    )

    print("Project files generated successfully!")


if __name__ == "__main__":
    generate_project(
        "project_config.json",
        "input.xlsx",
        "output"
    )