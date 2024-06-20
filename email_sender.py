import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

EMAIL_SERVER = "smtp.gmail.com"
PORT = 587

from dotenv import load_dotenv # pip install python-dotenv

# Send email
def send_email(data):

    # Load environment variables
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd() # Return current folder
    envars = current_dir / ".env"
    load_dotenv(envars)

    sender_email = os.getenv("EMAIL_SENDER")
    email_app_password = os.getenv("EMAIL_APP_PASSWORD")
    email_recepient = os.getenv("EMAIL_RECEPIENT")

    titles = [album['title'] for album in data]

    msg = EmailMessage()
    msg["Subject"] = ', '.join(titles)
    msg["From"] = formataddr(("VinylBot 🤖", f"{sender_email}"))
    msg["To"] = email_recepient

    env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
    )
    template = env.get_template("email.html")
    html = template.render(albums=data)

    # Send HTML
    msg.add_alternative(
        html,subtype="html"
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, email_app_password)
        server.sendmail(sender_email, email_recepient, msg.as_string())

# if __name__ == "__main__":
#     send_email(receiver_email="adross1027@gmail.com", post_title="PETE ROCK")