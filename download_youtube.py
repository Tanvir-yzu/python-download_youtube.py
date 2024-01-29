import os
import tkinter as tk
from pytube import YouTube
from tqdm import tqdm
from urllib.error import URLError

def get_valid_stream(video):
    while True:
        try:
            stream_num = int(entry.get())
            if 1 <= stream_num <= len(video.streams):
                break
            else:
                result_label.config(text="Invalid stream number, please try again", fg="red")
        except ValueError:
            result_label.config(text="Invalid input, please enter a number", fg="red")

    return stream_num

def download_stream(stream):
    filename = stream.default_filename

    if os.path.exists(filename):
        result_label.config(text=f"{filename} already exists. Overwrite? (y/n)", fg="blue")
        if input().lower() != "y":
            return

    try:
        with tqdm(total=stream.filesize, unit='B', unit_scale=True) as progress_bar:
            stream.download(output_path="downloads", filename=filename, callback=lambda d, t: progress_bar.update(d))
    except KeyboardInterrupt:
        result_label.config(text="Download interrupted", fg="red")
    except:
        result_label.config(text="Network error encountered", fg="red")
    finally:
        progress_bar.close()

    if os.path.getsize(filename) != stream.filesize:
        result_label.config(text="Incomplete download", fg="red")
    else:
        result_label.config(text=f"Downloaded {filename} successfully!", fg="green")

def download_video():
    url = entry_url.get()
    try:
        video = YouTube(url)
    except URLError:
        result_label.config(text="Invalid YouTube URL", fg="red")
        return

    if video.age_restricted:
        result_label.config(text="Video is age restricted, cannot download", fg="red")
        return

    result_label.config(text="Available streams:", fg="blue")
    for i, stream in enumerate(video.streams.filter(progressive=True).order_by("resolution").desc()):
        result_label.config(text=f"{i + 1}: {stream.resolution} {stream.fps}fps", fg="blue")
    
    stream_num = get_valid_stream(video.streams)
    stream = video.streams.order_by("resolution").desc()[stream_num - 1]

    download_stream(stream)

# GUI setup
root = tk.Tk()
root.title("YouTube Video Downloader")

# Entry for YouTube URL
label_url = tk.Label(root, text="Enter YouTube URL:")
label_url.pack(pady=10)
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=10)

# Button to start download
button_download = tk.Button(root, text="Download Video", command=download_video)
button_download.pack(pady=20)

# Label for displaying download result
result_label = tk.Label(root, text="", fg="black")
result_label.pack()

# Run the GUI
root.mainloop()
