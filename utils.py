def is_image_file(filename):
    ext = filename.lower().split('.')[-1]
    return ext in ['jpg', 'jpeg', 'png', 'heic', 'gif','GIF','mov', 'mp4', 'avi', 'mkv', 'webp', 'bmp', 'tiff', 'tif']

def get_extension(filename):
    return filename.lower().split('.')[-1]