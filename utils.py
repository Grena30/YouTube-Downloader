import yt_dlp
import shutil

from pathlib import Path


class YouTubeDownloader:
    def __init__(
        self,
        download_path: Path,
        audio_only: bool = False,
        max_resolution: str = "best",
        cookies_from_browser: str | None = None,
    ):
        self.download_path = download_path
        self.audio_only = audio_only
        self.max_resolution = max_resolution
        self.cookies_from_browser = cookies_from_browser
        self.ffmpeg_available = self._is_ffmpeg_available()

        if not self.ffmpeg_available and not self.audio_only:
            print(
                "Warning: FFmpeg is not detected in your system PATH. Videos may be limited to lower resolutions."
            )

    def _is_ffmpeg_available(self) -> bool:
        return shutil.which("ffmpeg") is not None

    def download(self, url: str) -> None:
        ydl_opts = {
            "outtmpl": str(self.download_path / "%(title)s.%(ext)s"),
            "noplaylist": False,
            "ignoreerrors": "only_download",
            "quiet": False,
        }

        if self.cookies_from_browser:
            ydl_opts["cookiesfrombrowser"] = (self.cookies_from_browser,)

        if self.audio_only:
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )
        else:
            if self.max_resolution == "best":
                video_format = (
                    "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
                )
            else:
                video_format = f"bestvideo[height<={self.max_resolution}][ext=mp4]+bestaudio[ext=m4a]/best[height<={self.max_resolution}][ext=mp4]/best"

            ydl_opts.update(
                {
                    "format": video_format,
                    "merge_output_format": "mp4",
                }
            )

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Fetching data for: {url}")
                ydl.download([url])
            print("\nDownload processing finished. Review yt-dlp output for skipped items.")

        except Exception as e:
            message = str(e)
            if "HTTP Error 403" in message:
                message += (
                    "\nA 403 usually means YouTube rejected the media request. "
                    "Try updating yt-dlp or retry with "
                    f"--cookies-from-browser {self.cookies_from_browser or 'brave'} "
                    "if the video plays in that browser."
                )
            print(f"\nAn error occurred during download: {message}")
