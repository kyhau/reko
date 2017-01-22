from __future__ import print_function
from argparse import ArgumentParser
import os
import sys

from cameraman import CameraMan
from rekognition import Rekognition


class Reko():
    def __init__(self, profile, collection_id):
        self.collection_id = collection_id
        self.__rekognition = Rekognition(profile)
        self.__cameraman = CameraMan()

    @staticmethod
    def tmp_image_file():
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_image.png')

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


def get_args():
    parser = ArgumentParser(description='Reko')
    parser.add_argument('-p', '--profile', metavar='PROFILE_NAME')
    parser.add_argument('-l', '--collections', action='store_true', default=False)
    parser.add_argument('-c', '--collection_id', metavar='COLLECTION_ID')
    parser.add_argument('-d', '--delete_collection', action='store_true', default=False)
    parser.add_argument('-f', '--faces', action='store_true', default=False)
    parser.add_argument('-i', '--signin', metavar='USERNAME')
    parser.add_argument('-u', '--signup', metavar='USERNAME')
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
        reko.signin(id=args.signin)

    elif args.signup:
        reko.signup(id=args.signup)


if __name__ == "__main__":
    sys.exit(main())
