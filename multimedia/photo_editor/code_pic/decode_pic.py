from PIL import Image 

img=Image.open(r"")
text = ""
i = 0
while True:
    if img.size[0] < 10*i:
        break
    pixel = img.getpixel((10*i, 100))
    text += chr(pixel[0])
    i += 1
print(text)