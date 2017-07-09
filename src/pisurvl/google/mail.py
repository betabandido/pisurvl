import base64
from email.mime.text import MIMEText

from googleapiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http

from pisurvl.google.credentials import get_credentials


class MailSender:
    @staticmethod
    def send_message(user_id, message):
        """Send an email message.

        Args:
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.

        Returns:
          Sent Message.
        """
        try:
            print('sending: {}'.format(message))
            service = MailSender._build_service(get_credentials())
            message = service.users().messages().send(
                userId=user_id,
                body=message).execute()
            print('Message sent: id={}'.format(message['id']))
            return message
        except errors.HttpError as error:
            print('An error occurred: {}'.format(error))

    @staticmethod
    def create_message(sender, to, subject, text):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          text: The text of the email message.

        Returns:
          An object containing a base64 encoded email object.
        """
        message = MIMEText(text)
        message['to'] = ','.join(to)
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    @staticmethod
    def _build_service(credentials):
        """Build a Gmail service object.

        httplib2.Http objects are not thread-safe. Therefore, each thread that
        makes requests must use its own instance of httplib2.Http (see:
        https://developers.google.com/api-client-library/python/guide/thread_safety).

        Args:
          credentials: OAuth 2.0 credentials.

        Returns:
          Gmail service object.
        """
        http = credentials.authorize(Http())
        return build('gmail', 'v1', http=http)
