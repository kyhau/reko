from __future__ import print_function
from argparse import ArgumentParser
import os
import subprocess
import sys

from cameraman import CameraMan
from polly import Polly
from rekognition import Rekognition


class Reko():
    def __init__(self, profile, collection_id):
        self.collection_id = collection_id
        self.__cameraman = CameraMan()
        self.__rekognition = Rekognition(profile)
        self.polly = Polly(profile)

    @staticmethod
    def tmp_image_file():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reko_image.png')

    @staticmethod
    def tmp_audio_file():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reko_audio.mp3')

    def list_collections(self):
        return self.__rekognition.list_collections()

    def list_faces(self):
        return self.__rekognition.list_faces(collection_id=self.collection_id)

    def signin(self, id):
        if not self.__rekognition.collection_exist(collection_id=self.collection_id):
            return False

        # Take an image
        tmp_image = self.tmp_image_file()
        self.__cameraman.take_picture(image_name=tmp_image)

        return self.__rekognition.search_faces_by_image(
            collection_id=self.collection_id,
            image_file=tmp_image,
            external_image_id=id
        )

    def signup(self, id):
        if not self.__rekognition.collection_exist(collection_id=self.collection_id) \
                and not self.__rekognition.create_collection(collection_id=self.collection_id):
            return False

        # Take an image
        tmp_image = self.tmp_image_file()
        self.__cameraman.take_picture(image_name=tmp_image)

        # Store faces
        return self.__rekognition.index_faces(
            collection_id=self.collection_id,
            image_file=tmp_image,
            external_image_id=id
        )

    def delete_collection(self):
        return self.__rekognition.delete_collection(collection_id=self.collection_id)

    def greeting(self, id):
        msg = "Hello {}!".format(id)
        if self.polly.synthesize_speech(text_message=msg, output_file=self.tmp_audio_file()) is True:
            Reko.play_audio(self.tmp_audio_file())
            return True
        return False

    @staticmethod
    def play_audio(audio_file):
        # Play the audio using the platform's default player
        if sys.platform == "win32":
            os.startfile(audio_file)
        else:
            # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, audio_file])


def get_args():
    parser = ArgumentParser(description='Reko')
    parser.add_argument('-p', '--profile', metavar='PROFILE_NAME')
    parser.add_argument('-l', '--collections', action='store_true', default=False)
    parser.add_argument('-c', '--collection_id', metavar='COLLECTION_ID')
    parser.add_argument('-d', '--delete_collection', action='store_true', default=False)
    parser.add_argument('-f', '--faces', action='store_true', default=False)
    parser.add_argument('-u', '--signup', metavar='USERNAME')
    parser.add_argument('-i', '--signin', metavar='USERNAME')
    parser.add_argument('-a', '--audio_on', action='store_true', default=False)
    return parser.parse_args()

def main():
    args = get_args()

    reko = Reko(profile=args.profile, collection_id=args.collection_id)
    print(args)

    if args.collections is True:
        reko.list_collections()

    elif args.delete_collection is True:
        reko.delete_collection()

    elif args.faces is True:
        reko.list_faces()

    elif args.signin:
        id = reko.signin(id=args.signin)
        if args.audio is True:
            reko.greeting(id)

    elif args.signup:
        reko.signup(id=args.signup)


if __name__ == "__main__":
    sys.exit(main())
