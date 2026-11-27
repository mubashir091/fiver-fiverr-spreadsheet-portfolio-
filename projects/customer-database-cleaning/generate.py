import os
import sys
import pandas as pd

# Locate the reusable template folder
ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

TEMPLATE_DIR = os.path.join(ROOT_DIR, "template")
sys.path.insert(0, TEMPLATE_DIR)

from excel_template import create_excel_file
from pdf_template import create_pdf_report


def clean_customer_data(data):
    # Remove duplicate records
    data = data.drop_duplicates()

    # Standardize text fields
    if "Name" in data.columns:
        data["Name"] = data["Name"].astype(str).str.strip().str.title()

    if "Email" in data.columns:
        data["Email"] = data["Email"].astype(str).str.strip().str.lower()

    if "City" in data.columns:
        data["City"] = data["City"].astype(str).str.strip().str.title()

    # Standardize dates
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(
            data["Date"], errors="coerce"
        )

    return data


def main():
    sample_dir = os.path.join(
        os.path.dirname(__file__), "sample_data"
    )

    input_file = os.path.join(sample_dir, "customers.xlsx")

    output_dir = os.path.join(
        ROOT_DIR, "output", "Excel"
    )

    os.makedirs(output_dir, exist_ok=True)

    data = pd.read_excel(input_file)
    cleaned_data = clean_customer_data(data)

    excel_path = os.path.join(
        output_dir, "customer_database_cleaned.xlsx"
    )

    pdf_path = os.path.join(
        ROOT_DIR, "output", "PDF",
        "customer_database_report.pdf"
    )

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    create_excel_file(cleaned_data, excel_path)

    create_pdf_report(
        "Customer Database Cleaning",
        "Demonstration of customer data cleaning and organization.",
        cleaned_data,
        pdf_path
    )

    print("Customer database project completed!")


if __name__ == "__main__":
    main()