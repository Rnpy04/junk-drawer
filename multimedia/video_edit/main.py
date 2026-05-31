from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def merge_videos():
    files = input("Enter video paths separated by comma: ").split(",")
    clips = [VideoFileClip(f.strip()) for f in files]
    final = concatenate_videoclips(clips)
    final.write_videofile("merged.mp4")
    print("Merged video saved as merged.mp4")

def cut_video():
    path = input("Enter video path: ").strip()
    start = float(input("Start time (seconds): "))
    end = float(input("End time (seconds): "))

    clip = VideoFileClip(path).subclip(start, end)
    clip.write_videofile("cut.mp4")
    print("Cut video saved as cut.mp4")

def extract_audio():
    path = input("Enter video path: ").strip()
    clip = VideoFileClip(path)
    clip.audio.write_audiofile("audio.mp3")
    print("Audio saved as audio.mp3")

def menu():
    while True:
        print("\n--- Video Tool Menu ---")
        print("1. Merge videos")
        print("2. Cut video")
        print("3. Extract audio from video")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            merge_videos()
        elif choice == "2":
            cut_video()
        elif choice == "3":
            extract_audio()
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

menu()
