# Reko

Simple Python scripts for supporting face based user verification.
 
1. Obtain verbal instructions using Google API - [speechrecognition](https://github.com/Uberi/speech_recognition) to get command. (Improvement required)
1. Control webcam to take image using [OpenCV 2](http://opencv.org/). 
1. Face recognition with [Amazon Rekognition](https://aws.amazon.com/rekognition/).
1. Verbal feedback (Text-to-Speech) using [Amazon Polly](https://aws.amazon.com/polly/details/).

- [LICENSE](LICENSE)
- [Release Notes](ReleaseNotes.md)

## Build

 ```
 virtualenv env
 env\Scripts\activate
 pip install -i https://pypi.python.org/pypi -e .
 ```

## Run 

1. Get Help from command line

   ```bash
   reko --help
   ```
   
1. List all collections from command line

   ```bash
   reko --profile AWS_PROFILE_NAME --collections
   ```
   
1. List all faces in a collection

   ```bash
   reko --profile AWS_PROFILE_NAME --collection_id COLLECTION_ID --faces
   ```
   
1. Sign-up from command line. If collection does not exist, it will be created

   ```bash
   reko --profile AWS_PROFILE_NAME --collection_id COLLECTION_ID --signup NAME
   ```
   
1. Sign-in from command line, with verbal feedback

   ```bash
   reko --profile AWS_PROFILE_NAME --collection_id COLLECTION_ID --signin NAME --audio_on
   ```
   
1. Delete a collection from command line

   ```bash
   reko --profile AWS_PROFILE_NAME --delete_collection COLLECTION_ID
   ```
   
1. Sign-in using microphone

   ```bash
   reko --profile AWS_PROFILE_NAME --collection_id COLLECTION_ID --audio_on --listen_on
   ```

1. Keep watching (at the specified internal )and sign-in when possible

   ```bash
   reko --profile AWS_PROFILE_NAME --collection_id COLLECTION_ID -audio_on --watch_on INTERVAL_SEC
   ```
