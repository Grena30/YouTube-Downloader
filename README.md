# YouTube video downloader

Python script for downloading YouTube videos, playlists and entire channels using the library [pytubefix](https://github.com/JuanBindez/pytubefix). Without [ffmpeg](https://github.com/FFmpeg/FFmpeg) the maximum resolution for videos seems to be around 360p and the process is faster.

## Installation

- Clone the repository. 
- Install ffmpeg (Optional)
- Install dependencies `pip install pytubefix`.

## Usage

- Run `python main.py -h` to view all available commands
- Run `python main.py -u <URL>` to download a specific video
- Run `python main.py -a [OPTIONS] <URL>` to download audio only version 