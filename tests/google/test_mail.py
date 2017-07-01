import base64
from unittest import TestCase

from google.mail import MailSender


class TestMailSender(TestCase):
    FROM_EMAIL = 'from@email.com'
    TO_EMAIL = ['to1@email.com', 'to2@gmail.com']
    A_SUBJECT = 'this is the subject'
    A_TEXT = 'this is the message text'

    def test_that_a_message_is_created_correctly(self):
        message = MailSender.create_message(
            self.FROM_EMAIL,
            self.TO_EMAIL,
            self.A_SUBJECT,
            self.A_TEXT)

        message = base64.urlsafe_b64decode(message['raw']).decode()
        parts = message.split('\n')

        self.assertIn('from: {}'.format(self.FROM_EMAIL), parts)
        self.assertIn('to: {}'.format(','.join(self.TO_EMAIL)), parts)
        self.assertIn('subject: {}'.format(self.A_SUBJECT), parts)
        self.assertIn(self.A_TEXT, parts)
