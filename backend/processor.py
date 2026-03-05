import pandas as pd

def process_data(df):

    # Tester productivity
    tester_summary = df.groupby("Name").size().reset_index(name="Total Bugs")

    # Severity summary
    severity_summary = df.groupby("Severity").size().reset_index(name="Count")

    # Product summary
    product_summary = df.groupby("Product").size().reset_index(name="Count")

    return tester_summary, severity_summary, product_summary
