from PIL import Image
import os

# مسیر پوشه‌ای که فایل‌ها در آن هستند
folder_path = "files"

# فرمت جدیدی که می‌خوایم تغییر بدیم (مثلاً "png" یا "jpeg")
new_format = "png"

# گرفتن همه فایل‌ها در پوشه
for filename in os.listdir(folder_path):
    # ساخت مسیر کامل فایل
    file_path = os.path.join(folder_path, filename)
    
    # فقط فایل‌های تصویری با پسوند مشخص رو پردازش می‌کنیم
    if filename.lower().endswith(("jpg", "jpeg", "bmp", "tiff", "gif", "png")):
        # باز کردن تصویر
        img = Image.open(file_path)
        
        # اسم فایل بدون پسوند
        base_name = os.path.splitext(filename)[0]
        
        # مسیر ذخیره فایل جدید
        new_file_path = os.path.join("new", f"{base_name}.{new_format}")
        
        # ذخیره تصویر با فرمت جدید
        img.save(new_file_path)
        print(f"{filename} -> {base_name}.{new_format}")
