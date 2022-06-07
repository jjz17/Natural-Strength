from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

# Email variables.
EMAIL_FROM = 'a.plus.or.no.rice@gmail.com'
EMAIL_TO = 'jasonjzhang17@gmail.com'
EMAIL_SUBJECT = 'Hello  from Lyfepedia!'
EMAIL_CONTENT = f'''
                <html>
                    <body>
                        <h1>Daily Fitness Motivation</h1>
                        <p>Hello {EMAIL_TO}, let's get to work!</p>
                    </body>
                </html>
                '''
# EMAIL_CONTENT = 'Hello, this is a test\nLyfepedia\nhttps://lyfepedia.com'

def create_message(sender, to, subject, message_text):
  """Create a message for an email.
  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, 'html')
  # message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  body = {'raw': raw}
  return body
  # return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
  """Send an email message.
  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def service_account_login():
  SCOPES = ['https://www.googleapis.com/auth/gmail.compose']
#   SERVICE_ACCOUNT_FILE = 'service-key.json'

#   credentials = service_account.Credentials.from_service_account_file(
#           SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
  # delegated_credentials = credentials.with_subject(EMAIL_FROM)
  service = build('gmail', 'v1', credentials=credentials)
  return service


service = service_account_login()
# Call the Gmail API
message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
sent = send_message(service,'me', message)