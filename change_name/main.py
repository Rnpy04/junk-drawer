import os

# مسیر پوشه
folder = "files"

# الگوی اسم جدید
new_name_pattern = "image"

# گرفتن لیست تمام فایل‌ها
files = os.listdir(folder)

# مرتب کردن فایل‌ها بر اساس نام (اختیاری)
files.sort()

# تغییر نام فایل‌ها
for i, filename in enumerate(files, start=1):
    # گرفتن پسوند فایل
    ext = os.path.splitext(filename)[1]  # .jpg, .png, ...
    # اسم جدید
    new_name = f"{new_name_pattern}_{i}{ext}"
    # مسیر کامل قدیمی و جدید
    old_path = os.path.join(folder, filename)
    new_path = os.path.join("changed", new_name)
    # تغییر نام
    os.rename(old_path, new_path)

print("done")
