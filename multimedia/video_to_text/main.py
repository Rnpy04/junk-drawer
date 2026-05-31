import whisper
import sys
import os

def extract_audio(video_path, audio_path="temp_audio.mp3"):
    import subprocess
    
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "libmp3lame",
        "-q:a", "2",
        "-y",  # overwrite
        audio_path
    ]
    
    print("🎬 video to voice...")
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ done")
    return audio_path

def transcribe_audio(audio_path, model_size="small", language="Persian"):
    
    print(f"📥loading model {model_size}...")
    
    # بارگذاری مدل
    model = whisper.load_model(model_size)
    
    print("🎯 processing...")
    
    # تبدیل به متن
    result = model.transcribe(
        audio_path,
        language=language,
        verbose=False
    )
    
    return result["text"]

def save_to_file(text, output_path):
    """ذخیره متن در فایل"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"saved in {output_path}")

def main():
    # تنظیمات
    video_file = ""
    output_file = "text.txt"
    model_size = "small"  # tiny, base, small, medium, large
    
    # بررسی وجود فایل
    if not os.path.exists(video_file):
        print(f"❌ فایل {video_file} یافت نشد!")
        return
    
    try:
        # مرحله ۱: استخراج صدا از ویدیو
        audio_path = "temp_audio.mp3"
        extract_audio(video_file, audio_path)
        
        # مرحله ۲: تبدیل به متن
        text = transcribe_audio(audio_path, model_size)
        
        # مرحله ۳: ذخیره در فایل
        save_to_file(text, output_file)
        
        # نمایش متن
        print("\n" + "="*50)
        print("📝text:")
        print("="*50)
        print(text)
        
        # پاک کردن فایل موقت
        os.remove(audio_path)
        print("\n✨ done")
        
    except Exception as e:
        print(f"❌ error: {e}")

if __name__ == "__main__":
    main()