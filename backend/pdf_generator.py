from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_pdf(tester_summary, severity_summary, product_summary):

    file_path = "daily_productivity_report.pdf"

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("QA Daily Productivity Report", styles['Title']))
    elements.append(Spacer(1,20))

    # Tester Table
    tester_data = [["Tester", "Total Bugs"]]
    tester_data += tester_summary.values.tolist()

    tester_table = Table(tester_data)
    tester_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.grey),
        ("GRID",(0,0),(-1,-1),1,colors.black)
    ]))

    elements.append(Paragraph("Tester Productivity", styles['Heading2']))
    elements.append(tester_table)
    elements.append(Spacer(1,20))

    # Severity Table
    severity_data = [["Severity","Count"]]
    severity_data += severity_summary.values.tolist()

    severity_table = Table(severity_data)
    severity_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.grey),
        ("GRID",(0,0),(-1,-1),1,colors.black)
    ]))

    elements.append(Paragraph("Severity Summary", styles['Heading2']))
    elements.append(severity_table)
    elements.append(Spacer(1,20))

    # Product Table
    product_data = [["Product","Count"]]
    product_data += product_summary.values.tolist()

    product_table = Table(product_data)
    product_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.grey),
        ("GRID",(0,0),(-1,-1),1,colors.black)
    ]))

    elements.append(Paragraph("Product Summary", styles['Heading2']))
    elements.append(product_table)

    pdf = SimpleDocTemplate(file_path, pagesize=A4)
    pdf.build(elements)

    return file_path
