from PIL import Image
import os

image_folder = "images"
output_pdf = "output.pdf"

image_files = [f for f in os.listdir(image_folder) if f.endswith((".png", ".jpg", ".jpeg"))]

image_files.sort()

images = [Image.open(os.path.join(image_folder, f)).convert('RGB') for f in image_files]

if images:
    first_image = images[0]
    rest_images = images[1:]
    first_image.save(output_pdf, save_all=True, append_images=rest_images)
    print(f" done : {output_pdf}")
else:
    print("هیچ تصویری پیدا نشد!")
