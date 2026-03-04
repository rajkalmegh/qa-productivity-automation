
import pandas as pd

def generate_report(tester_summary, severity_summary, product_summary):

    report_file = "daily_productivity_report.xlsx"

    with pd.ExcelWriter(report_file) as writer:

        tester_summary.to_excel(
            writer,
            sheet_name="Tester Productivity",
            index=False
        )

        severity_summary.to_excel(
            writer,
            sheet_name="Severity Summary",
            index=False
        )

        product_summary.to_excel(
            writer,
            sheet_name="Product Summary",
            index=False
        )

    return report_file
  
