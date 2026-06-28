from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def generate_pdf(name, subject, score, total, accuracy, grade, wrong_topics):
    filename = f"{name}_Quiz_Report.pdf"

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>AI Learning Companion</b>", styles["Title"]))
    story.append(Paragraph("<b>Quiz Performance Report</b>", styles["Heading2"]))

    story.append(Paragraph(f"Student Name: {name}", styles["Normal"]))
    story.append(Paragraph(f"Subject: {subject}", styles["Normal"]))
    story.append(Paragraph(f"Score: {score}/{total}", styles["Normal"]))
    story.append(Paragraph(f"Accuracy: {accuracy:.2f}%", styles["Normal"]))
    story.append(Paragraph(f"Grade: {grade}", styles["Normal"]))

    story.append(Paragraph("<br/><b>Topics To Review</b>", styles["Heading2"]))

    if wrong_topics:
        for topic in set(wrong_topics):
            story.append(Paragraph(f"• {topic}", styles["Normal"]))
    else:
        story.append(Paragraph("Excellent! No weak topics.", styles["Normal"]))

    story.append(Paragraph("<br/>Thank you for using AI Learning Companion.", styles["Normal"]))

    doc.build(story)

    return filename