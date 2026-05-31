from PIL import Image 
img=Image.open(r"")
# print(type(img.size))
# print(ord('a'))
# print(ord('z'))
ramz=""
for i in range(len(ramz)):
    img.putpixel((10*i,100),(ord(ramz[i]),0,0))
img.show()
img.save(r"")