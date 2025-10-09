import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="50bed54d4bde4cd5b897be63f20f0e48",
    client_secret="69ec6486a53c4edc98a44bef0371da0e",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-modify-playback-state,user-read-playback-state"
))

engine = pyttsx3.init()
def say(text):
    print("Penis:", text)
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()

mic_list = sr.Microphone.list_microphone_names()
default_mic_index = None

try:
    with sr.Microphone() as default_mic:
        default_mic_index = default_mic.device_index
except Exception as e:
    print("⚠️ Error finding def mic:", e)

if default_mic_index is not None:
    print(f"✅ Default mic is using: {mic_list[default_mic_index]}")
else:
    print("❌Using the first mic")
    default_mic_index = 0

mic = sr.Microphone(device_index=default_mic_index)

devices = sp.devices()
if devices["devices"]:
    device_id = devices["devices"][0]["id"]

#HERE YOU CAN ADD MORE COMMANDS WITH SPOTIPY

def play_music():
    try:
        if devices["devices"]:
            sp.start_playback(device_id=device_id)
            say("Music")
        else:
            say("No active Spotify players")
    except Exception as e:
        print("Error Spotify:", e)

def pause_music():
    sp.pause_playback()
    say("Paused")

def next():
    sp.next_track(device_id=device_id)
    print("Next track")

def prev():
    sp.previous_track(device_id=device_id)
    print("Previous track")

def vol(volume):
    sp.volume(device_id=device_id, volume_percent=volume)


def callback(recognizer, audio):
    try:
        command = recognizer.recognize_google(audio, language="en-US").lower()
        print("You said:", command)

        #AFTER YOU ADDED A DEF WITH A COMMAND WRITE IT HERE AS ELIF "command"

        if "music" in command:
            play_music()
        elif "pause" in command or "stop" in command:
            pause_music()

        elif "volume" in command:
            words = command.split()
            for word in words:
                if word.isdigit():
                    vol(int(word))
                    say(f"Volume set to {word}")

        elif "exit" in command:
            say("Exiting")
            quit()
    except sr.UnknownValueError:
        pass
    except Exception as e:
        print("Error:", e)

with mic as source:
    print("Setting im the mic...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    say("Come on bro, talk.")

stop_listening = recognizer.listen_in_background(mic, callback)

while True:
    time.sleep(0.0001)
