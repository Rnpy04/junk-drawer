import cv2
import pytesseract
from PIL import Image
from pathlib import Path
import re
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import numpy as np

# ---------- Paths ----------
pytesseract.pytesseract.tesseract_cmd = ""
POPPLER_PATH = ""

pdf_input = "input.pdf"
image_folder = Path("images")
processed_folder = Path("processed")
image_folder.mkdir(exist_ok=True)
processed_folder.mkdir(exist_ok=True)

# ---------- TEXT CLEANER ----------
def clean_text(text):
    text = re.sub(r"[^آ-ی0-9\n\s\.\،\:\؛\؟\!\(\)\[\]]", "", text)
    text = text.replace("ي", "ی").replace("ك", "ک")
    lines = [line for line in text.splitlines() if len(line.strip()) > 6]
    return "\n".join(lines)

# ---------- PDF TO IMAGES ----------
pages = convert_from_path(
    pdf_input,
    dpi=300,
    poppler_path=POPPLER_PATH
)

for i, page in enumerate(pages, 1):
    page.save(image_folder / f"page_{i:03}.png", "PNG")

# ---------- OCR PIPELINE ----------
book_text = ""

for img_path in sorted(image_folder.glob("page_*.png")):
    # 1️⃣ Load grayscale
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)

    # 2️⃣ Denoising
    img = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)

    # 3️⃣ CLAHE (contrast enhancement)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    img = clahe.apply(img)

    # 4️⃣ Adaptive Threshold
    img = cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    # 5️⃣ Morphological Closing (optional for broken text)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # 6️⃣ Save processed image
    processed_path = processed_folder / img_path.name
    cv2.imwrite(str(processed_path), img)

    # 7️⃣ OCR
    pil_img = Image.open(processed_path)
    text = pytesseract.image_to_string(pil_img, lang="fas")
    text = clean_text(text)
    book_text += text + "\n\n"

# ---------- SAVE TXT ----------
with open("book.txt", "w", encoding="utf-8") as f:
    f.write(book_text)

# # ---------- TXT TO FINAL PDF ----------
# pdf = canvas.Canvas("Final_Book.pdf", pagesize=A4)
# width, height = A4
# y = height - 50
# line_height = 16

# for line in book_text.split("\n"):
#     if y < 50:
#         pdf.showPage()
#         y = height - 50
#     pdf.drawRightString(width - 50, y, line)
#     y -= line_height

# pdf.save()

print("Done")
