import numpy as np
import smtplib, ssl
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
## The pandas library is only for generating the current date, which is not necessary for sending emails
import pandas as pd

import _pickle as cPickle

from application.user_metrics import UserMetrics, DummyUserMetrics

def send_notif_emails(users: list):
    # Set up the email addresses and password. Please replace below with your email address and password
    email_from = 'a.plus.or.no.rice@gmail.com'
    password = 'jiajia2002'

    for user in users:
        # If User has notifications turned on
        if user.notifications == 1:
            email_to = user.email

            # Define the HTML document
            html = f'''
                <html>
                    <body>
                        <h1>Daily S&P 500 prices report</h1>
                        <p>Hello {user.username}, welcome to your report!</p>
                    </body>
                </html>
                '''
            # Generate today's date to be included in the email Subject
            date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

            # Create a MIMEMultipart class, and set up the From, To, Subject fields
            email_message = MIMEMultipart()
            email_message['From'] = email_from
            email_message['To'] = email_to
            email_message['Subject'] = f'Report email - {date_str}'

            # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
            email_message.attach(MIMEText(html, "html"))
            # Convert it as a string
            email_string = email_message.as_string()

            # Connect to the Gmail SMTP server and Send Email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email_from, password)
                server.sendmail(email_from, email_to, email_string)

def choose_pred(current, pred):
    result = max(current, pred)
    if result == current:
        result *= 1.05
    return result


def copy_metrics(user_metric: UserMetrics):
    if user_metric != None:
        return DummyUserMetrics(user_metric.weight, user_metric.squat, user_metric.bench, user_metric.deadlift, user_metric.date)
    return None


def generate_null_metrics():
    return {'data': {'user_metric': DummyUserMetrics(None, None, None, None, None)}, 'units': ''}


def handle_unit_conversion(input_unit_kg: True, output_unit_kg: False, **data):
    if input_unit_kg and not output_unit_kg:
        for key in data.keys():
            # Check if data is a UserMetrics object
            if isinstance(data[key], UserMetrics) or isinstance(data[key], DummyUserMetrics):
                data[key] = metrics_kg_to_lbs(data[key])
            else:
                data[key] = kg_to_lbs(data[key])
        units = 'Lbs'
    elif not input_unit_kg and output_unit_kg:
        for key in data.keys():
            data[key] = lbs_to_kg(data[key])
        units = 'Kg'
    elif not output_unit_kg:
        for key in data.keys():
            # Check if data is a UserMetrics object
            if isinstance(data[key], UserMetrics) or isinstance(data[key], DummyUserMetrics):
                data[key] = metrics_kg_to_lbs(data[key])
        units = 'Lbs'
    else:
        units = 'Kg'
    return {'data': data, 'units': units}


def kg_to_lbs(kg):
    return round(float(kg) * 2.20462, 2)


def lbs_to_kg(lbs):
    return round(float(lbs) * 0.453592, 2)


def load_model(model_file: str):
    return cPickle.load(open(model_file, 'rb'))


def metrics_kg_to_lbs(user_metric):
    if user_metric == None:
        return None
    return DummyUserMetrics(kg_to_lbs(user_metric.weight), kg_to_lbs(user_metric.squat), kg_to_lbs(user_metric.bench), kg_to_lbs(user_metric.deadlift), user_metric.date)


def scale_stats(scaler, stats: list):
    return scaler.transform(np.array(stats).reshape(1, -1))
