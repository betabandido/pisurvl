from datetime import datetime

from pisurvl.google.mail import MailSender


class EventNotifier:
    """Class to send event notifications."""

    def __init__(self, settings):
        self.last_time = None
        self.mail_from = settings['from']
        self.mail_to = settings['to']
        self.min_distance = settings['motion']['min_distance']

    def send_motion_notification(self):
        """Sends a motion notification."""
        if self._notification_was_recently_sent():
            return

        curr_time = datetime.now()

        self.send_message(
            'Surveillance notification',
            'Motion detected at {}'.format(str(curr_time)))

        self.last_time = curr_time

    def send_message(self, subject, text=None):
        """Sends a generic message."""
        if text is None:
            text = subject
        msg = MailSender.create_message(
            self.mail_from,
            self.mail_to,
            subject,
            text)
        MailSender.send_message('me', msg)

    def _notification_was_recently_sent(self):
        return self.last_time is not None \
                and (datetime.now() - self.last_time).total_seconds() < self.min_distance
