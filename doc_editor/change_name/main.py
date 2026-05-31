import os

folder = "files"

new_name_pattern = "12345678912345678912345678912345"

files = os.listdir(folder)

files.sort()

for i, filename in enumerate(files, start=1):
    ext = os.path.splitext(filename)[1]  # .jpg, .png, ...
    new_name = f"{new_name_pattern}{ext}"
    old_path = os.path.join(folder, filename)
    new_path = os.path.join("changed", new_name)
    os.rename(old_path, new_path)

print("done")
