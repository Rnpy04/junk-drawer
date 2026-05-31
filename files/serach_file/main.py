import os

def search_files(start_dir, search_query, file_extension=None):
    matches = []
    
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if search_query.lower() in file.lower(): 
                if file_extension:
                    if file.lower().endswith(file_extension.lower()):
                        matches.append(os.path.join(root, file))
                else:
                    matches.append(os.path.join(root, file))
                    
    return matches

if __name__ == "__main__":
    start_directory = input("Enter start directory (like C:\\Users\\Aren\\Videos): ")
    query = input("Enter search query (file name or a part of that): ")
    ext = input("Enter file extension to filter (example: .mp4 or .srt, empty for all): ")
    ext = ext if ext else None

    found_files = search_files(start_directory, query, ext)
    
    if found_files:
        print(f"\n count :  {len(found_files)}\n")
        for f in found_files:
            print(f)
    else:
        print("\n file not found!")
