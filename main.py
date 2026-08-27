import argparse

from pathlib import Path
from utils import YouTubeDownloader

DEFAULT_DOWNLOAD_PATH = Path.home() / "Downloads" / "YouTube"


def read_urls_from_file(url_file: Path) -> list[str]:
    try:
        lines = url_file.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValueError(f"Could not read URL file '{url_file}': {error}") from error

    urls = [
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not urls:
        raise ValueError(f"URL file '{url_file}' does not contain any URLs.")
    return urls


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A robust YouTube downloader using yt-dlp."
    )

    parser.add_argument(
        "url",
        metavar="URL",
        type=str,
        nargs="?",
        help="The URL of the video, playlist, or channel to download.",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="url_file",
        type=Path,
        help="Read one URL per line from a UTF-8 text file.",
    )

    parser.add_argument(
        "-a",
        "--audio",
        action="store_true",
        help="Download audio only (converted to MP3).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=str(DEFAULT_DOWNLOAD_PATH),
        help=f"Output directory path. (Default: {DEFAULT_DOWNLOAD_PATH})",
    )

    parser.add_argument(
        "-r",
        "--resolution",
        type=str,
        default="best",
        choices=["best", "2160", "1440", "1080", "720", "480", "360"],
        help="Set a maximum resolution height (e.g., 1080, 720). Default is 'best'.",
    )
    parser.add_argument(
        "--cookies-from-browser",
        metavar="BROWSER",
        help="Read YouTube cookies from a browser (for example: brave or chrome).",
    )

    args = parser.parse_args()

    if bool(args.url) == bool(args.url_file):
        parser.error("provide exactly one of URL or --file")

    try:
        urls = [args.url] if args.url else read_urls_from_file(args.url_file)
    except ValueError as error:
        parser.error(str(error))

    download_path = Path(args.output)
    download_path.mkdir(parents=True, exist_ok=True)

    print(f"Initializing download...")
    print(f"Destination: {download_path}")

    if args.audio:
        print("Mode: Audio Only")
    else:
        print(
            f"Max Resolution: {args.resolution if args.resolution != 'best' else 'Uncapped (Highest available)'}"
        )

    downloader = YouTubeDownloader(
        download_path=download_path,
        audio_only=args.audio,
        max_resolution=args.resolution,
        cookies_from_browser=args.cookies_from_browser,
    )
    for url in urls:
        downloader.download(url)


if __name__ == "__main__":
    main()
