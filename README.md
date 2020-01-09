# Convert Video 


## Requirements

- Python 3.7
- brew install hachoir-metadata
- brew install ffmpeg


## Quick start
 
```sh
git clone git@github.com:dstoianov/video-converter.git
cd video-converter/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m video_converter.py
```


## Links

1. [Encoding H.265/HEVC for QuickTime with FFmpeg](https://brandur.org/fragments/ffmpeg-h265)
1. [Using FFmpeg to Create H.265/HEVC Videos That Work on Apple Devices](https://aaronk.me/ffmpeg-hevc-apple-devices/)
1. [19 FFmpeg Commands For All Needs](https://catswhocode.com/ffmpeg-commands/)
1. [Video files taking up too much space? Let's shrink them with FFmpeg!](http://coderunner.io/shrink-videos-with-ffmpeg-and-preserve-metadata/)
1. [H.264 Video Encoding Guide, Choose a preset and tune](https://trac.ffmpeg.org/wiki/Encode/H.264)
1. [H.265 FFmpeg Encoding Guide](https://trac.ffmpeg.org/wiki/Encode/H.265)

### Helpful commands

* convert to `libx264`

```bash
ffmpeg -i "input.mp4" -copy_unknown -map_metadata 0 -map 0 -codec copy \
    -codec:v libx264 -pix_fmt yuv420p -crf 23 \
    -codec:a aac -vbr 6 \
    -preset fast "output.mp4"
```
* convert to `libx265`

```bash
ffmpeg -i "input.mp4" -copy_unknown -map_metadata 0 -map 0 -codec copy \
    -codec:v libx265 -pix_fmt yuv420p -crf 28 \
    -codec:a aac -vbr 6 \
    -tag:v hvc1 -preset fast "output.mp4"
```


* Clear pycache

```shell 
$ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```
