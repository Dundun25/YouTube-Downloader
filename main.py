import tkinter as tk
from tkinter import ttk
import requests as rq
from tkinter import filedialog
import tkinter.font as tkfont
import pytube as pt
from PIL import ImageTk, Image

yt_video = None


# https://www.youtube.com/watch?v=H9154xIoYTA (example link)
# Function
def search():
    global yt_video, preview_img, canvas, cmbbox_reschoice
    yt_video = pt.YouTube(ent_url.get())
    lbl_preview.config(text=str(yt_video.title))
    # set preview image
    response = rq.get(yt_video.thumbnail_url)
    image = open("img/preview_new.jpg", "wb")
    image.write(response.content)
    image.close()
    preview_img = ImageTk.PhotoImage((Image.open("img/preview_new.jpg")).resize((600, 300), Image.ANTIALIAS))
    canvas = tk.Label(master=frm_preview, image=preview_img)
    canvas.grid(row=0, column=0, sticky="news")
    # set available resolution
    res_choices = list(set([str(i.resolution) for i in yt_video.streams]))
    try:
        res_choices.remove("None")
    except ValueError:
        pass
    cmbbox_reschoice["values"] = res_choices
    cmbbox_reschoice.current(0)


def download():
    global yt_video, cmbbox_reschoice
    if not yt_video:
        return
    path_name = filedialog.askdirectory(title="Select Save as Folder")
    if not path_name:
        return
    video = yt_video.streams.filter(res=cmbbox_reschoice.get()).first()
    video.download(path_name)

# Gui
window = tk.Tk()
window.title("Youtube Video Downloader")
window.resizable(width=False, height=False)
# Url input Frame Config
frm_url = tk.Frame(master=window, bg="#3b3b3b")
frm_url.grid(row=0, column=0, sticky="news", ipady=5)
# Preview Frame Config
frm_preview = tk.Frame(master=window, relief="sunken", borderwidth=2, bg="#3b3b3b")
frm_preview.grid(row=1, column=0, sticky="news")
cnv_preview = tk.Canvas(master=frm_preview, bg="#3b3b3b")
cnv_preview.grid(row=0, column=0, sticky="news")

# Url Frame Children
fontstyle = tkfont.Font(family="Lucida Grande", size=10)
lbl_url = tk.Label(master=frm_url, text="Link :", bg="#3b3b3b",
                   fg="white", font=fontstyle)
ent_url = tk.Entry(master=frm_url, relief="sunken", borderwidth=2, text="",
                   bg="#858383", fg="white", width=35, font=fontstyle)
btn_search = tk.Button(master=frm_url, text="Search", bg="#525252",
                       fg="white", relief="raised", borderwidth=1, font=fontstyle, command=search)
btn_download = tk.Button(master=frm_url, text="Download", relief="raised",
                         borderwidth=1, bg="#525252", fg="white", font=fontstyle, command=download)
# choice list box
lbl_list = tk.Label(master=frm_url, text="Select Res:", bg="#3b3b3b", fg="white")
cmbbox_reschoice = ttk.Combobox(master=frm_url, textvariable=tk.StringVar())
cmbbox_reschoice["state"] = "readonly"

# render url frame
lbl_url.grid(row=0, column=0, padx=3, sticky="e")
ent_url.grid(row=0, column=1, padx=2, sticky="s")
btn_search.grid(row=0, column=2, sticky="w", padx=5)
btn_download.grid(row=0, column=3, sticky="e")
lbl_list.grid(row=1, column=0, sticky="e")
cmbbox_reschoice.grid(row=1, column=1, sticky="w", padx=3, pady=5)

# Preview Frame Image
preview_img = ImageTk.PhotoImage((Image.open("img/preview.jpg")).resize((600, 300), Image.ANTIALIAS))
canvas = tk.Label(master=frm_preview, image=preview_img)
canvas.grid(row=0, column=0, sticky="news")
# label preview
lbl_preview = tk.Label(master=frm_preview, text="Preview", bg="#3b3b3b", fg="white", font=fontstyle)
lbl_preview.grid(row=1, column=0, sticky="news")

window.mainloop()
