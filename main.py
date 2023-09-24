from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
import os
import re
import inquirer
import sys


def main():
    general_path = "/Users/ahmedatef/Movies"  # change as you like
    inputLink = input("please enter the link: ")
    strLink = str(inputLink)
    link = f"{strLink}"
    yt = YouTube(link, on_progress_callback=on_progress)
    name = yt.title
    print(name)
    media_type = [inquirer.List(
        "extension", message="chooose media_type", choices=["audio only", "video only", "full mp4"])]
    media_ask = inquirer.prompt(media_type)
    media_extension = media_ask["extension"]
    if media_extension == "full mp4":
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
                    res=f"{res}p", mime_type="video/mp4").order_by('fps').last()
                print(stream)
                stream.download(path)

        download_vid(resolution, yt, general_path)

        def download_aud(st, path):
            audio = st.streams.filter(
                type="audio").order_by('abr').last()
            print(audio)
            audio.download(path)
        download_aud(yt, general_path)

        def multiple_replace(string, rep_dict):
            pattern = re.compile("|".join([re.escape(k) for k in sorted(
                rep_dict, key=len, reverse=True)]), flags=re.DOTALL)
            return pattern.sub(lambda x: rep_dict[x.group(0)], string)

        def concat(y, folderPath):
            x = multiple_replace(y, {".": "", "/": "", "'": "", "|": ""})
            print(x)
            vidfilePath = f"{x}.mp4"
            audfilepath = f"{x}.webm"
            mergedfilepath = f"{x}merged.mp4"
            vid_path = os.path.join(folderPath, vidfilePath)
            aud_path = os.path.join(folderPath, audfilepath)
            merged_path = os.path.join(folderPath, mergedfilepath)

            input_video = ffmpeg.input(vid_path)

            input_audio = ffmpeg.input(aud_path)

            ffmpeg.concat(input_video, input_audio, v=1, a=1).output(
                merged_path).run(overwrite_output=True)

            def remove():
                os.remove(vid_path)
                os.remove(aud_path)
            remove()
        concat(name, general_path)
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
