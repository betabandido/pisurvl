from pisurvl.camera.opencv import OpenCVCamera

from pisurvl.camera.factory import CameraFactory

CameraFactory.register('opencv', OpenCVCamera)
