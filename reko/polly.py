from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

DEFAULTS = {
    "region_name": "ap-southeast-2", # Sydney
    "voice_id": "Nicole",
    "input_text_type": "text",
    "output_format": "mp3",
    "output_filename": "polly_speech.mp3"
}

def status_code(ret):
    return ret["ResponseMetadata"]["HTTPStatusCode"]


class Polly():
    def __init__(self, profile, region=DEFAULTS["region_name"]):
        self.profile = profile
        self.region_name = region
        self.client = self.get_client()

    def get_client(self):
        # Create a client using the credentials and region defined in the [profile_name]
        # section of the AWS credentials file (~/.aws/credentials).
        session = Session(profile_name=self.profile)
        client = session.client("polly", region_name=self.region_name)
        return client

    def synthesize_speech(self,
            text_message, text_type=DEFAULTS["input_text_type"],
            voice_id=DEFAULTS["voice_id"],
            output_format=DEFAULTS["output_format"], output_file=DEFAULTS["output_filename"]
    ):
        try:
            import os
            if os.path.exists(output_file):
                print("Deleting existing file")
                os.remove(output_file)

            response = self.client.synthesize_speech(
                OutputFormat=output_format,
                Text=text_message,
                VoiceId=voice_id
            )
            # Access the audio stream from the response
            if "AudioStream" in response:
                # Note: Closing the stream is important as the service throttles on the
                # number of parallel connections. Here we are using contextlib.closing to
                # ensure the close method of the stream object will be called automatically
                # at the end of the with statement's scope.
                with closing(response["AudioStream"]) as stream:
                    try:
                        # Open a file for writing the output as a binary stream
                        with open(output_file, "wb") as file:
                            file.write(stream.read())

                        return True
                    except IOError as error:
                        # Could not write to file, exit gracefully
                        print(error)
            else:
                # The response didn't contain audio data, exit gracefully
                print("Could not stream audio")

        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)

        return False
