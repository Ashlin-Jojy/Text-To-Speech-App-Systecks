import os
import subprocess
import pygame
from tkinter import *
from tkinter import ttk, filedialog
import subprocess
from pydub import AudioSegment
from gtts import gTTS
from GradientFrame import GradientFrame

pygame.mixer.init()

def speak(text, pitch, rate, language):
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("output.mp3")
    sound = AudioSegment.from_mp3("output.mp3")
    new_sample_rate = int(sound.frame_rate * pitch)
    new_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    new_sound.export("output_pitched.mp3", format="mp3")
    
    # Change the rate of speech using ffmpeg
    cmd = f"ffmpeg -i output_pitched.mp3 -filter:a atempo={rate} output_rate_changed.mp3"
    subprocess.call(cmd, shell=True)
    
    pygame.mixer.music.load("output_rate_changed.mp3")
    pygame.mixer.music.play()

def stop_speech():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    while os.path.exists("output.mp3") and os.path.exists("output_pitched.mp3") and os.path.exists("output_rate_changed.mp3"):
        try:
            os.remove("output.mp3")
            os.remove("output_pitched.mp3")
            os.remove("output_rate_changed.mp3")
        except PermissionError:
            pass

paused = False

def pause_speech():
    global paused
    if pygame.mixer.music.get_busy() and not paused:
        pygame.mixer.music.pause()
        paused = True

def resume_speech():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False

def toggle_pause_resume():
    global paused
    if paused:
        pause_resume_button.config(text="Pause")
        resume_speech()
        paused = False
    else:
        pause_resume_button.config(text="Resume")
        pause_speech()
        paused = True

def save_audio():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    while os.path.exists("output_rate_changed.mp3"):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if filename:
                with open("output_rate_changed.mp3", "rb") as f:
                    with open(filename, "wb") as g:
                        g.write(f.read())
                os.remove("output_rate_changed.mp3")
                print(f"Audio saved as {filename}")
            break
        except PermissionError:
            pass

# Create Tkinter GUI
root = Tk()
root.title("Text-to-Speech")

root.state('zoomed')

gf = GradientFrame(root, colors = ("#000066", "#330033"), width = 1800, height = 999)
gf.config(direction = gf.top2bottom)
gf.pack()

icon_image = PhotoImage(file ="tts_icon.png")
root.iconphoto(False, icon_image)

Top_frame = Frame(root, bg ="white", width = 1800, height = 100)
Top_frame.place(x=0, y=0)
logo = PhotoImage(file="logo.png")
Label(Top_frame, bg= "white", image=logo).place(x=0, y=10)
Label(Top_frame, text="TEXT TO SPEECH APP", font="arial 15 bold", bg = "white", fg ="black").place(x=120, y=35)

# Create text entry field
text_entry = Text(root, bg="white", width=110, height= 25)
text_entry.place(x=10, y=120)

# Create language selection dropdown
language_var = StringVar()
language_var.set("en")  # Set default language to English
language_options = ["af", "sq", "ar", "hy", "ca", "zh-CN", "zh-TW", "zh", "hr", "cs", "da", "nl", "en", "eo", "fi", "fr", "de", "el", "ht", "hu", "is", "id", "it", "ja", "ko", "la", "lv", "mk", "no", "pl", "pt", "ro", "ru", "sr", "sk", "es", "sw", "sv", "ta", "th", "tr", "vi", "cy"]
language_menu = OptionMenu(root, language_var, *language_options)
language_menu.pack(padx=10, pady=10)
language_menu.config(width=7, height=1, font="arial 10 bold", bg= "white")
language_menu.place(x=1300, y =230)
Label(root, text="Language", font="arial 14 bold", bg= "#08005d", fg="white").place(x=1300,y=195)

# Create pitch slider
pitch_slider = Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Pitch")
pitch_slider.pack(padx=10, pady=10)
pitch_slider.set(1.0)  # Set default pitch
pitch_slider.pack(padx=10, pady=10)
pitch_slider.place(x=1300, y=310)
pitch_slider.config(width=15, font="arial 13 bold", bg= "#08005d", fg="white")

# Create rate slider
rate_slider = Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Rate")
rate_slider.pack(padx=10, pady=10)
rate_slider.set(1.0)  # Set default rate
rate_slider.pack(padx=10, pady=10)
rate_slider.place(x=1300, y=420)
rate_slider.config(width=15, font="arial 13 bold", bg= "#08005d", fg="white")

# Create speak button
speak_icon = PhotoImage(file="speak.png")
speak_button = Button(root, text="Speak",compound=LEFT, image=speak_icon, command=lambda: speak(text_entry.get("1.0", "end-1c"), pitch_slider.get(), rate_slider.get(), language_var.get()))
speak_button.pack(padx=10, pady=10)
speak_button.place(x=1000, y=220)
speak_button.config(width=150, font="arial 11 bold", bg="white")

# Create stop button
stop_button = Button(root, text="Stop", command=stop_speech)
stop_button.pack(padx=10, pady=10)
stop_button.place(x=1000, y=330)
stop_button.config(width=17, font="arial 11 bold", bg= "white")

# Create pause/resume button
pause_resume_button = Button(root, text="Pause", command=toggle_pause_resume)
pause_resume_button.pack(padx=10, pady=10)
pause_resume_button.place(x=1000, y=420)
pause_resume_button.config(width=17, font="arial 11 bold", bg= "white")

# Create save button
save_icon = PhotoImage(file="save.png")
save_button = Button(root, text="Save",compound=LEFT, image=save_icon, command=save_audio)
save_button.pack(padx=10, pady=10)
save_button.place(x=600, y=600)
save_button.config(width=250, font="arial 17 bold", bg= "white")


root.mainloop()