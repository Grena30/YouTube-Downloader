from utils import download_channel, download_playlist, download_video
import argparse
from pathlib import Path


DOWNLOAD_PATH: str = "Downloads\YouTube\\" # Change this to your download path

def main() -> None:
    parser = argparse.ArgumentParser(description="Download videos, audios, playlists, or channels from YouTube.")
    parser.add_argument("url", metavar="\"URL\"", type=str, help="The URL of the video, playlist, or channel to download. Enclose the URL in quotes.")
    parser.add_argument("-a", action="store_true", help="Download audio only.")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", action="store_true", help="Download video.")
    group.add_argument("-p", action="store_true", help="Download a playlist.")
    group.add_argument("-c", action="store_true", help="Download all videos from a channel.")
    
    args = parser.parse_args()
    
    try:
        Path(DOWNLOAD_PATH).mkdir(parents=True)
    except FileExistsError:
        print("Directory already exists")
    
    if DOWNLOAD_PATH == "Downloads\YouTube\\":
        print(f"Videos will be downloaded to default path {DOWNLOAD_PATH}.")
        
    if args.u:
        download_video(args.url, path=DOWNLOAD_PATH, audio_only=args.a)
    elif args.p:
        download_playlist(args.url, path=DOWNLOAD_PATH, audio_only=args.a)
    elif args.c:
        download_channel(args.url, path=DOWNLOAD_PATH, audio_only=args.a)
    else:
        print("Invalid combination of arguments.")
        
if __name__ == "__main__":  
    main()