from PyPDF2 import PdfReader, PdfWriter

input_pdf = "input.pdf"
output_pdf = "output.pdf"

start_page = 60
end_page = 129

reader = PdfReader(input_pdf)

if reader.is_encrypted:
    result = reader.decrypt("")
    if result == 0:
        raise Exception("PDF is encrypted and needs a password")

writer = PdfWriter()

total_pages = len(reader.pages)

if start_page < 1 or end_page > total_pages:
    raise ValueError("Page range is out of bounds")

for i in range(start_page - 1, end_page):
    writer.add_page(reader.pages[i])

with open(output_pdf, "wb") as f:
    writer.write(f)

print("PDF cut successfully.")
