from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
import os
import re
import inquirer
import sys


def main():
    general_path = ""  # change as you like
    inputLink = input("please enter the link: ")
    strLink = str(inputLink)
    link = f"{strLink}"
    yt = YouTube(link, on_progress_callback=on_progress)
    name = yt.title
    print(name)
    media_type = [inquirer.List(
        "extension", message="chooose media_type", choices=["audio only", "video only"])]
    media_ask = inquirer.prompt(media_type)
    media_extension = media_ask["extension"]

        

    if media_extension == "audio only":
        def download_aud(st, path):
            audio = st.streams.filter(
                mime_type="audio/mp4").order_by('abr').last()
            print(audio)
            audio.download(path)
        download_aud(yt, general_path)
    if media_extension == "video only":
        resolution_survey = [inquirer.List("quality",   message="what quality do you want",
                                           choices=['240', '360', '480',
                                                    '720', '1080', '2160'])]
        resolution_ask = inquirer.prompt(resolution_survey)
        resolution = resolution_ask["quality"]
        fps_survey = [inquirer.List("fps",   message="what fps do you want",
                                    choices=['high', 'low'])]
        fps_answer = inquirer.prompt(fps_survey)
        fps_count = fps_answer["fps"]

        def download_vid(res, st, path):

            if fps_count == "low":
                stream = st.streams.filter(
                    res=f"{res}p", mime_type="video/mp4").order_by('fps').first()
                print(stream)
                stream.download(path)
            if fps_count == "high":
                stream = st.streams.filter(
                    res=f"{res}p", mime_type="video/webm").order_by('fps').last()
                print(stream)
                stream.download(path)

        download_vid(resolution, yt, general_path)


if __name__ == "__main__":
    main()
    sys.exit("thank you for using the app\n")
