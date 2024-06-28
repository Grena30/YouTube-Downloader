from pytubefix import YouTube, Playlist, Channel
from pytubefix.cli import on_progress
import os
import subprocess


def _download_streams(yt, path: str, audio_only: bool) -> None:
    if audio_only:
        ys = yt.streams
        ys = ys.get_audio_only()
        ys.download(output_path=path, mp3=True)
    else:
        try:
            print("Using ffmpeg method to merge audio and video streams")
            ys = yt.streams
            video_stream = ys.filter(res='1080p', progressive=False).first()
            audio_stream = ys.get_audio_only()
            video_stream.download(filename=f"{yt.title}_video.mp4", output_path=path)
            audio_stream.download(filename=f"{yt.title}_audio", output_path=path, mp3=True)
            filename = os.path.join(path, yt.title + '.mp4')
            
            ffmpeg_command = [
                'ffmpeg',
                '-i', f'{path}{yt.title}_video.mp4',
                '-i', f'{path}{yt.title}_audio.mp3',
                '-c:v', 'copy',
                '-c:a', 'aac',
                filename
            ]
            subprocess.run(ffmpeg_command, check=True)
                
            os.remove(f'{path}{yt.title}_video.mp4')
            os.remove(f'{path}{yt.title}_audio.mp3')
        except:
            print("Using default method to download streams")
            ys = yt.streams
            ys = ys.get_highest_resolution()
            ys.download(output_path=path)
        
         
def download_video(url: str, path: str, audio_only: bool = False) -> None:
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"YouTube title: {yt.title}")
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
