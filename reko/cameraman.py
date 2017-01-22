"""
Reference: https://codeplasma.com/2012/12/03/getting-webcam-images-with-python-and-opencv-2-for-real-this-time/
"""
from __future__ import print_function

import cv2
import os
import sys

# TODO Check if Camera 0 is the webcam on your machine
DEFAULT_CAMERA_PORT = 0

# Number of frames to throw away while the camera adjusts to light levels
DEFAULT_RAMP_FRAMES = 30


class CameraMan():
    def __init__(self, camera_port=DEFAULT_CAMERA_PORT):
        """
        :param camera_port: The camera port number of the webcam on your machine
        """
        self.camera_port = camera_port

    def get_image(self, camera):
        """
        Captures a single image from the camera and returns it in PIL format
        :return:
        """
        # read is the easiest way to get a full image out of a VideoCapture object.
        retval, im = camera.read()
        return im

    def take_picture(self, image_name, ramp_frames=DEFAULT_RAMP_FRAMES):
        """
        :param ramp_frames: Number of frames to throw away while the camera adjusts to light levels
        :return:
        """
        # Now we can initialize the camera capture object with the
        # cv2.VideoCapture class. All it needs is the index to a camera port.
        camera = cv2.VideoCapture(self.camera_port)

        # Ramp the camera - these frames will be discarded and are only used to
        # allow v4l2 to adjust light levels, if necessary
        for i in xrange(ramp_frames):
            temp = self.get_image(camera)

        print("Taking image...")

        # Take the actual image we want to keep
        camera_capture = self.get_image(camera)
        file = "test_image.png"

        # A nice feature of the imwrite method is that it will automatically
        # choose the correct format based on the file extension you provide.
        cv2.imwrite(image_name, camera_capture)

        # You'll want to release the camera, otherwise you won't be able to
        # create a new capture object until your script exits
        del (camera)

        print("Image saved to {}".format(image_name))


def main(argv):
    app = CameraMan()
    myimage = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_image.png')
    app.take_picture(image_name=myimage)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
