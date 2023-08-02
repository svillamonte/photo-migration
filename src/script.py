# big folder is www:www
# sudo docker build -t photo-migration .
# sudo docker run -v /mnt/photos_src/:/mnt/photos_src/ -v /mnt/photos/:/mnt/photos/ photo-migration

from PIL import Image
from PIL.ExifTags import TAGS
import os
from datetime import datetime
import shutil

def get_image_taken_date(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        return value
            return None
    except (AttributeError, KeyError, IndexError):
        return None

def copy_file_with_dirs(src_file, dest_file):
    dest_path = os.path.dirname(dest_file)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    try:
        shutil.copy2(src_file, dest_file)
    except FileNotFoundError:
        print(f"Source file '{src_file}' not found.")
    except PermissionError:
        print(f"Permission denied while copying '{src_file}' to '{dest_file}'.")
    except Exception as e:
        print(f"Error occurred: {e}")

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def get_file_path(src_image, date_taken):
    extension = os.path.splitext(src_image)[1]

    target_filename = "IMG" + date_taken.strftime("%Y%m%d%H%M%S")
    target_directory = date_taken.strftime("%Y/%m/%d")

    return "/mnt/photos/" + target_directory + "/" + target_filename + extension

def process_image(image_path, filename):
    print(f"Processing: {filename}")

    try:
        date_taken = get_image_taken_date(image_path)
        parsed_date_taken = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")
        target_path = get_file_path(image_path, parsed_date_taken)

        copy_file_with_dirs(image_path, target_path)
    except:
        print(f"{image_path} failed")
        default_path = "/mnt/photos/failures/" + filename
        copy_file_with_dirs(image_path, default_path)

if __name__ == "__main__":
    folder_path = "/mnt/photos_src/big"
    i = 0
    for filename in os.listdir(folder_path):
        if (i := i + 1) > 5:
            break

        image_path = os.path.join(folder_path, filename)        
        process_image(image_path, filename)
