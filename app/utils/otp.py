import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def generate_otp(length: int = 6) -> str:
    digits = "0123456789"
    otp = "".join(random.choices(digits, k=length))
    return otp


def send_otp_email(email: str, otp: str):
    sender_email = "your-email@example.com"
    sender_password = "your-email-password"
    subject = "Your OTP Code"
    body = f"Your OTP code is {otp}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.close()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
