# from pdf2docx import Converter

# pdf_file = "input.pdf"
# docx_file = "output.docx"

# cv = Converter(pdf_file)
# cv.convert(docx_file, start=0, end=None)
# cv.close()

import fitz  # PyMuPDF
from docx import Document

doc = Document()
pdf = fitz.open("input.pdf")

for page in pdf:
    text = page.get_text()
    doc.add_paragraph(text)

doc.save("output.docx")
