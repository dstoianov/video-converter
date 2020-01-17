#!/bin/bash

#
# script fo sync folders with files
#

#year="2020"
#source="/media/funker/3/FOTO/${year}/" # must ended with '/'
#destination="/media/funker/1.5T/FOTO/${year}" # must ended without '/'

# Folders
source="/media/funker/3/FOTO/" # must ended with '/'
destination="/media/funker/1.5T/FOTO" # must ended without '/'

# folder="2010"
#source="/media/funker/3/FOTO/${folder}/" # must ended with '/'
#destination="funker@192.168.178.100:/media/files/${folder}" # must ended without '/'

#rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST


start_date=$(date '+%Y-%m-%d %H:%M:%S')

echo "[+] Started syncing folders and files at ${start_date}.."
echo "[+] from '${source}'"
echo "[+] to   '${destination}'"

#rsync --help


# -r, --recursive: Browse into sub-directories for additional files.r
# --delete                delete extraneous files from destination dirs
# We can use ‘–delete‘ option to delete files that are not there in source directory.
#  -t, --times   preserve times
# -h Shows the information that rsync provides us in a human readable format, the amounts are given in K's, M's, G's and so on.
# -h, --human-readable        output numbers in a human-readable format

# test run
#sudo rsync --recursive --human-readable --times --verbose --dry-run --progress ${source} ${destination}
#rsync --recursive 'ssh -p 21598' --human-readable --times --verbose --dry-run --delete --progress ${source} ${destination}


#rsync --recursive --human-readable --times --verbose --delete --dry-run --progress \
rsync --recursive --human-readable --times --verbose --delete --dry-run --progress \
        --exclude '.directory' --exclude 'Lightroom/*' ${source} ${destination}

# for sync via ssh
#rsync --recursive --human-readable --times --verbose --delete --dry-run --progress \
#        --exclude '.directory' --exclude 'Lightroom/*' \
#         -e 'ssh -p 21598' ${source} ${destination}

#sudo rsync -aAXv --delete --exclude=/dev/* --exclude=/proc/* --exclude=/sys/* --exclude=/tmp/* \
#    --exclude=/run/* --exclude=/mnt/* --exclude=/media/* --exclude="swapfile" --exclude="lost+found" \
#    --exclude=".cache" --exclude="Downloads" --exclude=".VirtualBoxVMs" --exclude=".ecryptfs" $source $destination

echo "[+] Started at  ${start_date}"
echo "[+] Finished at `date '+%Y-%m-%d %H:%M:%S'`"
