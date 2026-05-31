import os
import zipfile

def merge_zip_files(zip_file_list, output_zip):
    # Temporary directory for storing the extracted contents of each zip file
    temp_dir = "temp_extracted"
    
    try:
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # Extract all files from each ZIP file into the temporary directory
        for zip_file in zip_file_list:
            with zipfile.ZipFile(zip_file, 'r') as z:
                z.extractall(path=temp_dir)
        
        # Create a new ZIP file and add the combined content to it
        with zipfile.ZipFile(output_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    new_zip.write(file_path, arcname=arcname)
        
        print(f"Successfully merged {len(zip_file_list)} ZIP files into {output_zip}")
    finally:
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(temp_dir)

# Example usage
zip_files_to_merge = []
for i in range(3):
    zip_files_to_merge.append(f"class.vision.zip.part{i+1}")
    
merged_zip_file = 'merged_output.zip'
merge_zip_files(zip_files_to_merge, merged_zip_file)
