import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fitlife.config import settings

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str):
        """
        Sends an HTML email using SMTP configuration.
        """
        if not settings.smtp.user or not settings.smtp.password:
            print(f"Skipping email to {to_email} (SMTP credentials not configured)")
            return False

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.smtp.from_email
        message["To"] = to_email

        # Attach HTML content
        part = MIMEText(html_content, "html")
        message.attach(part)

        try:
            with smtplib.SMTP(settings.smtp.host, settings.smtp.port) as server:
                if settings.smtp.use_tls:
                    server.starttls()
                server.login(settings.smtp.user, settings.smtp.password)
                server.sendmail(settings.smtp.from_email, to_email, message.as_string())
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            return False
