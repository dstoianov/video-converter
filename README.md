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
python -m pytest
```


## Links

1. [19 FFmpeg Commands For All Needs](https://catswhocode.com/ffmpeg-commands/)
1. [Video files taking up too much space? Let's shrink them with FFmpeg!](http://coderunner.io/shrink-videos-with-ffmpeg-and-preserve-metadata/)
        

### Helpful commands

* convert files

```bash
ffmpeg -i "input.mp4" -copy_unknown -map_metadata 0 -map 0 -codec copy \
    -codec:v libx264 -pix_fmt yuv420p -crf 23 \
    -codec:a libfdk_aac -vbr 4 \
    -preset fast "output.mp4"
```

* Clear pycache

```shell 
$ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```
