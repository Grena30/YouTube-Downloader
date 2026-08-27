# YouTube video downloader

Python script for downloading YouTube videos, playlists and entire channels using the library [yt-dlp](https://github.com/yt-dlp/yt-dlp).

- Recommended [ffmpeg](https://github.com/FFmpeg/FFmpeg)

## Installation

- Clone the repository.
- Install dependencies `pip install -r requirements.txt`.

## Usage

- Run `python main.py -h` to view all available commands
- Run `python main.py "<URL>"` to download a specific video, playlist, or channel
- Run `python main.py -a` to download audio only
- Run `python main.py "<PLAYLIST-URL>" -a` to download every playlist item as MP3
- Run `python main.py "<CHANNEL-URL>" -a` to download videos from a channel as MP3
- Run `python main.py --file urls.txt -a` to download audio for multiple URLs

Quote YouTube URLs in the shell, especially URLs containing `&`. Otherwise,
Bash treats `&` as a command separator before Python receives the argument:

```bash
python main.py "https://www.youtube.com/watch?v=-yIUzB_CI0Y&list=PLQlreteDLSIU" -a
```

Use `python main.py`, not `python python main.py`. Escaping the ampersand as
`\&` also works, but quoting the complete URL is recommended.

For batch downloads, create a UTF-8 text file with one URL per line. Blank lines
and lines beginning with `#` are ignored:

```text
# Morning playlist
https://www.youtube.com/watch?v=...
https://www.youtube.com/watch?v=...
```

The existing single-URL command remains supported. Use `--file` (or `-f`) instead
of pasting multiple URLs into the terminal.

Playlist and channel URLs are expanded automatically. All converted MP3 files
are placed in the selected output directory. If an individual item is
unavailable, yt-dlp reports it and continues with the remaining items.

## Troubleshooting HTTP 403 errors

YouTube can reject a downloader's signed media request even when a public video
plays normally in a browser. This is usually an anti-bot or client-context check,
not a requirement to authenticate every download. If the video works in Brave,
retry with its browser cookies:

```bash
python main.py "https://www.youtube.com/watch?v=..." -a --cookies-from-browser brave
```

The option can also be used with `--file` and accepts other browser names
supported by yt-dlp. Cookies are sensitive session data; they are read locally
and should never be committed, copied into URL files, or printed in logs. If
cookies do not help, update yt-dlp and retry because YouTube's extractor/client
requirements change frequently.
