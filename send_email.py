import os
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_credentials import email, password

smtp_port = 587
smtp_server = "smtp.gmail.com"

email_from = email
email_list = [ email]
pswd = password

subject = "New email sent from your Device😎"


def send_emails(email_list):
    for person in email_list:
        body = f"""
        The person tried to access your Device at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:
        please be safe..
        """

        picture_folder = "pictures of unauthorized persons"
        picture_files = [f for f in os.listdir(picture_folder) if f.endswith('.png')]

        latest_picture = max(picture_files, key=lambda x: os.path.getmtime(os.path.join(picture_folder, x)))

        msg = MIMEMultipart()
        msg["From"] = email_from
        msg["To"] = person
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        file_path = os.path.join(picture_folder, latest_picture)
        attachment = open(file_path, 'rb')
        attachment_package = MIMEBase("application", 'octet-stream')
        attachment_package.set_payload(attachment.read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', f"attachment; filename={latest_picture}")
        msg.attach(attachment_package)

        text = msg.as_string()

        print("Connecting with the server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Successfully connected to the server")
        print()

        print(f"Sending email to: {person}....")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

        TIE_server.quit()

if __name__ == "__main__":
    send_emails(email_list)
















































