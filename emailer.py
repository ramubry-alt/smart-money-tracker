</> Python

import smtplib
from email.mime.text import MIMEText
from config import EMAIL_FROM, EMAIL_TO, EMAIL_APP_PASSWORD, SMTP_SERVER, SMTP_PORT


def send_email(subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully.")

    except Exception as e:
        print(f"Email failed: {e}")
