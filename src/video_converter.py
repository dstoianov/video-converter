import os
import shlex
import subprocess
import time

from src import logger, write_to_csv_file

# path = '/Users/dstoianov/Documents/convert-video/'
path = '/media/funker/3/FOTO/2016/'
# path = '/media/funker/3/FOTO/2016/2016-Lenovo-S850-Lena/'

csv_file_name = f"{path.replace('/', '_').replace(' ', '_')}.csv".lower()

files = []
files_ext = {}
skipped_file_extensions = ['nfo', 'ini', 'jpg', 'nef', 'txt', 'db', 'png', 'jpeg', 'sh', 'gif', 'pdf', 'ppt', 'mp3',
                           'xls', 'mht', 'htm', 'zip']

"""
19 FFmpeg Commands For All Needs
        https://catswhocode.com/ffmpeg-commands/

Video files taking up too much space? Let's shrink them with FFmpeg!
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
    logger.info("=== " * 20)
    logger.info("Collecting files..")
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
    return local_files


def convert_videos(files):
    logger.info("=== " * 20)
    logger.info("Convert files..")
    # 18 more quality, 23 - default, 28 less quality
    crf = 23
    prefix = '-ffmpeg-crf-'
    g_start = time.time()
    for i, filename in enumerate(files, start=1):
        if prefix in filename['name']:
            continue  # skipp already decoded files by prefix
        input_file = filename['path']
        chunks = input_file.split(".")
        output_file = f"{chunks[0]}{prefix}{crf}.mp4"
        command = f"ffmpeg -i \"{input_file}\" -copy_unknown -map_metadata 0 -map 0 -codec copy \
            -codec:v libx264 -pix_fmt yuv420p -crf {crf} \
            -codec:a aac -vbr 5 \
            -preset medium \"{output_file}\""
        #   presets: slow, medium, fast
        # print(command)

        logger.info("%s) Converting file '%s - %sMB - %s sec'..", str(i), filename['name'], filename['size'],
                    filename['duration'])
        start = time.time()
        if not os.path.isfile(output_file):
            res = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 universal_newlines=True)
            if 'Conversion failed!' in res.stdout:
                logger.error(res.stdout)
                raise Exception('Error. Check parameters for decoding.')

        size_mb = round(os.path.getsize(output_file) / 1024 / 1024, 2)
        logger.info("\tElapsed time for converting '%s'", time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))
        logger.info("\tOld size '%sMB' --> new size '%sMB', ratio '%.4s'", filename['size'], size_mb,
                    filename['size'] / size_mb)

    logger.info("Total elapsed time for converting '%s'", time.strftime("%H:%M:%S", time.gmtime(time.time() - g_start)))


def aaa(start_time):
    e = int(time.time() - start_time)
    return "{:02d}:{:02d}:{:02d}".format(e // 3600, (e % 3600 // 60), e % 60)


def collect_statistics():
    logger.info("=== " * 20)
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


def delete_broken_files(delete=False):
    logger.info("=== " * 20)
    logger.info("Delete broken files..")
    for file in files:
        if file.get('duration') is None:
            logger.info("delete file '%s', size '%.5s' MB", file['path'], file['size'])
            if delete:
                os.remove(file['path'])
            else:
                logger.warn("Skipp deleting...")


def read_files_metadata():
    logger.info("=== " * 20)
    logger.info("Collect file metadata..")
    for i, file in enumerate(files, start=1):
        logger.info(" %s) Processing '%s' file - '%sMB'..", str(i), file['name'], file['size'])
        properties = get_media_properties(file['path'])
        file.update(properties)

    logger.info("======= Total collected '%s' files =======", len(files))


def list_duplicates(seq):
    return sorted(set([x for x in seq if seq.count(x) > 1]))


def delete_files(files: list, delete=False):
    for file in files:
        logger.info(f"Removing file '{file['path']}'..")
        if delete:
            os.remove(file['path'])
        else:
            logger.info("\tskipp removing..")


def delete_decoded_files(delete):
    all_files = read_files()
    logger.info("=== " * 20)
    logger.info("Delete converted files..")
    files_converted = list(filter(lambda d: '-crf-23.mp4' in d['name'], all_files))
    files_to_delete = list(filter(lambda d: '-crf-23.mp4' not in d['name'], all_files))

    new_size = sum([i['size'] for i in files_to_delete])
    old_size = sum([i['size'] for i in files_converted])
    logger.info("Old size '%.7sMB', new size '%.7sMB', released size '%.7sMB'", old_size, new_size,
                (old_size - new_size))

    delete_files(files_to_delete, delete)


if __name__ == "__main__":
    files = read_files()
    collect_statistics()

    read_files_metadata()
    delete_broken_files(delete=False)
    fnames = ['name', 'size', 'duration', 'mime_type', 'width', 'height', 'creation_date', 'last_modification', 'path']
    write_to_csv_file(csv_file_name, files, fnames)
    convert_videos(files)

    delete_decoded_files(delete=False)

    logger.info('Done')
