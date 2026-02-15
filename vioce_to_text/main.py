import whisper
import torch

# 1. بررسی GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# 2. بارگذاری مدل بزرگتر برای دقت بیشتر
model = whisper.load_model("small").to(device)  # میتونی medium یا large هم بزنی

# 3. فایل صوتی
audio_file = "audio.mp3"

# 4. تبدیل صدا به متن فارسی
result = model.transcribe(audio_file, language="fa")

# 6. ذخیره متن در فایل
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("saved")
