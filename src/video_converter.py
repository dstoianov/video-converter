import os
import shlex
import subprocess
import time

from src import logger

# path = '/media/funker/3/FOTO/2017/2017-Samsung A5 and S7 Denys/2017-04/'
path = '/Users/dstoianov/Documents/convert-video/'

csv_file_name = 'movies_all_mp4_2017.csv'

files = []
files_ext = {}
skipped_file_extensions = ['nfo', 'ini', 'jpg', 'txt', 'db', 'png', 'jpeg', 'sh']

"""
http://coderunner.io/shrink-videos-with-ffmpeg-and-preserve-metadata/


ffmpeg -i "input.mp4" -copy_unknown -map_metadata 0 -map 0 -codec copy \
    -codec:v libx264 -pix_fmt yuv420p -crf 23 \
    -codec:a libfdk_aac -vbr 4 \
    -preset fast "output.mp4"
    
"""


def get_media_properties(filename):
    result = subprocess.Popen(['hachoir-metadata', filename, '--raw'],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    results = result.stdout.readlines()

    properties = {}

    for item in results:

        if item.startswith('- duration'):
            properties['duration'] = item.lstrip('- duration: ').strip()

        if item.startswith('- mime_type'):
            properties['mime_type'] = item.lstrip('- mime_type: ').strip()

        if item.startswith('- width: '):
            properties['width'] = item.lstrip('- width: ').strip()

        if item.startswith('- height: '):
            properties['height'] = item.lstrip('- height: ').strip()

        if item.startswith('- creation_date'):
            properties['creation_date'] = item.lstrip('- creation_date: ').strip()

        if item.startswith('- last_modification'):
            properties['last_modification'] = item.lstrip('- last_modification: ').strip()

    return properties


def read_files():
    local_files = []
    # r=root, d=directories, f = files
    for r, d, ff in os.walk(path):
        for file in ff:
            if file in ['.directory', 'desktop.ini', '.DS_Store']:
                continue
            if file.split('.')[-1].lower() in skipped_file_extensions:
                continue

            full_path = os.path.join(r, file)
            size_mb = round(os.path.getsize(full_path) / 1024 / 1024, 2)
            local_files.append({'name': file, 'size': size_mb, 'path': full_path})

    logger.info("Total collected '%s' files " % str(len(local_files)))
    logger.info("=== " * 20)
    return local_files


def convert_videos(files):
    logger.info("Going to convert files..")
    # 18 more quality, 23 - default, 28 less quality
    crf = 23
    prefix = '-crf-'
    for filename in files:
        if prefix in filename['name']:
            continue
        input_file = filename['path']
        chunks = input_file.split(".")
        output_file = f"{chunks[0]}{prefix}{crf}.mp4"
        command = f"ffmpeg -i {input_file} -copy_unknown -map_metadata 0 -map 0 -codec copy \
            -codec:v libx264 -pix_fmt yuv420p -crf {crf} \
            -codec:a aac -vbr 5 \
            -preset medium {output_file}"
        #   presets: slow, medium, fast
        # print(command)

        logger.info("Converting file '%s - %sMb'..", filename['name'], filename['size'])
        start = time.time()
        if not os.path.isfile(output_file):
            res = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 universal_newlines=True)
            if 'Conversion failed!' in res.stdout:
                logger.error(res.stdout)
                raise Exception('Error. Check parameters for decoding.')

        end = time.time()
        size_mb = round(os.path.getsize(output_file) / 1024 / 1024, 2)
        logger.info("\tElapsed time '%.4s' sec", end - start)
        logger.info("\tOld size '%sMb' new size '%sMb', ratio '%.4s'", filename['size'], size_mb,
                    filename['size'] / size_mb)


def collect_statistics():
    logger.info("Collect statistics..")
    file_types = []
    for file in files:
        f_ext = file['name'].split('.')[-1]
        file_types.append(f_ext)

    for extension in set(file_types):
        files_ext[extension] = file_types.count(extension)

    logger.info(files_ext)

    logger.info("Check for duplicates..")

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
            else:
                logger.warn("Skipp deleting...")
    logger.info("=== " * 20)


def read_files_metadata():
    logger.info("Collect file metadata..")
    for i, file in enumerate(files):
        logger.info("Processing %s) '%s' file..", str(i), file['name'])
        properties = get_media_properties(file['path'])
        file.update(properties)

    logger.info("=== " * 20)


def list_duplicates(seq):
    return sorted(set([x for x in seq if seq.count(x) > 1]))


def delete_files(files: list):
    logger.info("Potential released size '%sMb'", sum([i['size'] for i in files]))

    for file in files:
        logger.info(f"Removing file '{file['path']}'..")
        os.remove(file['path'])


if __name__ == "__main__":
    # files = read_files()
    # collect_statistics()

    # read_files_metadata()
    # delete_broken_files(delete=True)
    # fnames = ['name', 'size', 'duration', 'mime_type', 'width', 'height', 'creation_date', 'last_modification', 'path']
    # write_to_csv_file(csv_file_name, files, fnames)
    # convert_videos(files)

    all_files = read_files()

    files_to_delete = list(filter(lambda d: '-crf-23.mp4' in d['name'], all_files))
    delete_files(files_to_delete)

    logger.info('Done')
