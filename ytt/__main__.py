import argparse

import pathlib
import os.path

import warnings

import pytube
import pytube.extract


HOME = pathlib.Path.home()

YTT_CACHE = os.path.join(HOME, ".cache", "ytt")


def mute_whisper_warnings():
    warnings.filterwarnings("ignore")


def ensure_ytt_dir():
    pathlib.Path(YTT_CACHE).mkdir(parents=True, exist_ok=True)


def get_input_url() -> str:
    parser = argparse.ArgumentParser("Get the  script of a video.")

    parser.add_argument("video", help="YouTube Video URL", type=str)

    args = parser.parse_args()

    return args.video


def video_cache(video_id: str, extension: str):
    return os.path.join(YTT_CACHE, f"{video_id}.{extension}")


def transcribe(path: str, model="small") -> str:
    import whisper

    model = whisper.load_model(model)

    result = model.transcribe(path)

    text = result["text"]

    return str(text)


def log_file(file_path: str):
    with open(file_path, "r") as file:
        contents = file.read()

    print(contents)


def save_and_log_file(file_path: str, content: str):
    with open(file_path, "w") as file:
        file.write(content)

    print(content)


def main():
    ensure_ytt_dir()
    mute_whisper_warnings()

    input_url = get_input_url()

    try:
        video_id = pytube.extract.video_id(input_url)
    except pytube.extract.RegexMatchError:
        print("That's not a valid URL!")
        return

    video_text_backup = video_cache(video_id, "txt")

    try:
        log_file(video_text_backup)
    except FileNotFoundError:
        audio_backup_file = video_cache(video_id, "mp3")

        video = pytube.YouTube(input_url)

        audio = video.streams.get_audio_only()

        if not audio:
            return print("The video audio does not have audio.")

        audio.download(filename=audio_backup_file)

        text = transcribe(audio_backup_file)

        save_and_log_file(video_text_backup, text)


main()
