import smtplib
from email.message import EmailMessage

from src.config.logger import logger
from src.config.config import (
    SMTP_HOST,
    SMTP_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    TARGET_EMAIL
)

required = {
    "SMTP_HOST": SMTP_HOST,
    "EMAIL_USER": EMAIL_USER,
    "EMAIL_PASSWORD": EMAIL_PASSWORD,
    "TARGET_EMAIL": TARGET_EMAIL
}

missing = [key for key, value in required.items() if not value]

if missing:
    raise ValueError(
        f"Missing environment variables: {', '.join(missing)}"
    )
    
    
class Mailer:

    def __init__(self, products):
        self.products = products

    def _send_email(self):

        try:

            logger.info("Preparing price drop email...")

            if not self.products:
                logger.info("No price dropped products found. Email skipped.")
                return

            message = EmailMessage()

            message["Subject"] = "Daraz Price Drop Alert 🔥"
            message["From"] = EMAIL_USER
            message["To"] = TARGET_EMAIL

            body = "Daraz Price Drop Alert\n\n"

            for product in self.products:

                body += f"""
                Product: {product.get('title')}
Old Price: Rs. {product.get('oldPrice')}
Price: Rs. {product.get('newPrice')}
Link: {product.get('productLink')}

----------------------------------------
"""

            message.set_content(body)

            logger.info("Connecting to SMTP server...")

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:

                server.starttls()

                server.login(
                    EMAIL_USER,
                    EMAIL_PASSWORD
                )

                server.send_message(message)

            logger.info("Price drop email sent successfully!")

        except Exception as e:

            logger.error(f"Failed to send email | {e}")
            raise