import os

from PIL import Image
from movies import logger

# path = '/media/funker/3/FOTO/2018/2018-Samsung_A5_and_S9/2018-03/'
path = '/media/funker/3/FOTO/2017/'
# path = '/home/funker/video/src/'


files = []
files_ext = {}
skipped_file_extensions = ['nfo', 'mp3', 'avi', '3gp', 'mp4', 'mov', 'txt', 'db', 'pdf']


def read_exif():
    logger.info("Collect statistics..")

    for file in files:
        try:
            img = Image.open(file['path'])
            img_exif = img.getexif()

            # print(type(img_exif))
            # <class 'PIL.Image.Exif'>

            if img_exif:
                continue
                # print(dict(img_exif))
                # { .. 271: 'FUJIFILM', 305: 'Adobe Photoshop Lightroom 6.14 (Macintosh)', }

                # img_exif_dict = dict(img_exif)
                # for key, val in img_exif_dict.items():
                #     if key in ExifTags.TAGS:
                #         print(f"{ExifTags.TAGS[key]}: {repr(val)}")
            else:
                print(f"Sorry, image has no exif data '{file['path']}'")
        except IOError as e:
            print(f"Can't open file '{file['path']}'")


def collect_files():
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if file in ['.directory', 'desktop.ini']:
                continue
            if file[-6:].split('.')[1].lower() in skipped_file_extensions:
                continue

            full_path = os.path.join(r, file)
            size_mb = round(os.path.getsize(full_path) / 1024 / 1024, 2)
            files.append({'name': file, 'size': size_mb, 'path': full_path})

    logger.info("Total collected '%s' files " % str(len(files)))
    logger.info("=== " * 20)


def collect_statistics():
    logger.info("Collect statistics..")
    file_types = []
    for file in files:
        f_ext = file['name'].split(".")[-1]
        file_types.append(f_ext)

    for extension in set(file_types):
        files_ext[extension] = file_types.count(extension)

    logger.info(files_ext)

    logger.info("Find duplicates..")

    names = list(a['name'] for a in files)
    duplicates = list_duplicates(names)
    logger.info("Found '%s' duplicates %s", len(duplicates), duplicates)
    logger.info("=== " * 20)


def delete_broken_files(delete=False):
    for file in files:
        if file.get('duration') is None:
            logger.info("delete file '%s', size '%.5s' Mb", file['path'], file['size'])
            if delete:
                os.remove(file['path'])
    logger.info("=== " * 20)


def list_duplicates(seq):
    return sorted(set([x for x in seq if seq.count(x) > 1]))


if __name__ == "__main__":
    collect_files()
    read_exif()
    collect_statistics()
    #
    # delete_broken_files(False)

    logger.info('Done')
