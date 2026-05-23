import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# Create CSV file
def generate_csv_report(data, filename="seo_report.csv"):
    rows = []

    for key, value in data.items():
        rows.append({
            "Metric": key,
            "Value": str(value)
        })

    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)

    return filename


# Create PDF file
def generate_pdf_report(data, filename="seo_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("SEO Analysis Report", styles["Title"]))
    story.append(Spacer(1, 12))

    for key, value in data.items():
        line = f"<b>{key}</b>: {value}"
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 8))

    doc.build(story)

    return filename
