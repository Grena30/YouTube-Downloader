from pytubefix import YouTube, Playlist, Channel
from pytubefix.cli import on_progress
import ffmpeg
import os


def _download_streams(yt, path: str, audio_only: bool) -> None:
    if audio_only:
        ys = yt.streams
        ys = ys.get_audio_only()
        ys.download(output_path=path, mp3=True)
    else:
        try:  
            ys = yt.streams
            video_stream = ys.filter(res='1080p', progressive=False).first()
            audio_stream = ys.filter(progressive=False).first()
            video_stream.download(filename='temp_video.mp4')
            audio_stream.download(filename='temp_audio.mp3')
            audio = ffmpeg.input('temp_audio.mp3')
            video = ffmpeg.input('temp_video.mp4')
            filename = os.path.join(path, yt.title + '.mp4')
            ffmpeg.output(audio, video, filename).run(overwrite_output=True)
            os.remove('temp_video.mp4')
            os.remove('temp_audio.mp3')
        except:
            print("Failed")
            ys = yt.streams
            ys = ys.get_highest_resolution()
            ys.download(output_path=path)
        
         
def download_video(url: str, path: str, audio_only: bool = False) -> None:
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)
        _download_streams(yt, path, audio_only)
    except Exception as e:
        print(f"Error downloading video: {e}")

def download_playlist(url: str, path: str, audio_only: bool = False) -> None:
    try:
        pl = Playlist(url)
        print(f'Playlist name: {pl.title}')
        
        video_count = len(pl.videos)
        print(f'Downloading... {video_count} videos found')
        
        for video in pl.videos:
            print(f'{video.title}, left: {video_count}')
            try:
                _download_streams(video, path, audio_only)
            except Exception as e:
                print(f"Error downloading video {video.title}: {e}")
            video_count -= 1
    except Exception as e:
        print(f"Error processing playlist: {e}")

def download_channel(url: str, path: str, audio_only: bool = False) -> None:
    try:
        ch = Channel(url)
        print(f'Channel name: {ch.channel_name}')
        
        video_count = len(ch.videos)
        print(f'Downloading... {video_count} videos found')
        
        for video in ch.videos:
            print(f'{video.title}, left: {video_count}')
            try:
                _download_streams(video, path, audio_only)
            except Exception as e:
                print(f"Error downloading video {video.title}: {e}")
            video_count -= 1
    except Exception as e:
        print(f"Error processing channel: {e}")
