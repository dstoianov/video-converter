#!/bin/bash

#
# script fo sync folders with files
#

source="/media/funker/3/FOTO/2011/"
destination="/media/funker/1.5T/FOTO/2011"

#source="/media/funker/3/FOTO/2016/"
#destination="/media/funker/1.5T/FOTO/2016"

start_date=$(date '+%Y-%m-%d %H:%M:%S')

echo "[+] Started syncing folders and files at ${start_date}.."
echo "[+] from '${source}'"
echo "[+] to   '${destination}'"

#rsync --help


# -r, --recursive: Browse into sub-directories for additional files.r
# --delete                delete extraneous files from destination dirs
# We can use ‘–delete‘ option to delete files that are not there in source directory.
#  -t, --times                 preserve times
# -h Shows the information that rsync provides us in a human readable format, the amounts are given in K's, M's, G's and so on.
# -h, --human-readable        output numbers in a human-readable format

# test run
#sudo rsync --recursive --human-readable --times --verbose --dry-run --progress ${source} ${destination}
rsync --recursive --human-readable --times --verbose --dry-run --delete --progress ${source} ${destination}

#sudo rsync -aAXv --delete --exclude=/dev/* --exclude=/proc/* --exclude=/sys/* --exclude=/tmp/* \
#    --exclude=/run/* --exclude=/mnt/* --exclude=/media/* --exclude="swapfile" --exclude="lost+found" \
#    --exclude=".cache" --exclude="Downloads" --exclude=".VirtualBoxVMs" --exclude=".ecryptfs" $source $destination

echo "[+] Started at  ${start_date}"
echo "[+] Finished at `date '+%Y-%m-%d %H:%M:%S'`"
