import gtts
import speech_recognition as sr
import os
from playsound import playsound
from notion import NotionClient
from datetime import datetime

r = sr.Recognizer()
token = "secret_x5lxfAzd80OwM7Tn234b6su5NMsNOE6pku6L80KCHpp"
database_id = "b96b16f9055c4fabbab01deaf68c1e47"

client = NotionClient(token, database_id)
activation_command = "hey pat"

def retrieve_audio():
    with sr.Microphone() as source:
        print("Say something:")
        audio = r.listen(source)
    return audio

def play_audio(text):
    try:
        tts = gtts.gTTS(text)
        tempfile = "./temp.mp3"
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except AssertionError:
        print("Error playing sound.")

def speech_to_text(audio):
    text = ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("PAT could not understand audio.")
    except sr.RequestError:
        print("Could not request results from API.")
    return text



if __name__ == "__main__":
    while True:
        audio_input = retrieve_audio()
        command = speech_to_text(audio_input)

        if activation_command in command.lower():
            print("PAT is now activated!")
            play_audio("What new item would you like to add?")
            task = retrieve_audio()
            task = speech_to_text(task)

            if task:
                play_audio(task)
                now = datetime.now().astimezone().isoformat()
                res = client.create_page(task, now, status="Active")
                if res.status_code == 200:
                    play_audio("New item succesfully added")