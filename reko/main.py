from __future__ import print_function
from argparse import ArgumentParser
import sys

import speechreko


def get_args():
    parser = ArgumentParser(description='Reko')
    parser.add_argument('-p', '--profile', metavar='PROFILE_NAME')
    parser.add_argument('-s', '--collections', action='store_true', default=False)
    parser.add_argument('-c', '--collection_id', metavar='COLLECTION_ID')
    parser.add_argument('-d', '--delete_collection', action='store_true', default=False)
    parser.add_argument('-f', '--faces', action='store_true', default=False)

    parser.add_argument('-u', '--signup', metavar='USERNAME')
    parser.add_argument('-i', '--signin', metavar='USERNAME')

    parser.add_argument('-a', '--audio_on', action='store_true', default=False)
    parser.add_argument('-l', '--listen_on', action='store_true', default=False)
    return parser.parse_args()


def main():
    args = get_args()

    app = speechreko.SpeechReko(profile=args.profile, collection_id=args.collection_id, audio_on=args.audio_on)
    print(args)

    if args.collections is True:
        app.list_collections()

    elif args.delete_collection is True:
        app.delete_collection()

    elif args.faces is True:
        app.list_faces()

    elif args.signin:
        app.signin(id=None)

    elif args.signup:
        app.signup(id=args.signup)

    elif args.listen_on is True:
        app.listening()


if __name__ == "__main__":
    sys.exit(main())
