from PIL import Image
import os

# مسیر پوشه‌ای که تصاویر داخلش هستن
image_folder = "images"
# نام فایل خروجی PDF
output_pdf = "output.pdf"

# گرفتن لیست تمام فایل‌های تصویری در پوشه
image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]

# مرتب کردن تصاویر بر اساس نام (اختیاری، اگر میخوای ترتیب خاصی باشه)
image_files.sort()

# باز کردن تصاویر و تبدیل به RGB (چون PDF فقط RGB رو پشتیبانی می‌کنه)
images = [Image.open(os.path.join(image_folder, f)).convert('RGB') for f in image_files]

# اولین تصویر رو جدا می‌کنیم و بقیه رو بهش اضافه می‌کنیم
if images:
    first_image = images[0]
    rest_images = images[1:]
    first_image.save(output_pdf, save_all=True, append_images=rest_images)
    print(f" done : {output_pdf}")
else:
    print("هیچ تصویری پیدا نشد!")
