import cv2
import imutils
from PIL import Image

from pisurvl.motion.inspector import DummyInspector


class MotionDetector:
    def __init__(self, settings, inspector=DummyInspector()):
        self.delta_threshold = settings['delta_threshold']
        self.min_area = settings['min_area']
        self.resize_width = settings['resize_width']
        self.inspector = inspector

        self.avg = None

    def detect_motion(self, frame):
        frame = imutils.resize(frame, self.resize_width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)  # TODO add setting
        self.inspector.dump(gray, 'gray')

        if self.avg is None:
            self.avg = gray.copy().astype('float')
            return False

        cv2.accumulateWeighted(gray, self.avg, 0.5)
        delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        self.inspector.dump(delta, 'delta')

        threshold = cv2.threshold(delta, self.delta_threshold, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)
        self.inspector.dump(threshold, 'threshold')
        (_, contours, _) = cv2.findContours(threshold.copy(),
                                            cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for c in contours:
            print('ca:{}'.format(cv2.contourArea(c)))
            if cv2.contourArea(c) < self.min_area:
                continue
            motion_detected = True

        return motion_detected


if __name__ == '__main__':
    import argparse
    from numpy import array

    from pisurvl.motion import BasicInspector
    from pisurvl.settings import settings
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_images',
                        nargs='+',
                        help='Input images')
    args = parser.parse_args()
    detector = MotionDetector(settings['motion'], inspector=BasicInspector())
    for filename in args.input_images:
        img = array(Image.open(filename))
        motion = detector.detect_motion(img)
        print('Motion: {}'.format(motion))
