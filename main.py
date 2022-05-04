#Import Required modules
import sys
import pygame
pygame.init()
from tkinter import*
import os
import tkinter as tk
from PIL import Image
import random
import threading
import time
from mutagen.mp3 import MP3
import datetime
os.system("cls")
from tkinter import messagebox
#Create instance of a Tk() Class
root = Tk()
#Set title of the window
root.title("MP3 Player -Bidhan, Inc")
#make it unresizable i.e. users cannot maximize or e=restore window
root.resizable(0,0)
#Set window width and height
window_width = 480
window_height = 350
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
#Set icon of a window
root.iconbitmap("other\\icon.ico")
#Get current loggedin username
username = (os.path.split(os.path.expanduser('~'))[-1])
#This a folder from which music is played
musicFolder = f"C:\\Users\\{username}\\Music\\"
myList = os.listdir(musicFolder)
#Put all the collected music in a list
musicList = []
#Check whether the files in the folder are in .mp2 format or not
for music in os.listdir(musicFolder):
        if music.endswith(".mp3"):
            #Put only .mp3 files in the list created before
            musicList.append(music)
#check whether the music list contains .mp3 files or not, if the folder contains .mp3 files, ignore this line or
#show a dialog box and exit
if len(musicList) == 0:
    messagebox.showinfo("No files to play!", f"MP3 files not found in {musicFolder}\nAdd some music in this folder to play.")
    sys.exit()
#Function to select random music from list and play music
def play():
    check_song_details_thread()
    global song
    song = random.choice(musicList)
    mnLabel.config(text=f"Playing: {song[:-4]}")
    audio = MP3(f"{musicFolder}{song}")
    audio_info = audio.info
    length = int(audio_info.length)
    hours, mins, seconds = audio_duration(length)
    if len(str(hours)) == 1:
        hours = "0"+str(hours)
    if len(str(mins)) == 1:
        mins = "0"+str(mins)
    if len(str(seconds)) == 1:
        seconds = "0"+str(seconds)
    a_d_Label.config(text=f"{hours}:{mins}:{seconds}")
    pygame.mixer.music.load(f"{musicFolder}{song}")
    pygame.mixer.music.play()
#Function to pause music
def pause():
    global checking
    checking = False
    ppBtn.config(text="▶", command=unpause)
    pygame.mixer.music.pause()
    mnLabel.config(text=f"Paused: {song}")
    stop_animation()
#function to unpause music
def unpause():
    ppBtn.config(text="⏸", command=pause)
    pygame.mixer.music.unpause()
    mnLabel.config(text=f"Playing: {song}")
    global checking
    checking = True
    check_thread()
    change_color_thread()
    count = 0
    global anim
    anim = None
    animation(count)
#function to stop playing music
def stop_music():
    global checking
    checking = False
    stBtn.config(text="⏺", command=unstop_music)
    stop_animation()
    pygame.mixer.music.stop()
    mnLabel.config(text=f"Stopped: {song}")
    pygame.mixer.music.unload()
#function to play music again
def unstop_music():
    global checking
    checking = True
    stBtn.config(text="⏹", command=stop_music)
    check_thread()
    change_color_thread() 
    mnLabel.config(text=f"Playing: {song}")
    count = 0
    global anim
    anim = None
    animation(count)
#Creating boolean variables for while loops
global checking
checking = True
#Check whether the music is playing or not
def check():
    while checking:
        if not pygame.mixer.music.get_busy():
            play()
        elif pygame.mixer.music.get_busy():
            pass
        time.sleep(1)
#show a directory selection window
def settings_window():
    h_w = Toplevel()
    window_width = 300
    window_height = 200
    h_w.resizable(0,0)
    h_w.title("MP3 Player Settings")
    screen_width = h_w.winfo_screenwidth()
    screen_height = h_w.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    h_w.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
#load music gif
file="other\\music.gif"
info = Image.open(file)
frames = info.n_frames
im = [tk.PhotoImage(file=file,format=f"gif -index {i}") for i in range(frames)]
count = 0
anim = None
#show gif animation
def animation(count):
    global anim
    im2 = im[count]
    gif_label.configure(image=im2)
    count += 1
    if count == frames:
        count = 0
    anim = root.after(120,lambda :animation(count))
#function stop gif animation
def stop_animation():
    root.after_cancel(anim)
#function to exit app
def exit_app():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    global c_d
    c_d = False
    global checking
    checking = False
    root.destroy()
#show gif in tkinter label
gif_label = tk.Label(root,image="")
gif_label.pack()
#create a frame for buttons and other details
btnFrame = LabelFrame(root, bd=0, bg="black")
btnFrame.place(x=0,y=231,width=480,height=119)
#label to show hint when hovering over buttons
hLabel = Label(btnFrame,font=("arial", 10), bg="black")
hLabel.place(relx=0.70, rely=0.90, anchor=SW)
#Label to show name of the music
mnLabel = Label(btnFrame, font=("arial", 10), bg="black")
mnLabel.place(relx=0.50, rely=0.10, anchor=N)
#button to play next music
nBtn = Button(btnFrame, cursor="hand2", text="⏩", bd=0,command=play, bg="black",
                activebackground="black", activeforeground="green", font=("arial",15))
nBtn.place(relx=0.30, rely=0.50, anchor=W)
def nBtnE(e):
    hLabel.config(text="Next Song")
def nBtnL(e):
    hLabel.config(text="")
nBtn.bind("<Enter>", nBtnE)
nBtn.bind("<Leave>", nBtnL)
#Button to pause or play music
ppBtn = Button(btnFrame, cursor="hand2", text="⏸", bd=0,command=pause, bg="black",
                activebackground="black", activeforeground="yellow", font=("arial",15))
ppBtn.place(relx=0.40, rely=0.50, anchor=W)
def ppBtnE(e):
    hLabel.config(text="Play/Pause")
def ppBtnL(e):
    hLabel.config(text="")
ppBtn.bind("<Enter>", ppBtnE)
ppBtn.bind("<Leave>", ppBtnL)
#button to stop or play music
stBtn = Button(btnFrame, cursor="hand2", text="⏹", bd=0,command=stop_music, bg="black",
                activebackground="black", activeforeground="blue", font=("arial",15))
stBtn.place(relx=0.50, rely=0.50, anchor=W)
def stBtnE(e):
    hLabel.config(text="Stop/Play")
def stBtnL(e):
    hLabel.config(text="")
stBtn.bind("<Enter>", stBtnE)
stBtn.bind("<Leave>", stBtnL)
#Button to exit app
exBtn = Button(btnFrame, cursor="hand2", text="❎", bd=0,command=exit_app, bg="black",
                activebackground="black", activeforeground="red", font=("arial",15))
exBtn.place(relx=0.60, rely=0.50, anchor=W)
def exBtnE(e):
    hLabel.config(text="Stop and Exit")
def exBtnL(e):
    hLabel.config(text="")
exBtn.bind("<Enter>", exBtnE)
exBtn.bind("<Leave>", exBtnL)
#Label to show audio duration of current music
a_d_Label = Label(btnFrame, font=("arial", 10), bg="black")
a_d_Label.place(relx=0.50, rely=0.90, anchor=SE)
#label to show the current position of the music
a_c_d_Label = Label(btnFrame, font=("arial", 10), bg="black")
a_c_d_Label.place(relx=0.50, rely=0.90, anchor=SW)
#Calling gif animation function
animation(count)
#thread to check current music details
def check_song_details_thread():
    threading.Thread(target=check_song_details).start()
#Creating boolean variables for while loops
global c_d
c_d = True
def check_song_details():
    while c_d:
        a_c_d_Label.config(text=f"{datetime.timedelta(seconds=round(int(pygame.mixer.music.get_pos())/1000))}")
        time.sleep(1)
#function to change color of the widgets like buttons, labels
def change_colors():
    while checking:
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        rgb = (red, green, blue)
        color = "#%02x%02x%02x" % rgb
        mnLabel.config(fg=color)
        a_c_d_Label.config(fg=color)
        a_d_Label.config(fg=color)
        nBtn.config(fg=color)
        ppBtn.config(fg=color)
        stBtn.config(fg=color)
        exBtn.config(fg=color)
        hLabel.config(fg=color)
        time.sleep(0.20)
#thread to change color of the widgets
def change_color_thread():
    threading.Thread(target=change_colors).start()
#convert seconds to hour, mins, second in formated way like, 456 seconds to xx:xx:xx format
def audio_duration(length):
    hours = length // 3600
    length %= 3600
    mins = length // 60
    length %= 60
    seconds = length
    return hours, mins, seconds
#thread to check music is playing or not
def check_thread():
    threading.Thread(target=check).start()
#running a check_thread function to check whether a music is played or not
check_thread()
change_color_thread()
#function to minimize window if close (X) button is pressed
def minimize_window():
    root.iconify()
#setting a window protocol to call a function (minimize_window function)
root.protocol('WM_DELETE_WINDOW', minimize_window)
#show window in a mainloop
root.mainloop()
#This much:)
#Made by Bidhan Acharya