from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages
import os

# Makes setup work inside of a virtualenv
use_system_lib = True
if os.environ.get("BUILD_LIB") == "1":
    use_system_lib = False

base_dir = os.path.dirname(__file__)

__author__ = "Kayan Hau"
__email__ = "virtualda@gmail.com"

__title__ = "reko"
__version__ = "0.1.0.dev0"
__summary__ = "This package supports face-based user verification using Amazon Rekognition."
__uri__ = "https://github.com/kyhau/reko"

__requirements__ = [
    'boto3>=1.4.4',
    'opencv-python>=3.2.0.6',
    'numpy>=1.11.1+mkl',
    'playsound>=1.2.1',
    'SpeechRecognition>=3.6.0',
    'PyAudio>=0.2.10'
]

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    author=__author__,
    author_email=__email__,
    url=__uri__,
    zip_safe=False,
    install_requires=__requirements__,
    data_files=[
        ('', ['ReleaseNotes.md']),
    ],
    entry_points={
        'console_scripts': [
            'reko = reko.main:main'
          ]
      },
)
