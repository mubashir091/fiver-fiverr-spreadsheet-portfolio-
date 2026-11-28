# Customer Database Cleaning & Data Quality Project

## Project Overview

This portfolio project demonstrates how to transform an inconsistent customer database into a clean, organized, and professionally formatted dataset.

The project simulates a common business task: a company has collected customer information from different sources, and the data contains inconsistent formatting, missing information, invalid entries, and duplicate records.

The objective is to improve data quality while preserving the original information for review.

> **Portfolio demonstration:** All customer records and contact details in this project are fictional. This is a self-created sample project, not a real client engagement.

---

## Business Scenario

Imagine a small business has a customer database containing names, email addresses, cities, dates, and phone numbers.

Over time, information has been entered by different people using different formats.

This creates problems such as:

- Duplicate customer records.
- Inconsistent capitalization.
- Extra spaces in names and email addresses.
- Invalid email formats.
- Missing customer information.
- Inconsistent date formats.
- Inconsistent city names.

These issues make the database difficult to manage, search, and analyze.

This project demonstrates a structured cleaning and validation process to address these problems.

---

## Project Objectives

1. Organize the original customer data.
2. Standardize names, email addresses, and city names.
3. Normalize dates into a consistent format.
4. Identify duplicate records.
5. Detect missing and invalid information.
6. Preserve phone numbers as text.
7. Create a professional Excel workbook.
8. Prepare a data quality report.
9. Document all cleaning decisions clearly.

---

## Dataset Information

The sample dataset contains fictional customer information.

| Field | Description |
|---|---|
| Name | Customer's full name |
| Email | Customer's email address |
| City | Customer's city |
| Date | Associated record date |
| Phone | Fictional phone number |

The dataset intentionally includes data-quality issues so that the cleaning process can be demonstrated.

---

## Data Cleaning Process

### 1. Standardizing Text

- Removed unnecessary leading and trailing spaces.
- Standardized capitalization in names and cities.
- Converted email addresses to lowercase.
- Removed unnecessary spaces from email addresses.

### 2. Date Standardization

- Identified dates entered in different formats.
- Converted recognizable dates into a consistent date format.
- Flagged missing or invalid dates for review.

### 3. Duplicate Detection

- Identified exact duplicate records.
- Retained the first occurrence of an exact duplicate.
- Flagged duplicate entries in the validation report.

Records are not merged based on similar names or email addresses alone.

### 4. Missing Information

- Identified missing names, emails, and cities.
- Flagged missing information for review.
- Did not invent or guess missing customer details.

### 5. Email Validation

- Checked basic email formatting.
- Flagged entries that do not follow a recognizable email pattern.
- Did not claim to verify whether an email inbox actually exists.

### 6. Phone Number Handling

- Preserved phone numbers as text.
- Avoided treating phone numbers as numerical values.
- This helps retain leading zeros and formatting.

---

## Expected Deliverables

The completed project will include:

### Excel Workbook

A professionally formatted workbook containing:

- **Raw Data:** Original imported records.
- **Cleaned Data:** Standardized customer information.
- **Validation Report:** Missing, invalid, and duplicate entries.
- **Summary:** Overview of data quality findings.

### PDF Report

A readable report explaining:

- Project objectives.
- Original data issues.
- Cleaning methods.
- Validation results.
- Final data quality observations.

### Supporting Files

- Original sample CSV dataset.
- Python cleaning and generation script.
- Reproducible project instructions.

---

## Tools and Technologies

- Microsoft Excel
- Python
- Pandas
- OpenPyXL
- ReportLab
- CSV data processing

---

## Quality and Accuracy Principles

This project follows several important data-handling principles:

- Original data is preserved separately.
- Cleaning decisions are documented.
- Missing information is flagged rather than invented.
- Invalid records are identified for review.
- Duplicate detection follows a clearly defined rule.
- Phone numbers are handled as text.
- Validation results are transparent.

---

## Project Workflow

1. Import the original customer dataset.
2. Inspect the data for inconsistencies.
3. Standardize text fields.
4. Normalize recognizable dates.
5. Detect duplicate records.
6. Validate required information.
7. Generate the cleaned dataset.
8. Create the Excel workbook.
9. Generate the PDF report.
10. Review the final outputs.

---

## Intended Applications

This type of data-cleaning workflow can be useful for:

- Small businesses.
- Customer contact databases.
- Sales records.
- Administrative spreadsheets.
- Lead lists.
- General data organization.

---

## About This Portfolio Sample

This project was created to demonstrate practical spreadsheet organization, data cleaning, validation, and reporting skills.

It is intended as a sample of the type of structured data-management work that can be delivered to clients.
