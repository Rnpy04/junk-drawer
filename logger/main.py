import datetime
import time
import psutil
import socket

def get_network_usage():
    net_io = psutil.net_io_counters()
    return {
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv,
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv
    }

def format_bytes(bytes_value):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"

# ذخیره مقادیر اولیه
initial_usage = get_network_usage()
last_usage = initial_usage

while True:
    try:
        current_usage = get_network_usage()
        now = datetime.datetime.now()
        
        # محاسبه مصرف از ابتدا
        total_sent = current_usage['bytes_sent'] - initial_usage['bytes_sent']
        total_recv = current_usage['bytes_recv'] - initial_usage['bytes_recv']
        
        # محاسبه مصرف از آخرین لاگ
        interval_sent = current_usage['bytes_sent'] - last_usage['bytes_sent']
        interval_recv = current_usage['bytes_recv'] - last_usage['bytes_recv']
        
        with open("internet_log.txt", "a", encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"زمان: {now}\n")
            f.write(f"مصرف کل - ارسال: {format_bytes(total_sent)} | دریافت: {format_bytes(total_recv)}\n")
            f.write(f"مصرف در 10 ثانیه - ارسال: {format_bytes(interval_sent)} | دریافت: {format_bytes(interval_recv)}\n")
            f.write(f"سرعت لحظه‌ای - آپلود: {format_bytes(interval_sent/10)}/s | دانلود: {format_bytes(interval_recv/10)}/s\n")
        
        last_usage = current_usage
        
        print(f"[{now}] download: {format_bytes(interval_recv/10)}/s | upload: {format_bytes(interval_sent/10)}/s")
        
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("\n stoped.")
        break
    except Exception as e:
        print(f"error: {e}")
        time.sleep(10)