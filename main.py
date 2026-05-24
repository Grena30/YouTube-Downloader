import argparse

from pathlib import Path
from utils import YouTubeDownloader

DEFAULT_DOWNLOAD_PATH = Path.home() / "Downloads" / "YouTube"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A robust YouTube downloader using yt-dlp."
    )

    parser.add_argument(
        "url",
        metavar="URL",
        type=str,
        help="The URL of the video, playlist, or channel to download.",
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

    args = parser.parse_args()

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
    )
    downloader.download(args.url)


if __name__ == "__main__":
    main()
