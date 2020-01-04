import csv
import logging
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

    with open(csv_file_name, mode='w') as f:
        writer = csv.DictWriter(f, fieldnames=fnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for movie in files:
            writer.writerow(movie)
