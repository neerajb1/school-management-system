from fpdf import FPDF

def generate_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in data:
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(filename)
