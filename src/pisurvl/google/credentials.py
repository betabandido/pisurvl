import oauth2client
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import os.path


SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.send'
]

PISURVL_PATH = os.path.join(os.path.expanduser('~'), '.pisurvl')
CREDENTIALS_PATH = os.path.join(PISURVL_PATH, 'credentials.json')
CLIENT_SECRETS_PATH = os.path.join(PISURVL_PATH, 'client_secrets.json')
APPLICATION_NAME = 'pisurvl'


def get_credentials(flags=None):
    """Gets valid user credentials from storage.

    If no credentials have been stored yet, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        The obtained credentials.
    """
    store = oauth2client.file.Storage(CREDENTIALS_PATH)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_PATH, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6 (TODO: do we need this?)
            credentials = tools.run_flow(flow, store)

    return credentials

if __name__ == '__main__':
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    get_credentials(flags)
