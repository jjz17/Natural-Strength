import numpy as np

from datetime import date
import _pickle as cPickle
from collections.abc import Iterable

from user_metrics import UserMetrics, DummyUserMetrics
from em import service_account_login, create_message, send_message


def send_notification_emails(users: Iterable):
    # Log in to gmail account
    service = service_account_login()
    EMAIL_FROM = 'a.plus.or.no.rice@gmail.com'
    date_str = date.today()
    for user in users:
        # If user settings permit notification emails
        if user.notifications == 1:
            EMAIL_TO = user.email
            EMAIL_SUBJECT = f'Daily Fitness Motivation: {date_str}'
            EMAIL_CONTENT = f'''
                    <html>
                        <body>
                            <h1>Daily Fitness Motivation</h1>
                            <p>Hello {user.username}, let's get to work!</p>
                            <p>Upload your daily metrics to stay on track and continue progressing on your fitness journey.</p>
                        </body>
                    </html>
                    '''
            # Create email message
            message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
            # Send email message
            sent = send_message(service,'me', message)
            # print(sent)


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
