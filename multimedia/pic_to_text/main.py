import cv2
import pytesseract
from PIL import Image
from pathlib import Path
import re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

image_folder = Path("images")
processed_folder = Path("processed")
processed_folder.mkdir(exist_ok=True)

def clean_text(text):
    text = re.sub(r"[^آ-ی0-9\n\s\.\،\:\؛\؟\!\(\)\[\]]", "", text)
    text = text.replace("ي", "ی").replace("ك", "ک")

    lines = []
    for line in text.splitlines():
        if len(line.strip()) > 6:
            lines.append(line)

    return "\n".join(lines)


book_text = ""

for img_path in sorted(image_folder.glob("image_*.png")):
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)

    img = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    img = clahe.apply(img)

    img = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    processed_path = processed_folder / img_path.name
    cv2.imwrite(str(processed_path), img)

    pil_img = Image.open(processed_path)
    text = pytesseract.image_to_string(pil_img, lang="fas")

    text = clean_text(text)
    book_text += text + "\n\n"


with open("book.txt", "w", encoding="utf-8") as f:
    f.write(book_text)


pdf = canvas.Canvas("Final_Book.pdf", pagesize=A4)
width, height = A4
x = 50
y = height - 50
line_height = 16

for line in book_text.split("\n"):
    if y < 50:
        pdf.showPage()
        y = height - 50
    pdf.drawRightString(width - 50, y, line)
    y -= line_height

pdf.save()

print("Pipeline finished. book.txt and Final_Book.pdf created.")
