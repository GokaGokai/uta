import os
import keyboard
import speech_recognition as sr
import win32clipboard
import pygame


os.system("title 歌")
pygame.mixer.init()
r = sr.Recognizer()
mic = sr.Microphone()

listening = False
text = ""
lang = ["en-US","fr-FR","ja-JP","ar-SA"]
indexLang = 0

def toggle_listening():
    global listening
    if listening:
        listening = False
        print(f"Ignoring.                                ", end ="\r")
    else:
        listening = True
        text = ""
        audio_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound.wav')
        sound_effect = pygame.mixer.Sound(audio_path1)
        sound_effect.play()
        print(f"Listening in " + lang[indexLang] + ", " + text + "                                     ", end="\r")

def selectLang():
    global indexLang
    indexLang += 1
    if indexLang == len(lang):
        indexLang = 0
    print(f"Listening in " + lang[indexLang] + ", " + text + "                                     ", end="\r")

keyboard.add_hotkey('alt+q', toggle_listening)
keyboard.add_hotkey('alt+W', selectLang)

print("")
print("------------------------------------------------")
print("    uta")
print("  by GokaGokai/ JohnTitorTitor/ Kanon")
print("------------------------------------------------")
print("")
print("ToggleListen:    alt+q")
print("SelectLang:      alt+w")
print("")
toggle_listening()

while 1:
    try:
        while listening:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio, language=lang[indexLang])
                    
                    print(f"Listening in " + lang[indexLang] + ", " + text + "                                     \n", end="\r")
                    audio_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound2.wav')
                    sound_effect = pygame.mixer.Sound(audio_path2)
                    sound_effect.play()

                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
                    win32clipboard.CloseClipboard()
                except sr.UnknownValueError:
                    text = "..."
                    print(f"Listening in " + lang[indexLang] + ", " + text + "                                     ", end="\r")
                except sr.RequestError as e:
                    print(f"Could not request results from Speech Recognition service; {e}")
        while not listening:
            print(f"Ignoring.                                ", end ="\r")
    except KeyboardInterrupt:
        break

# remove the keyboard shortcut
keyboard.remove_hotkey('alt+q')