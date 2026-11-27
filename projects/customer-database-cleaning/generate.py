
import os
import sys
import re
import pandas as pd

# Locate reusable templates
ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

TEMPLATE_DIR = os.path.join(ROOT_DIR, "template")
sys.path.insert(0, TEMPLATE_DIR)

from excel_template import create_excel_file
from pdf_template import create_pdf_report


def clean_customer_data(data):

    data = data.copy()
    issues = {index: [] for index in data.index}

    # Check required fields
    required_fields = ["Name", "Email", "City"]

    for field in required_fields:
        if field in data.columns:
            missing = (
                data[field].isna()
                | data[field].astype("string").str.strip().eq("")
            )

            for index in data.index[missing]:
                issues[index].append(f"Missing {field}")

    # Standardize text fields
    for field in ["Name", "City"]:
        if field in data.columns:
            data[field] = (
                data[field].fillna("").astype(str)
                .str.strip().str.title()
            )

    if "Email" in data.columns:
        data["Email"] = (
            data["Email"].fillna("").astype(str)
            .str.strip().str.lower()
        )

        # Validate email formats
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        invalid_email = (
            data["Email"].ne("")
            & ~data["Email"].str.fullmatch(email_pattern)
        )

        for index in data.index[invalid_email]:
            issues[index].append("Invalid email format")

    # Validate and standardize dates
    if "Date" in data.columns:
        original_dates = data["Date"].copy()

        date_text = (
            original_dates.fillna("").astype(str).str.strip()
        )

        parsed_dates = pd.to_datetime(
            original_dates, errors="coerce"
        )

        missing_dates = date_text.eq("")
        invalid_dates = ~missing_dates & parsed_dates.isna()

        for index in data.index[missing_dates]:
            issues[index].append("Missing Date")

        for index in data.index[invalid_dates]:
            issues[index].append("Invalid Date")

        data["Date"] = parsed_dates

    # Detect duplicate records after standardization
    duplicates = data.duplicated(keep="first")

    for index in data.index[duplicates]:
        issues[index].append("Duplicate record")

    # Prepare validation report
    report_rows = []

    for index, row_issues in issues.items():
        if row_issues:
            report_rows.append({
                "Row Number": index + 2,
                "Customer Name": data.loc[index].get("Name", ""),
                "Email": data.loc[index].get("Email", ""),
                "Issues": "; ".join(row_issues)
            })

    validation_report = pd.DataFrame(
        report_rows,
        columns=[
            "Row Number",
            "Customer Name",
            "Email",
            "Issues"
        ]
    )

    # Remove duplicates from cleaned output
    cleaned_data = data.loc[~duplicates].copy()

    summary = {
        "Original records": len(data),
        "Duplicates removed": int(duplicates.sum()),
        "Final records": len(cleaned_data),
        "Records flagged for review": len(validation_report)
    }

    return cleaned_data, validation_report, summary


def main():

    sample_dir = os.path.join(
        os.path.dirname(__file__), "sample_data"
    )

    input_file = os.path.join(
        sample_dir, "customers.csv"
    )

    output_dir = os.path.join(
        ROOT_DIR, "output", "Excel"
    )

    pdf_dir = os.path.join(
        ROOT_DIR, "output", "PDF"
    )

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    # Read source data
    data = pd.read_csv(
        input_file,
        dtype={"Phone": str}
    )

    # Clean and validate
    cleaned_data, validation_report, summary = (
        clean_customer_data(data)
    )

    # Generate Excel workbook
    excel_path = os.path.join(
        output_dir,
        "customer_database_cleaned.xlsx"
    )

    create_excel_file(cleaned_data, excel_path)

    # Generate PDF report
    pdf_path = os.path.join(
        pdf_dir,
        "customer_database_report.pdf"
    )

    create_pdf_report(
        "Customer Database Cleaning",
        "Demonstration of customer data cleaning and organization.",
        cleaned_data,
        pdf_path
    )

    # Save validation report
    validation_path = os.path.join(
        output_dir,
        "customer_database_validation.csv"
    )

    validation_report.to_csv(
        validation_path,
        index=False
    )

    # Display summary
    print("\nCUSTOMER DATA CLEANING SUMMARY")

    for label, value in summary.items():
        print(f"{label}: {value}")

    print("\nAll project files generated successfully!")


if __name__ == "__main__":
    main()
