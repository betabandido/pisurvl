from camera.factory import CameraFactory
from camera.opencv import OpenCVCamera

CameraFactory.register('opencv', OpenCVCamera)
