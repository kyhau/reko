from __future__ import print_function
import os

from cachestore import CacheStore
from cameraman import CameraMan
from playsound import playsound
from polly import Polly
from rekognition import Rekognition


class Reko():
    def __init__(self, profile, collection_id, audio_on=False):
        self.collection_id = collection_id
        self.audio_on = audio_on
        self._cameraman = CameraMan()
        self._cache = CacheStore()
        self._rekognition = Rekognition(profile)
        self._polly = Polly(profile)

    def __del__(self):
        pass

    def list_collections(self):
        """
        List all collections.
        """
        return self._rekognition.list_collections()

    def list_faces(self):
        """
        List all faces of the current collection.
        """
        return self._rekognition.list_faces(collection_id=self.collection_id)

    def signin(self, id=None):
        """
        :param id: (optional) external_image_id
        :return: external_image_id or None if not found
        """
        if not self._rekognition.collection_exist(collection_id=self.collection_id):
            return None

        # Take an image
        if self.take_picture() is False:
            return None

        ret_id = self._rekognition.search_faces_by_image(
            collection_id=self.collection_id, image_file=self._cache.cache_img, external_image_id=id)

        if self.audio_on is True:
            self.speak("Hello {}!".format(ret_id) if ret_id is not None else "Sorry! I do not recognise you.")

        return ret_id

    def signup(self, id):
        """
        :param id: external_image_id
        :return:
        """
        if not self._rekognition.collection_exist(collection_id=self.collection_id) \
                and not self._rekognition.create_collection(collection_id=self.collection_id):
            return False

        # Take an image
        if self.take_picture() is False:
            return False

        # Store face
        succeeded = self._rekognition.index_faces(
            collection_id=self.collection_id, image_file=self._cache.cache_img, external_image_id=id)

        if self.audio_on is True:
            self.speak("Hello {}!".format(id) if succeeded is True else "Sorry {}! I have problem remembering you!".format(id))

        return succeeded

    def take_picture(self):
        """
        Connect to the webcam and capture an image and save to the give file.
        """
        # Take an image
        if self._cameraman.take_picture(image_name=self._cache.cache_img) is False:
            if self.audio_on: self.speak("Sorry! I'm unable to connect to the camera.")
            return False

        if self.audio_on: self.speak("I can see you.")
        return True

    def delete_collection(self):
        """
        Delete the current collection.
        """
        return self._rekognition.delete_collection(collection_id=self.collection_id)

    def speak(self, msg):
        """
        Create an audio file for the given msg and play it.
        """
        filename = self._cache.get_filename(msg, 'mp3')
        filepath = self._cache.get_filepath(filename)
        if os.path.exists(filepath):
            Reko.play_audio(filepath)
            return True
        if self._polly.synthesize_speech(text_message=msg, output_file=filepath) is True:
            Reko.play_audio(filepath)
            return True
        return False

    @staticmethod
    def play_audio(audio_file):
        """
        Play sound
        """
        playsound(audio_file)
