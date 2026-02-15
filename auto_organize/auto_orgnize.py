import os
import shutil
from pathlib import Path

class DownloadOrganizer:
    def __init__(self, download_path=None):
        """
        سازماندهی فایل‌های دانلود بر اساس نوع
        """
        if download_path is None:
            self.download_path = Path.home() / "Downloads"
        else:
            self.download_path = Path(download_path)
        
        # دسته‌بندی فایل‌ها بر اساس پسوند
        self.file_categories = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Programs': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'],
            'Others': [] 
        }
    
    def create_folders(self):
        """ایجاد پوشه‌های مورد نیاز"""
        for folder_name in self.file_categories.keys():
            folder_path = self.download_path / folder_name
            folder_path.mkdir(exist_ok=True)
            print(f"✓ پوشه {folder_name} ایجاد شد: {folder_path}")
    
    def get_file_category(self, file_extension):
        """تشخیص دسته‌بندی فایل بر اساس پسوند"""
        file_extension = file_extension.lower()
        for category, extensions in self.file_categories.items():
            if file_extension in extensions:
                return category
        return 'Others'
    
    def organize_files(self, dry_run=False):
        """
        سازماندهی فایل‌ها
        dry_run=True فقط نمایش می‌دهد بدون جابجایی
        """
        if not self.download_path.exists():
            print(f"❌ پوشه دانلود یافت نشد: {self.download_path}")
            return
        
        # ایجاد پوشه‌ها
        if not dry_run:
            self.create_folders()
        
        moved_files = 0
        skipped_files = 0
        
        # پیمایش فایل‌های موجود در پوشه دانلود
        for file_path in self.download_path.iterdir():
            # نادیده گرفتن پوشه‌ها و فایل‌های مخفی
            if file_path.is_dir() or file_path.name.startswith('.'):
                continue
            
            # تشخیص دسته‌بندی فایل
            file_extension = file_path.suffix
            category = self.get_file_category(file_extension)
            
            # مسیر مقصد
            destination_folder = self.download_path / category
            destination_path = destination_folder / file_path.name
            
            # چک کردن وجود فایل در مقصد
            if destination_path.exists():
                print(f"⚠️  فایل وجود دارد: {file_path.name}")
                skipped_files += 1
                continue
            
            # نمایش عملیات
            print(f"📁 {file_path.name} → {category}/")
            
            # جابجایی فایل (اگر dry_run نباشد)
            if not dry_run:
                try:
                    shutil.move(str(file_path), str(destination_path))
                    moved_files += 1
                except Exception as e:
                    print(f"❌ خطا در جابجایی {file_path.name}: {e}")
                    skipped_files += 1
            else:
                moved_files += 1
        
        # گزارش نهایی
        print("\n" + "="*50)
        if dry_run:
            print(f"🔍  {moved_files} ready file ")
        else:
            print(f"✅ complete")
            print(f"📊  {moved_files}move. {skipped_files} pass")
    
    def show_statistics(self):
        """نمایش آمار فایل‌های موجود"""
        stats = {}
        total_files = 0
        
        for file_path in self.download_path.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                category = self.get_file_category(file_path.suffix)
                stats[category] = stats.get(category, 0) + 1
                total_files += 1
        
        print("\n📊 exist:")
        print("="*30)
        for category, count in sorted(stats.items()):
            print(f"{category}: {count} file")
        print(f"\nall : {total_files}")

def main():
    # ایجاد نمونه سازماندهنده
    organizer = DownloadOrganizer("D:\Downloads_d")
    
    print("🗂️  organize")
    print("="*40)
    
    # نمایش آمار فعلی
    organizer.show_statistics()
    
    # اجرای حالت نمایش (بدون جابجایی واقعی)
    print("\n🔍 حالت نمایش (بدون جابجایی):")
    organizer.organize_files(dry_run=True)
    
    response = input("\n❓do you want ?(y/n): ")
    
    if response.lower() in ['y', 'yes', 'بله']:
        print("\n🚀 start..")
        organizer.organize_files(dry_run=False)
    else:
        print("❌ cancel")

if __name__ == "__main__":
    main()