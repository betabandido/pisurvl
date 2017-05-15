from camera.factory import register_camera
from camera.opencv import OpenCVCamera

register_camera('opencv', OpenCVCamera)
