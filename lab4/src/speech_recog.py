#!/usr/bin/env python3

'''
Speech to text conversion

dependencies:
pyaudio: http://people.csail.mit.edu/hubert/pyaudio/#downloads
SpeechRecognition: https://pypi.org/project/SpeechRecognition/

references:
https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py
'''

import speech_recognition as sr

def recognize_audio(r, audio):
    try:
        print(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Unable to recognize audio")
    except sr.RequestError as e:
        print("Request Error:", str(e))

if __name__ == '__main__':
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening for audio...")
            audio = r.listen(source)
        recognize_audio(r, audio)

'''
relying on recognize_google api calls makes program irresponsive to audio input
pocketsphinx - better for continuously streaming audio but has low accuracy
- requires fine-tuning dictionaries and models
may attempt C# SR toolkits or improving pocketsphinx performance
'''