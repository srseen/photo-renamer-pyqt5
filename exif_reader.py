from PIL import Image
from PIL.ExifTags import TAGS
import datetime
import os

def get_taken_date(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return None
        for tag, value in exif.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "DateTimeOriginal":
                return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except:
        pass
    return None