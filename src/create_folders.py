import os
import pathlib

from src import logger, read_files


def prepare_dirs(path: str):
    files = read_files(path=path, skipped_file_extensions=[])
    dirs = set(f['name'][:6] for f in files)  # extract potential dirs
    my_dirs = sorted(set(d[:4] + '-' + d[4:] for d in dirs if d.isdigit()))  # insert '-' in the dir name
    print(my_dirs)
    return files, my_dirs


def create_dirs_if_not_exist(path: str, dirs: list):
    for _dir in dirs:
        to_create = path + _dir
        if not os.path.exists(to_create):
            logger.info("Create directory '%s'..", to_create)
            os.makedirs(to_create)
            pathlib.Path(to_create).mkdir(parents=True, exist_ok=True)
        else:
            logger.info("Directory '%s' exist.", to_create)


if __name__ == '__main__':
    files_dir = "/media/funker/3/FOTO/2019/2019-Samsung_S9 (Lena)/"

    files, dirs_to_create = prepare_dirs(path=files_dir)
    create_dirs_if_not_exist(path=files_dir, dirs=dirs_to_create)

    for file in files:
        pass
