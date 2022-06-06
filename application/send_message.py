from __future__ import print_function

import base64
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials


def gmail_send_message():
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    # If modifying these scopes, delete the file token.json.
    # SCOPES = ['https://www.googleapis.com/auth/gmail.labels https://www.googleapis.com/auth/gmail.compose']
    SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

    # creds, _ = google.auth.default()
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText('This is automated draft mail')
        message['To'] = 'jasonjzhang17@gmail.com'
        message['From'] = 'a.plus.or.no.rice@gmail.com'
        message['Subject'] = 'Automated draft'
        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'message': {

                'raw': encoded_message
            }
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


if __name__ == '__main__':
    gmail_send_message()