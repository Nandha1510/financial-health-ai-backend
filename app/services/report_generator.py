from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_pdf(filename, summary, recommendations):
    c = canvas.Canvas(filename, pagesize=A4)
    y = 800

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "SME Financial Health Report")
    y -= 40

    c.setFont("Helvetica", 11)
    for k, v in summary.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 18

    y -= 20
    c.drawString(50, y, "Recommendations:")
    y -= 20

    for r in recommendations:
        c.drawString(60, y, f"- {r}")
        y -= 15

    c.save()
    return filename
