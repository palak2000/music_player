from tkinter import *
root = Tk()

playPhoto = PhotoImage(file='play-button.png')
playBtn = Button(root, image=playPhoto)
playBtn.grid(row=0, column=0)

pausePhoto = PhotoImage(file='pause_button.png')
pauseBtn = Button(root, image=pausePhoto)
pauseBtn.grid(row=0, column=1)

stopPhoto = PhotoImage(file='stop_button.png')
stopBtn = Button(root, image=stopPhoto)
stopBtn.grid(row=1, column=0)

root.mainloop()
