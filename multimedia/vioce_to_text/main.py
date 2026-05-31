import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

model = whisper.load_model("small").to(device)  

audio_file = "audio.mp3"

result = model.transcribe(audio_file, language="fa")

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])

print("saved")
