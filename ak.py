from tkinter import *
import pygame
import time
from mutagen.mp3 import MP3
from tkinter import filedialog
import tkinter.ttk as ttk


root = Tk()
root.title("Blossom Player")
root.iconbitmap(r"C:\Users\Ayush\Desktop\Blossom_Player\Images\music-note.ico")
root.geometry("500x350")


# functions
def add_music():

    song = filedialog.askopenfilename(
        initialdir='audio/', title="Choose Music", filetypes=(("mp3 files", "*.mp3"), ))
    song = song.replace("C:/Users/Ayush/Desktop/Blossom_Player/Audio/", "")
    song = song.replace(".mp3", "")
    playlist.insert(END, song)


def play():
    song = playlist.get(ACTIVE)
    song = f"C:/Users/Ayush/Desktop/Blossom_Player/Audio/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    play_time()


def stop():
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)


global paused
paused = False


def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def next_song():
    next_music = playlist.curselection()
    next_music = next_music[0]+1
    song = playlist.get(next_music)
    song = f"C:/Users/Ayush/Desktop/Blossom_Player/Audio/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(next_music)
    playlist.selection_set(next_music, last=None)


def prev_song():
    next_music = playlist.curselection()
    next_music = next_music[0]-1
    song = playlist.get(next_music)
    song = f"C:/Users/Ayush/Desktop/Blossom_Player/Audio/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist.selection_clear(0, END)
    playlist.activate(next_music)
    playlist.selection_set(next_music, last=None)


def del_music():
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()


def del_all():
    playlist.delete(0, END)
    pygame.mixer.music.stop()


def add_many_music():
    songs = filedialog.askopenfilenames(
        initialdir='audio/', title="Choose Music", filetypes=(("mp3 files", "*.mp3"), ))
    for song in songs:
        song = song.replace("C:/Users/Ayush/Desktop/Blossom_Player/Audio/", "")
        song = song.replace(".mp3", "")
        playlist.insert(END, song)


def play_time():

    current_time = pygame.mixer.music.get_pos()/1000
    conv = time.strftime('%M:%S', time.gmtime(current_time))
    curr_song = playlist.curselection()

    song = playlist.get(curr_song)
    song = f"C:/Users/Ayush/Desktop/Blossom_Player/Audio/{song}.mp3"
    Muta = MP3(song)
    global song_len
    song_len = Muta.info.length

    conv_length = time.strftime('%M:%S', time.gmtime(song_len))
    status_bar.config(text=f'{conv}/{conv_length}')

    status_bar.after(1000, play_time)


pygame.mixer.init()
playlist = Listbox(root, bg="black", fg="blue",
                   selectbackground="gray", selectforeground="black", width=70)
playlist.pack(pady=20)

# buttons
play_btn = PhotoImage(
    file=r"C:\Users\Ayush\Desktop\Blossom_Player\Images\play.png")
pause_btn = PhotoImage(
    file=r"C:\Users\Ayush\Desktop\Blossom_Player\Images\pause.png")
stop_btn = PhotoImage(
    file=r"C:\Users\Ayush\Desktop\Blossom_Player\Images\stop.png")
frwd_btn = PhotoImage(
    file=r"C:\Users\Ayush\Desktop\Blossom_Player\Images\next.png")
prev_btn = PhotoImage(
    file=r"C:\Users\Ayush\Desktop\Blossom_Player\Images\prev.png")
# Player Control Panel
control = Frame(root)
control.pack()

# Panel Buttons
play_button = Button(control, image=play_btn, borderwidth=0, command=play)
pause_button = Button(control, image=pause_btn,
                      borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control, image=stop_btn, borderwidth=0, command=stop)
frwd_button = Button(control, image=frwd_btn, borderwidth=0, command=next_song)
prev_button = Button(control, image=prev_btn, borderwidth=0, command=prev_song)


play_button.grid(row=0, column=0, padx=10)
pause_button.grid(row=0, column=1, padx=10)
stop_button.grid(row=0, column=2, padx=10)
frwd_button.grid(row=0, column=3, padx=10)
prev_button.grid(row=0, column=4, padx=10)

# menu
menu_play = Menu(root)
root.config(menu=menu_play)

# Add Songs
add_music_menu = Menu(menu_play)
menu_play.add_cascade(label="Add Music", menu=add_music_menu)
add_music_menu.add_command(label="Add Music to Playlist", command=add_music)
add_music_menu.add_command(
    label="Add Musics to Playlist", command=add_many_music)

# del
rm_music_menu = Menu(menu_play)
menu_play.add_cascade(label="Remove Music", menu=rm_music_menu)
rm_music_menu.add_command(label="Delete one Music", command=del_music)
rm_music_menu.add_command(label="Delete all Music", command=del_all)


status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


root.mainloop()
