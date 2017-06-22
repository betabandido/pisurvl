from mockito import ANY, mock, patch, unstub, verify, when
import numpy
from unittest import TestCase

from camera.factory import CameraFactory
from surveil.surveil import SurveillanceManager


class TestSurveillanceManager(TestCase):
    def setUp(self):
        self._motion_detector = mock(strict=True)
        self._event_notifier = mock(strict=True)
        self._backup_service = mock(strict=True)
        self._camera = mock(strict=True)
        self._frame = numpy.zeros((16, 16, 3), dtype=numpy.uint8)

        when(CameraFactory).create() \
            .thenReturn(self._camera)

        when(self._camera).get_frame() \
            .thenReturn(self._frame)

        self._manager = SurveillanceManager(
            self._motion_detector,
            self._event_notifier,
            self._backup_service
        )

    def tearDown(self):
        unstub()

    def test_that_a_frame_is_processed(self):
        self._setup_no_motion_detected()

        self._manager._process_frame(self._camera)

        verify(self._camera, times=1).get_frame()

    def test_that_notification_and_image_backup_occurs_if_motion_is_detected(self):
        self._setup_motion_detected()

        self._manager._process_frame(self._camera)

        verify(self._event_notifier, times=1).send_motion_notification()
        verify(self._backup_service, times=1).backup_image(ANY)

    def test_that_a_peek_request_returns_the_last_frame(self):
        self._setup_no_motion_detected()

        patch(SurveillanceManager.is_surveillance_enabled, lambda: True)

        self._manager.queue_surveillance_request(
            {'cmd': 'peek'},
            self._assert_peek_response_is_valid
        )

        self._manager._process_frame(self._camera)

    def _assert_peek_response_is_valid(self, request, response):
        self.assertTrue(numpy.array_equal(response['frame'], self._frame))

    def _setup_no_motion_detected(self):
        when(self._motion_detector).detect_motion(ANY) \
            .thenReturn(False)

    def _setup_motion_detected(self):
        when(self._motion_detector).detect_motion(ANY) \
            .thenReturn(True)

        when(self._event_notifier).send_motion_notification()
        when(self._backup_service).backup_image(ANY)
