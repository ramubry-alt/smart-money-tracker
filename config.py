import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


EMAIL_FROM = os.getenv("EMAIL_FROM", "ramubry@gmail.com")
EMAIL_TO = os.getenv("EMAIL_TO", "ramubry@gmail.com")

EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
