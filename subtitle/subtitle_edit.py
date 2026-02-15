from datetime import timedelta
import re

# مسیر فایل اصلی و فایل خروجی
input_path = r"D:\film\series\1friends\Friends English Subtitles\Friends - season 10.en"+"\\"
input_file = input_path+"Friends - 10x03 - The One With Ross's Tan.en.srt"
output_file = input_path+"edited.srt"

# تابع تبدیل زمان SRT به timedelta
def srt_time_to_timedelta(srt_time):
    h, m, s_ms = srt_time.split(":")
    s, ms = s_ms.split(",")
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))

# تابع تبدیل timedelta به زمان SRT
def timedelta_to_srt_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = td.microseconds // 1000 + td.seconds % 1 * 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{td.microseconds // 1000:03}"

# خواندن فایل
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

pattern = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")
shifted_lines = []

for line in lines:
    match = pattern.match(line)
    if match:
        start = srt_time_to_timedelta(match.group(1)) + timedelta(seconds=6.7)
        end = srt_time_to_timedelta(match.group(2)) + timedelta(seconds=6.7)
        shifted_lines.append(f"{str(start)[:-3].replace('.',',')} --> {str(end)[:-3].replace('.',',')}\n")
    else:
        shifted_lines.append(line)

# ذخیره فایل جدید
with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(shifted_lines)

print("saved")
