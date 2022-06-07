from utils import send_notification_emails
from base import Session
from user import User
from user_metrics import UserMetrics

from datetime import date

# Script runs daily at 10:00am

# Create session
db_session = Session()
user_query = db_session.query(User)

today = date.today()

target_users = []
# Generate list of users who haven't uploaded metrics today
for user in user_query:
    # Retrieve most recently uploaded metric
    user_metric = db_session.query(UserMetrics) \
        .filter(UserMetrics.user_id == user.id) \
        .order_by(UserMetrics.date.desc()) \
        .first()

    # If user has uploaded metrics in the past and has not yet for today
    if user_metric != None and user_metric.date != today:
        target_users.append(user)


# Send emails to target users
send_notification_emails(target_users)