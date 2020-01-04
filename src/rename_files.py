import os

files_dir = "/media/funker/3/FOTO/"


# Function to rename multiple files
def main():
    for filename in os.listdir(files_dir):
        if "download_" in filename:
            new_name = filename.replace("download_", "")
            src = files_dir + filename
            dst = files_dir + new_name
            print("Rename '{}' to '{}'".format(filename, new_name))
            # rename() function will
            # rename all the files
            os.rename(src, dst)


if __name__ == '__main__':
    main()
