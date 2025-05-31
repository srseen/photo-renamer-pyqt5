import os
import datetime
from exif_reader import get_taken_date
from utils import get_extension

def rename_photos(folder, file_list, format_str, start_num):
    index = start_num
    renamed_count = 0

    try:
        def get_sort_key(filename):
            full_path = os.path.join(folder, filename)
            date = get_taken_date(full_path)
            if date is None:
                mtime = os.path.getmtime(full_path)
                date = datetime.datetime.fromtimestamp(mtime)
            return date

        sorted_files = sorted(file_list, key=get_sort_key)

        for filename in sorted_files:
            full_path = os.path.join(folder, filename)
            date = get_taken_date(full_path)
            ext = get_extension(filename)
            new_name = format_str.format(num=index, ext=ext, date=date) if date else format_str.format(num=index, ext=ext)
            new_path = os.path.join(folder, new_name)
            os.rename(full_path, new_path)
            index += 1
            renamed_count += 1

        return True, f"Renamed {renamed_count} files."
    except Exception as e:
        return False, str(e)
