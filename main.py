import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
import time
import threading

from pygame import mixer

root = Tk()

statusbar = Label(root, text=' welcome to MusicPlayer ', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the submenu
subMenu = Menu(menubar, tearoff=0)

playlist = []


# playlist = contain full path + filename
# playlistbox = contain filename
# full path +filename is required to play the music inside play_music load func

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    Playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About musicplayer', 'This is the MusicPlayer built by Palak jain.')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()
root.geometry('300x300')
root.title('Melody')
root.iconbitmap(r'images/headphones.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30)

Playlistbox = Listbox(leftframe)
Playlistbox.pack()

addbtn = Button(leftframe, text="+ Add", command=browse_file)
addbtn.pack(side=LEFT)


def del_song():
    selected_song = Playlistbox.curselection()
    selected_song = int(selected_song[0])
    Playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delbtn = Button(leftframe, text="- Del", command=del_song)
delbtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

filelabel = Label(topframe, text='lets make some noise!!')
filelabel.pack()

lengthlabel = Label(topframe, text='Total length :--:--')
lengthlabel.pack(pady=5)

currenttimelabel = Label(topframe, text='Current Time :--:--', relief=GROOVE)
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{02d}'.format(mins, secs)
    lengthlabel['text'] = 'Total Length' + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy() - returns False when we press the stop button (music stop playing)
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{02d}'.format(mins, secs)
            currenttimelabel['text'] = 'Current Time' + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = 'Music Resumed'
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = Playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = 'Playing Music' + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'MusicPlayer could not found the file. Please check again.')


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = 'Music paused'


def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'Music Stopped'


def rewind_music():
    play_music()
    statusbar['text'] = 'Music Rewinded'


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. example-0.5,0.2


muted = FALSE


def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


# middleFrame

middleframe = Frame(rightframe, relief=RAISED, borderwidth=1)
middleframe.pack(pady=10)

playPhoto = PhotoImage(file='images/play-button.png')
playBtn = Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

pausePhoto = PhotoImage(file='images/pause_button.png')
pauseBtn = Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=1, padx=10)

stopPhoto = PhotoImage(file='images/stop_button.png')
stopBtn = Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)

# BottomFrame

bottomframe = Frame(rightframe)
bottomframe.pack()

rewindPhoto = PhotoImage(file='images/rewind_button.png')
rewindBtn = Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)

scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
# mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
