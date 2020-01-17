import csv
import logging
import os
from typing import List

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def read_csv_to_list(csv_file_name: str) -> List:
    with open(csv_file_name) as f:
        records = csv.DictReader(f)
        movies_ordered = list(records)
        movies = [dict(m) for m in movies_ordered]
        return movies


def write_to_csv_file(csv_file_name: str, files: list, fnames: List[str]):
    if len(files) == 0:
        logger.info("There is no files to write. Exit.")
        return
    logger.info("Write to csv '%s' file...", csv_file_name)

    sorted_list = sorted(files, key=lambda i: i['name'])

    with open(csv_file_name, mode='w') as f:
        writer = csv.DictWriter(f, fieldnames=fnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for file in sorted_list:
            writer.writerow(file)


def read_files(path: str, skipped_file_extensions: list):
    logger.info("=== " * 20)
    logger.info("Collecting files in folder '%s'..", path)
    local_files = []
    # r=root, d=directories, f = files
    for r, d, ff in os.walk(path):
        for file in ff:
            if file.split('.')[-1].lower() in skipped_file_extensions:
                continue

            full_path = os.path.join(r, file)
            size_mb = round(os.path.getsize(full_path) / 1024 / 1024, 2)
            local_files.append({'name': file, 'size': size_mb, 'path': full_path})

    logger.info("Total collected '%s' files " % str(len(local_files)))
    return local_files
