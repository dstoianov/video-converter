import os
import shlex
import subprocess
import time

from src import logger, write_to_csv_file, read_files

params = [
    {'crf': '23', 'codec': 'libx264'},  # 18 more quality, 23 - default, 28 less quality
    {'crf': '28', 'codec': 'libx265'}  # 28 - default
]
param = params[1]  # 0 or 1

"""
19 FFmpeg Commands For All Needs
        https://catswhocode.com/ffmpeg-commands/

Video files taking up too much space? Let's shrink them with FFmpeg!
        http://coderunner.io/shrink-videos-with-ffmpeg-and-preserve-metadata/


ffmpeg -i "input.mp4" -copy_unknown -map_metadata 0 -map 0 -codec copy \
    -codec:v libx264 -pix_fmt yuv420p -crf 23 \
    -codec:a aac -vbr 5 \
    -preset fast "output.mp4"
    
"""


def get_media_properties(filename):
    result = subprocess.Popen(['hachoir-metadata', filename, '--raw'],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    results = result.stdout.readlines()

    properties = {}

    for item in results:

        if item.startswith('- duration'):
            properties['duration'] = item.lstrip('- duration: ').strip().split('.')[0]

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


def elapsed_time(started_time):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - started_time))


def convert_videos(files):
    logger.info("=== " * 20)
    logger.info("Convert files..")
    errors = []  # Errors counter
    # 18 more quality, 23 - default, 28 less quality
    crf = param['crf']
    codec = param['codec']
    prefix = f"-ffmpeg-{codec}-crf-"
    g_start = time.time()
    for i, filename in enumerate(files, start=1):
        if 'ffmpeg' in filename['name']:
            continue  # skipp already decoded files by prefix
        input_file = filename['path']
        chunks = input_file.split(".")
        output_file = f"{chunks[0]}{prefix}{crf}-fast.mp4"
        command = f"ffmpeg -i \"{input_file}\" -copy_unknown -map_metadata 0 -map 0 -codec copy \
            -codec:v {codec} -pix_fmt yuv420p -crf {crf} \
            -codec:a aac -vbr 5 \
            -tag:v hvc1 \
            -max_muxing_queue_size 4000 \
            -preset fast \"{output_file}\""
        #   presets: slow, medium, fast
        # print(command)

        logger.info("%s) Converting file '%s - %sMB - %s sec'..", str(i), filename['name'], filename['size'],
                    filename['duration'])
        start = time.time()
        if not os.path.isfile(output_file):
            res = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 universal_newlines=True)
            if 'Conversion failed!' in res.stdout or 'Invalid argument' in res.stdout:
                errors.append({'name': filename['name'], 'command': command})
                # errors.append({'name': filename['name'], 'command': command,'error': res.append})
                logger.error('Error. Check parameters for decoding.')
                continue

        new_size_mb = round(os.path.getsize(output_file) / 1024 / 1024, 2)
        logger.info("\tConverting time '%s', original size '%sMB' --> new size '%sMB', ratio '%.4s'",
                    elapsed_time(start), filename['size'], new_size_mb, filename['size'] / new_size_mb)

    logger.info("Total elapsed time for converting '%s'", elapsed_time(g_start))
    if len(errors) > 0:
        logger.error("Files with errors, check this manual")
        print(errors)


def collect_statistics(files):
    logger.info("=== " * 20)
    logger.info("Collect statistics..")
    file_types = []
    files_ext = {}
    for file in files:
        f_ext = file['name'].split('.')[-1]
        file_types.append(f_ext)

    for extension in set(file_types):
        files_ext[extension] = file_types.count(extension)

    logger.info(files_ext)

    logger.info("Check for duplicates..")

    names = list(file['name'] for file in files)
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
                logger.warning("Skipp deleting...")


def read_files_metadata(files):
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
        message = f"Removing file '{file['path']}'.."
        if delete:
            logger.info(message)
            os.remove(file['path'])
        else:
            logger.info(f"\t{message} --> skipp removing..")


def delete_decoded_files(path, extetions, delete):
    all_files = read_files(path=path, skipped_file_extensions=extetions)
    logger.info("=== " * 20)
    logger.info("Delete converted files..")
    files_converted = list(filter(lambda d: 'ffmpeg' in d['name'], all_files))
    files_to_delete = list(filter(lambda d: 'ffmpeg' not in d['name'], all_files))

    old_size = sum([i['size'] for i in files_to_delete])
    new_size = sum([i['size'] for i in files_converted])
    logger.info("Old size '%.7sMB', new size '%.7sMB', released size '%.7sMB'",
                old_size, new_size, (old_size - new_size))

    delete_files(files_to_delete, delete)


if __name__ == "__main__":
    # path = '/Users/dstoianov/Documents/convert-video/'
    path = '/media/funker/3/FOTO/2013/'
    skipped_file_extensions = ['nfo', 'ini', 'jpg', 'nef', 'txt', 'db', 'png', 'jpeg', 'sh', 'gif', 'pdf', 'ppt', 'mp3',
                               'xls', 'mht', 'htm', 'zip', 'directory', 'ds_store']

    files = read_files(path=path, skipped_file_extensions=skipped_file_extensions)
    collect_statistics(files)

    read_files_metadata(files)

    delete_broken_files(delete=False)
    fnames = ['name', 'size', 'duration', 'mime_type', 'width', 'height', 'creation_date', 'last_modification', 'path']
    csv_file_name = f"{path.replace('/', '_').replace(' ', '_')}.csv".lower()
    write_to_csv_file(csv_file_name, files, fnames)
    # convert_videos(files)

    delete_decoded_files(path=path, extetions=skipped_file_extensions, delete=False)

    logger.info('Done')
