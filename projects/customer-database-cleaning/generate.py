import os
import sys
import re
import pandas as pd


# ==========================================
# PROJECT PATHS
# ==========================================

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

TEMPLATE_DIR = os.path.join(ROOT_DIR, "template")
sys.path.insert(0, TEMPLATE_DIR)

from excel_template import create_excel_file
from pdf_template import create_pdf_report
from portfolio_showcase import create_portfolio_showcase


# ==========================================
# DATA CLEANING FUNCTIONS
# ==========================================

def clean_text(value):
    """Remove unnecessary spaces and standardize text."""

    if pd.isna(value):
        return ""

    return str(value).strip()


def parse_date(value):
    """Convert different date formats into a standard date."""

    if pd.isna(value) or str(value).strip() == "":
        return pd.NaT

    value = str(value).strip()

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%B %d, %Y",
        "%b %d, %Y"
    ]

    for date_format in formats:
        try:
            return pd.to_datetime(
                value,
                format=date_format,
                errors="raise"
            )
        except (ValueError, TypeError):
            continue

    return pd.NaT


def clean_customer_data(data):

    data = data.copy()

    issues = {
        index: [] for index in data.index
    }

    # --------------------------------------
    # 1. CHECK REQUIRED COLUMNS
    # --------------------------------------

    required_columns = [
        "Name",
        "Email",
        "City",
        "Date",
        "Phone"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # --------------------------------------
    # 2. STANDARDIZE TEXT
    # --------------------------------------

    for field in ["Name", "City"]:

        data[field] = (
            data[field]
            .apply(clean_text)
            .str.title()
        )

    data["Email"] = (
        data["Email"]
        .apply(clean_text)
        .str.lower()
    )

    # Keep phone numbers as text
    data["Phone"] = (
        data["Phone"]
        .apply(clean_text)
    )

    # --------------------------------------
    # 3. CHECK MISSING INFORMATION
    # --------------------------------------

    for field in ["Name", "Email", "City"]:

        missing = data[field].eq("")

        for index in data.index[missing]:
            issues[index].append(
                f"Missing {field}"
            )

    # --------------------------------------
    # 4. VALIDATE EMAIL ADDRESSES
    # --------------------------------------

    email_pattern = (
        r"^[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    invalid_emails = (
        data["Email"].ne("")
        & ~data["Email"].str.fullmatch(email_pattern)
    )

    for index in data.index[invalid_emails]:
        issues[index].append(
            "Invalid email format"
        )

    # --------------------------------------
    # 5. STANDARDIZE DATES
    # --------------------------------------

    original_dates = data["Date"].copy()

    data["Date"] = original_dates.apply(parse_date)

    missing_dates = (
        original_dates.isna()
        | original_dates.astype(str).str.strip().eq("")
    )

    invalid_dates = (
        ~missing_dates
        & data["Date"].isna()
    )

    for index in data.index[missing_dates]:
        issues[index].append("Missing Date")

    for index in data.index[invalid_dates]:
        issues[index].append("Invalid Date")

    # --------------------------------------
    # 6. CHECK DUPLICATE RECORDS
    # --------------------------------------

    duplicates = data.duplicated(
        keep="first"
    )

    for index in data.index[duplicates]:
        issues[index].append(
            "Duplicate record"
        )

    # --------------------------------------
    # 7. CREATE VALIDATION REPORT
    # --------------------------------------

    report_rows = []

    for index, row_issues in issues.items():

        if row_issues:

            report_rows.append({
                "Row Number": index + 2,
                "Customer Name": data.loc[index, "Name"],
                "Email": data.loc[index, "Email"],
                "City": data.loc[index, "City"],
                "Issues": "; ".join(row_issues)
            })

    validation_report = pd.DataFrame(
        report_rows,
        columns=[
            "Row Number",
            "Customer Name",
            "Email",
            "City",
            "Issues"
        ]
    )

    # --------------------------------------
    # 8. REMOVE EXACT DUPLICATES
    # --------------------------------------

    cleaned_data = (
        data.loc[~duplicates]
        .reset_index(drop=True)
    )

    # --------------------------------------
    # 9. GENERATE SUMMARY
    # --------------------------------------

    summary = {
        "Original records": len(data),
        "Duplicate records detected": int(duplicates.sum()),
        "Final records": len(cleaned_data),
        "Records flagged for review": len(validation_report),
        "Missing names": sum(
            "Missing Name" in item for item in issues.values()
        ),
        "Missing emails": sum(
            "Missing Email" in item for item in issues.values()
        ),
        "Missing cities": sum(
            "Missing City" in item for item in issues.values()
        ),
        "Invalid emails": int(invalid_emails.sum()),
        "Invalid dates": int(invalid_dates.sum())
    }

    return cleaned_data, validation_report, summary


# ==========================================
# PROJECT EXECUTION
# ==========================================

def main():

    print("\nCUSTOMER DATABASE CLEANING PROJECT")
    print("=" * 45)

    sample_dir = os.path.join(
        os.path.dirname(__file__),
        "sample_data"
    )

    input_file = os.path.join(
        sample_dir,
        "customers.csv"
    )

    output_dir = os.path.join(
        ROOT_DIR,
        "output",
        "Excel"
    )

    pdf_dir = os.path.join(
        ROOT_DIR,
        "output",
        "PDF"
    )

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    # --------------------------------------
    # READ ORIGINAL DATA
    # --------------------------------------

    print("\nReading original customer dataset...")

    data = pd.read_csv(
        input_file,
        dtype={"Phone": str}
    )

    print(f"Records imported: {len(data)}")

    # --------------------------------------
    # CLEAN AND VALIDATE
    # --------------------------------------

    print("\nCleaning and validating records...")

    cleaned_data, validation_report, summary = (
        clean_customer_data(data)
    )

    # --------------------------------------
    # GENERATE EXCEL WORKBOOK
    # --------------------------------------

    excel_path = os.path.join(
        output_dir,
        "customer_database_cleaned.xlsx"
    )

    create_excel_file(
    cleaned_data,
    excel_path,
    raw_data=data,
    validation_report=validation_report,
    summary=summary
)

    # --------------------------------------
    # GENERATE PDF REPORT
    # --------------------------------------

    pdf_path = os.path.join(
        pdf_dir,
        "customer_database_report.pdf"
    )

    create_pdf_report(
    "Customer Database Cleaning",
    "Professional customer data cleaning and quality assessment.",
    cleaned_data,
    pdf_path,
    summary=summary,
    validation_report=validation_report
)    # Generate Fiverr Portfolio Showcase
    showcase_path = os.path.join(
        pdf_dir,
        "customer_database_portfolio_showcase.pdf"
    )

    create_portfolio_showcase(
        summary,
        showcase_path
    )

    # --------------------------------------
    # SAVE VALIDATION REPORT
    # --------------------------------------

    validation_path = os.path.join(
        output_dir,
        "customer_database_validation.csv"
    )

    validation_report.to_csv(
        validation_path,
        index=False
    )

    # --------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------

    print("\n" + "=" * 45)
    print("DATA CLEANING SUMMARY")
    print("=" * 45)

    for label, value in summary.items():
        print(f"{label}: {value}")

    print("\nPROJECT OUTPUTS")
    print("=" * 45)

    print(f"Excel: {excel_path}")
    print(f"PDF: {pdf_path}")
    print(f"Validation: {validation_path}")

    print("\nCleaning process completed successfully!")


if __name__ == "__main__":
    main()