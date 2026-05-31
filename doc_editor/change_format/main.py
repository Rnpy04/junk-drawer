from PIL import Image
import os

folder_path = "files"

new_format = "png"

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    if filename.lower().endswith(("jpg", "jpeg", "bmp", "tiff", "gif", "png")):
        img = Image.open(file_path)
        
        base_name = os.path.splitext(filename)[0]
        
        new_file_path = os.path.join("new", f"{base_name}.{new_format}")
        
        img.save(new_file_path)
        print(f"{filename} -> {base_name}.{new_format}")
