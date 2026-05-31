# from PIL import Image # pyright: ignore[reportMissingImports]
# import openpyxl.workbook  # pyright: ignore[reportMissingModuleSource]
# # img=Image.open(r"")


# # new_img=img.resize((640,360))
# # new_img.show()
# # # print(img.size)




# def resize(path,x,y):
#     img=Image.open(path)
#     new_img=img.resize((x,y))
#     return new_img

# new_img=resize(r"",640,360)
# new_img.save(r"")

from PIL import Image
import os

def resize_images(paths, output_folder, width=500, height=500):
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for path in paths:
        img = Image.open(path)
        new_img = img.resize((width, height))
        
        # Get the file name from the path
        file_name = os.path.basename(path)
        
        # Save the resized image in the output folder
        save_path = os.path.join(output_folder, file_name)
        new_img.save(save_path)
        print(f"Saved resized image to: {save_path}")

# Example usage
images = [

]

resize_images(images, "")
