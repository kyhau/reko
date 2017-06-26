"""
NOTE: this example requires PyAudio because it uses the Microphone class
""" 
from __future__ import print_function
import os
import speech_recognition as sr
import time
from playsound import playsound

from polly import Polly
from reko import Reko


class SpeechReko(Reko):
    def __init__(self, profile, collection_id, audio_on=False):
        Reko.__init__(self, profile, collection_id)
        self._audio_on = audio_on
        self._polly = Polly(profile)

    def signin(self, id=None):
        """
        :param id: (optional) external_image_id
        :return: external_image_id or None if not found
        """
        ret_id = super(SpeechReko, self).signin(id)
        if self._audio_on is True:
            self.speak("Hello {}!".format(ret_id) \
                if ret_id is not None else "Sorry! I do not recognise you.")
        return ret_id

    def signup(self, id):
        """
        :param id: external_image_id
        :return:
        """
        succeeded = super(SpeechReko, self).signup(id)
        if self._audio_on is True:
            self.speak("Hello {}!".format(id) if succeeded is True else "Sorry {}! I have problem remembering you!".format(id))
        return succeeded

    def take_picture(self):
        """Connect to the webcam and capture an image and save to the give file.
        """
        succeeded = super(SpeechReko, self).take_picture()
        if succeeded is False and self._audio_on:
            self.speak("Sorry! I'm unable to connect to the camera.")
        return succeeded

    def speak(self, msg):
        """Create an audio file for the given msg and play it.
        """
        if self._audio_on is False:
            print(msg)
            return True

        filename = self._cache.get_filename(msg, 'mp3')
        filepath = self._cache.get_filepath(filename)
        if os.path.exists(filepath):
            SpeechReko.play_audio(filepath)
            return True
        if self._polly.synthesize_speech(text_message=msg, output_file=filepath) is True:
            SpeechReko.play_audio(filepath)
            return True
        return False

    @staticmethod
    def play_audio(audio_file):
        """
        Play sound
        """
        playsound(audio_file)

    def watching(self, interval_sec=30):
        """
        """
        while True:
            print("Watching ...")
            try:
                ret_id = super(SpeechReko, self).signin()
                if ret_id and self._audio_on is True:
                    self.speak("Hello {}!".format(ret_id))
            except Exception as e:
                print("Error: {0}".format(e))

            time.sleep(interval_sec)

    def listening(self):
        """Obtain audio from the microphone
        """
        while True:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening ...")
                audio = recognizer.listen(source)
                try:
                    input_msg = recognizer.recognize_google(audio)
                    if self.process_message(input_msg) is False:
                        break
                except sr.UnknownValueError:
                    self.speak("Please say it again")
                except sr.RequestError as e:
                    self.speak("I have problem listening to you")
                    print("Error: {0}".format(e))

    def process_message(self, input_msg):
        """Process message and return False if stop listening
        """
        print("You said " + input_msg)

        # TODO still in progress, this part is tmp code
        if 'bye' in input_msg or 'goodbye' in input_msg or 'good bye' in input_msg:
            self.speak("Goodbye")
            return False

        if 'sign in' in input_msg or 'sign-in' in input_msg:
            self.signin()

        return True
