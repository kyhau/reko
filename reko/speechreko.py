"""
NOTE: this example requires PyAudio because it uses the Microphone class
""" 
from __future__ import print_function
import speech_recognition as sr


# this is called from the background thread
def callback(recognizer, audio):
    try:
        print("Google thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Google error; {0}".format(e))


def listening_simple():
    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
        try:
            print("Google thinks you said " + recognizer.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google could not understand audio")
        except sr.RequestError as e:
            print("Google error; {0}".format(e))


def listening():
    recognizer = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        recognizer.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = recognizer.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    # do some other computation for 5 seconds, then stop listening and keep doing other computations
    import time
    for _ in range(50):
        time.sleep(0.1)  # we're still listening even though the main thread is doing other things
    stop_listening()  # calling this function requests that the background listener stop listening
    while True:
        time.sleep(0.1)


listening_simple()
