import csv
import sys
from dataclasses import dataclass
from typing import List

VALID_STATUSES = {"active", "inactive", "pending"}


@dataclass
class ValidationIssue:
    row: int
    field: str
    message: str


def validate_record(row_number: int, record: dict) -> List[ValidationIssue]:
    issues = []

    if not record.get("product_code", "").strip():
        issues.append(
            ValidationIssue(row_number, "product_code", "Product code is required.")
        )

    try:
        quantity = int(record.get("quantity", ""))
        if quantity < 0:
            issues.append(
                ValidationIssue(row_number, "quantity", "Quantity cannot be negative.")
            )
    except ValueError:
        issues.append(
            ValidationIssue(row_number, "quantity", "Quantity must be an integer.")
        )

    try:
        price = float(record.get("price", ""))
        if price < 0:
            issues.append(
                ValidationIssue(row_number, "price", "Price cannot be negative.")
            )
    except ValueError:
        issues.append(
            ValidationIssue(row_number, "price", "Price must be numeric.")
        )

    status = record.get("status", "").strip().lower()
    if status not in VALID_STATUSES:
        issues.append(
            ValidationIssue(
                row_number,
                "status",
                f"Status must be one of: {', '.join(sorted(VALID_STATUSES))}.",
            )
        )

    return issues


def validate_csv(path: str) -> List[ValidationIssue]:
    issues = []

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row_number, record in enumerate(reader, start=2):
            issues.extend(validate_record(row_number, record))

    return issues


def main():
    if len(sys.argv) != 2:
        print("Usage: python validator.py <csv_file>")
        raise SystemExit(1)

    issues = validate_csv(sys.argv[1])

    if not issues:
        print("Validation passed: no issues found.")
        return

    print(f"Found {len(issues)} issue(s):")

    for issue in issues:
        print(f"Row {issue.row} | {issue.field}: {issue.message}")


if __name__ == "__main__":
    main()
