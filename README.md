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

Clear pycache

```shell 
$ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
```




