# -------------------------------------------------------------------
# File Path: Scripts/notifier.py
# Description: Sends notifications (via email) after certain events,
# such as successful publication or errors during the automation process.
# -------------------------------------------------------------------

import smtplib
from email.mime.text import MIMEText
import logging

# -------------------------------------------------------------------
# Section 1: Configuration Setup
# -------------------------------------------------------------------
# SMTP server configuration (for Gmail; replace with your email service)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Use 465 for SSL, or 587 for TLS
SENDER_EMAIL = "tradingrobotplug@gmail.com"  # Replace with your email address
SENDER_PASSWORD = "Falcons#1247"  # Replace with your email password or app-specific password

# Recipient's email address
RECIPIENT_EMAIL = "dadudekc@gmail.com"  # Replace with recipient's email address

# -------------------------------------------------------------------
# Section 2: Email Notification Function
# -------------------------------------------------------------------
def send_email_notification(subject, body):
    """
    Sends an email notification with the provided subject and body.
    
    Args:
        subject (str): The subject of the email.
        body (str): The body of the email (can include details such as status, errors, etc.).

    Returns:
        None
    """
    try:
        # Create the email content
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        
        # Set up the SMTP connection and send the email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        
        logging.info(f"Email notification sent to {RECIPIENT_EMAIL}. Subject: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}")

# -------------------------------------------------------------------
# Section 3: Example Usage (Main Section)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Example email subject and body
    subject = "Journal Entry Published Successfully"
    body = "The journal entry 'New Automated Journal Entry' was published successfully on your WordPress site."
    
    # Send the notification
    send_email_notification(subject, body)
