import subprocess
import os

def remove_vocals(input_audio, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "demucs",
        "--two-stems", "vocals",
        input_audio,
        "-o", output_dir
    ]

    subprocess.run(command, check=True)

    print("Done! Instrumental and vocals separated.")

remove_vocals("song.mp3")
