from enum import Enum


class EmailTemplates(Enum):
    CONFIRM_EMAIL = "CONFIRM_EMAIL"


def mail_notify(recipient_email, template, *args):
    print(f"Email sent to {recipient_email}")
