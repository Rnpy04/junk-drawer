import subprocess

# Run a Python script from within the same directory
result = subprocess.run(['cmd', '/c', 'ffmpeg', '-i','input.mkv','-map','0:s:0','subtitle.srt'], capture_output=True, text=True)
  
