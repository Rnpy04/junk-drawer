# from pytube import YouTube
# # import os
# # import pytube
# import socks
# import socket

# # اگر از proxy socks5 مثل shadowrocket یا v2ray استفاده می‌کنی
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 2080)
# socket.socket = socks.socksocket


# try:
#     url = input("Enter the YouTube URL: ")
    
#     yt = YouTube(url)
    
#     print("Title:", yt.title)
#     print("Views:", yt.views)

#     # Get the highest resolution stream
#     yd = yt.streams.get_highest_resolution()
    

#     yd.download()
    
#     print("Download complete.")
# except Exception as e:
#     print("An error occurred:", str(e))
import yt_dlp

# آدرس پروکسی SOCKS5 (مثال: لوکال هاست و پورت 2080)
proxy = "socks5://127.0.0.1:2080"
url = input("url : ")

quality = input("quality: ")

# تنظیمات yt-dlp
ydl_opts = {
    'proxy': proxy,
    'format': quality,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("done")
except Exception as e:
    print("error : ", e)
