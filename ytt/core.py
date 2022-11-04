import argparse
import os
from pathlib import Path
import sys
import warnings

import pytube
from pytube import extract
import whisper

warnings.filterwarnings("ignore")

YTT_CACHE = os.path.join(Path.home(), ".cache", "ytt")

Path(YTT_CACHE).mkdir(parents=True, exist_ok=True)


def get_video_url() -> str:
    """
    Get Arguments
    """
    parser = argparse.ArgumentParser("Get the  script of a video.")

    parser.add_argument("video", help="YouTube Video URL", type=str)

    args = parser.parse_args()

    return args.video


video_url = get_video_url()

video_id = extract.video_id(video_url)

video_text = os.path.join(YTT_CACHE, f"{video_id}.txt")

try:
    with open(video_text) as file:
        contents = file.read()

        print(contents)
except FileNotFoundError:
    video_file = os.path.join(YTT_CACHE, f"{video_id}.mp4")

    yt_video = pytube.YouTube(video_url)

    audio = yt_video.streams.get_audio_only()

    if not audio:
        sys.exit(1)

    audio.download(filename=video_file)

    model = whisper.load_model("small")

    result = model.transcribe(video_file)

    text = result["text"]

    with open(video_text, "w") as file:
        file.write(str(text))

    print(text)
