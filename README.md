# Reko (in progress)

Simple scripts for supporting face-based user verification using 
[Amazon Rekognition](https://aws.amazon.com/rekognition/) and [OpenCV 2](http://opencv.org/).
Also support vocal confirmation using [Amazon Polly](https://aws.amazon.com/polly/details/).

- [LICENSE](LICENSE)
- [Release Notes](ReleaseNotes.md)

## Build

1. Install [OpenCV 2](http://opencv.org/) (not in pypi):

    1. On Debian-based systems: `sudo apt-get install python-opencv` 
    1. On Windows: Download [opencv_python-2.4.13.2](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv) into a folder (e.g. named `dist_ext`)

1. Install python dependencies

   ```
   virtualenv env
   env\Scripts\activate
   pip install --find-links dist_ext -e .
   
   ```
