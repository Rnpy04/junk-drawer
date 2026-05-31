import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    'User-Agent': ''
    }

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

def extract_links_from_page(url, base_url=None):
    try:
        resp = SESSION.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"خطا در دریافت صفحه {url}: {e}")
        return []
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href'].strip()
        if not href:
            continue
        abs_url = urljoin(base_url or url, href)
        links.append(abs_url)
    return links

def filter_links(links, pattern, use_regex=False):
    if use_regex:
        compiled = re.compile(pattern)
        return [link for link in links if compiled.search(link)]
    else:
        return [link for link in links if pattern in link]

def download_file(url, output_folder, max_retries=3):
    local_filename = os.path.join(output_folder, url.split('/')[-1])
    if os.path.exists(local_filename):
        file_size = os.path.getsize(local_filename)
        print(f"[SKIP] {local_filename} از قبل وجود دارد.")
        return local_filename
    
    for attempt in range(max_retries):
        try:
            # درخواست با هدر resume
            headers = HEADERS.copy()
            if os.path.exists(local_filename):
                existing_size = os.path.getsize(local_filename)
                headers['Range'] = f'bytes={existing_size}-'
            else:
                existing_size = 0
                
            resp = SESSION.get(url, stream=True, headers=headers, timeout=30)
            resp.raise_for_status()
            
            mode = 'ab' if existing_size > 0 else 'wb'
            with open(local_filename, mode) as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"[OK] دانلود شد: {local_filename}")
            return local_filename
        except Exception as e:
            print(f"[ERROR] تلاش {attempt+1} برای {url} ناموفق: {e}")
            time.sleep(2)
    print(f"[FAIL] دانلود نشد: {url}")
    return None

def main():
    parser = argparse.ArgumentParser(description='دانلود منعطف لینک‌های یک صفحه وب بر اساس الگو')
    parser.add_argument('url', help='آدرس صفحه‌ای که می‌خواهید لینک‌هایش را استخراج کنید')
    parser.add_argument('-p', '--pattern', required=True, help='الگوی جستجو (مثلاً .mkv یا .rar یا regex)')
    parser.add_argument('-r', '--regex', action='store_true', help='اگر الگو از نوع regex است این گزینه را فعال کنید')
    parser.add_argument('-o', '--output', default='downloads', help='پوشه ذخیره فایل‌ها (پیش‌فرض: downloads)')
    parser.add_argument('-d', '--download', action='store_true', help='فعال کردن دانلود خودکار (در غیر این صورت فقط لیست لینک‌ها نشان داده می‌شود)')
    parser.add_argument('-t', '--threads', type=int, default=3, help='تعداد تردهای همزمان برای دانلود (پیش‌فرض: 3)')
    args = parser.parse_args()
    
    # ایجاد پوشه خروجی
    os.makedirs(args.output, exist_ok=True)
    
    print(f"در حال بررسی صفحه: {args.url}")
    all_links = extract_links_from_page(args.url, args.url)
    print(f"تعداد کل لینک‌های یافت شده: {len(all_links)}")
    
    filtered = filter_links(all_links, args.pattern, use_regex=args.regex)
    print(f"تعداد لینک‌های منطبق با الگو: {len(filtered)}")
    
    if not filtered:
        print("هیچ لینکی با الگوی مورد نظر یافت نشد.")
        return
    
    # نمایش لینک‌ها
    for idx, link in enumerate(filtered, 1):
        print(f"{idx}: {link}")
    
    if args.download:
        print(f"\nشروع دانلود {len(filtered)} فایل با {args.threads} ترد همزمان...")
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = {executor.submit(download_file, link, args.output): link for link in filtered}
            for future in as_completed(futures):
                link = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"خطا در دانلود {link}: {e}")
        print("عملیات دانلود به پایان رسید.")
    else:
        print("\nبرای دانلود خودکار، اسکریپت را با گزینه -d اجرا کنید.")
        print(f"مثال: python {os.path.basename(__file__)} {args.url} -p '{args.pattern}' -d")

if __name__ == "__main__":
    main()