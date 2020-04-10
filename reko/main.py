import click
import sys

from reko import speechreko


@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name.")
@click.option("--collections", "-s", is_flag=True, help="List all collections.")
@click.option("--collection_id", "-c", help="Collection ID.")
@click.option("--delete_collection", "-d", is_flag=True, help="Delete the collection of collection_id.")
@click.option("--faces", "-f", is_flag=True, help="List all faces.")
@click.option("--signup", "-u", help="Signup USERNAME.")
@click.option("--signin", "-i", help="Signin USERNAME.")
@click.option("--audio_on", "-a", is_flag=True, help="Turn on audio feedback.")
@click.option("--listen_on", "-l", is_flag=True, help="Sign-in using microphone.")
@click.option("--watch_on", "-w", help="Keep watching (at the specified interval seconds) and sign-in when possible.")
def main(profile, collections, collection_id, delete_collection, faces, signup, signin, audio_on, listen_on, watch_on):

    app = speechreko.SpeechReko(profile=profile, collection_id=collection_id, audio_on=audio_on)

    if collections is True:
        app.list_collections()

    elif delete_collection is True:
        app.delete_collection()

    elif faces is True:
        app.list_faces()

    elif signin:
        app.signin(id=None)

    elif signup:
        app.signup(id=signup)

    elif watch_on:
        try:
            interval_sec = float(watch_on)
        except:
            interval_sec = 30
        app.watching(interval_sec=interval_sec)

    elif listen_on is True:
        app.listening()


if __name__ == "__main__":
    sys.exit(main())
