#!/usr/bin/env bash


mkdir decoded/

for i in *.mp4
do
	new_file_name="`basename $i .mp4`_decoded.mp4"
	echo "New file name is [$new_file_name]"

	ffmpeg -i $i -vcodec h264 -acodec aac -strict -2 decoded/$new_file_name
	echo "Done."
done

ls -all


