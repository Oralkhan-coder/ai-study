import os
import smtplib
import ssl
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


class EmailService:
    def __init__(self, sender_email: str, sender_password: str, smtp_server: str, smtp_port: int):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    async def send_email(self, to_email: str, subject: str, html_content: str):
        message = MIMEMultipart("alternative")
        message["From"] = self.sender_email
        message["To"] = to_email
        message["Subject"] = subject

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        await asyncio.to_thread(
            self._send_smtp, to_email, message
        )

    def _send_smtp(self, to_email: str, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, to_email, message.as_string())



async def get_email_service() -> EmailService:
    load_dotenv()
    return EmailService(
        os.getenv("EMAIL_USER"),
        os.getenv("EMAIL_PASSWORD"),
        os.getenv("SMTP_SERVER"),
        int(os.getenv("SMTP_PORT"))
    )