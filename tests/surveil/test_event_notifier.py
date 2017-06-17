from mockito import expect, unstub, verifyNoUnwantedInteractions
from unittest import TestCase

import google.mail
from surveil.event_notifier import EventNotifier


class TestEventNotifier(TestCase):
    A_SUBJECT = 'subject'
    A_TEXT = 'text'
    A_MESSAGE = 'message'

    def setUp(self):
        self._settings = self._create_settings()

    def test_that_it_can_send_a_message(self):
        expect(google.mail.MailSender, times=1).create_message(
                self._settings['from'],
                self._settings['to'],
                self.A_SUBJECT,
                self.A_TEXT) \
            .thenReturn(self.A_MESSAGE)

        expect(google.mail.MailSender, times=1).send_message(
                'me',
                self.A_MESSAGE)

        event_notifier = EventNotifier(self._create_settings())

        event_notifier.send_message('subject', 'text')

        verifyNoUnwantedInteractions()
        unstub()

    @staticmethod
    def _create_settings():
        return {
            'from': 'from@mail.com',
            'to': ['to@mail.com'],
            'motion': {
                'min_distance': 60
            }
        }
