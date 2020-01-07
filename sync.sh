#!/bin/bash

#
# script fo sync folders with files
#

source="/home/dddd"
destination="/home/dddd"

echo "[+] Started syncing folders and files at `date '+%Y-%m-%d %H:%M:%S'`.."
echo "[+] from '${source}'"
echo "[+] to   '${destination}'"

rsync --help


# -r, --recursive: Browse into sub-directories for additional files.r
# --delete                delete extraneous files from destination dirs
# We can use ‘–delete‘ option to delete files that are not there in source directory.
#  -t, --times                 preserve times
# -h Shows the information that rsync provides us in a human readable format, the amounts are given in K's, M's, G's and so on.
# -h, --human-readable        output numbers in a human-readable format

# test run
#sudo rsync --recursive --human-readable --times --verbose --dry-run --progress ${source} ${destination}

#sudo rsync -aAXv --delete --exclude=/dev/* --exclude=/proc/* --exclude=/sys/* --exclude=/tmp/* \
#    --exclude=/run/* --exclude=/mnt/* --exclude=/media/* --exclude="swapfile" --exclude="lost+found" \
#    --exclude=".cache" --exclude="Downloads" --exclude=".VirtualBoxVMs" --exclude=".ecryptfs" $source $destination

echo "[+] Done at `date '+%Y-%m-%d %H:%M:%S'`"
