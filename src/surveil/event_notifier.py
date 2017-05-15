from datetime import datetime
import os.path
import yaml

from google.mail import create_message, send_message
from settings import basepath


class EventNotifier:
    """Class to send event notifications."""

    def __init__(self, settings):
        with open(os.path.join(basepath, 'mail_secrets.yaml')) as f:
            doc = yaml.load(f)
            self.MAIL_FROM = doc['from']
            self.MAIL_TO = doc['to']

        self.last_time = None
        self.min_distance = settings['min_distance']

    def send_motion_notification(self):
        """Sends a motion notification."""
        if self._notification_was_recently_sent():
            return

        curr_time = datetime.now()

        msg = create_message(
            self.MAIL_FROM,
            self.MAIL_TO,
            'Surveillance notification',
            'Motion detected at {}'.format(str(curr_time)))
        send_message("me", msg)

        self.last_time = curr_time

    def send_message(self, subject, text=None):
        """Sends a generic message."""
        if text is None:
            text = subject
        msg = create_message(
            self.MAIL_FROM,
            self.MAIL_TO,
            subject,
            '{}, time:{}'.format(text, str(datetime.now())))
        send_message("me", msg)

    def _notification_was_recently_sent(self):
        return self.last_time is not None \
                and (datetime.now() - self.last_time).total_seconds() < self.min_distance


if __name__ == '__main__':
    from settings import settings

    notifier = EventNotifier(settings['notification'])
    notifier.send_motion_notification()
    notifier.send_motion_notification()  # this one shouldn't be sent
    notifier.send_message('test', 'test')
