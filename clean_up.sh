#!/bin/bash


start_date=$(date '+%Y-%m-%d %H:%M:%S')
folder=`pwd`

echo "[+] Started cleaning up folders and files at ${start_date}.."
echo "[+] current folder '${folder}'"

#find . -name .idea -type d -exec rm -r {} ';'
#find -type d -name ".idea" -exec  rm -rf {} +
#find -type d -name ".venv" -exec  rm -rf {} +
#find -type d -name "target" -exec  rm -rf {} +

find -type d -name "__MACOSX" -exec  rm -rf {} +
find . -name '._*' -delete
find . -name .DS_Store -delete


rm -rf `find -type d -name venv`
echo -ne "."

rm -rf `find -type d -name env`
echo -ne "."

rm -rf `find -type d -name .venv`
echo -ne "."

rm -rf `find -type d -name .env`
echo -ne "."

rm -rf `find -type d -name .idea`
echo -ne "."

rm -rf `find -type d -name target`
echo -ne "."
echo " "

echo "[+] Started at  ${start_date}"
echo "[+] Finished at `date '+%Y-%m-%d %H:%M:%S'`"

echo "[+] 👌 Awesome, all mac files deleted"
