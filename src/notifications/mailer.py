import smtplib
from email.message import EmailMessage
from pathlib import Path

from src.config.logger import logger
from src.config.config import (
    SMTP_HOST,
    SMTP_PORT,
    EMAIL_USER,
    EMAIL_PASSWORD,
    PREVIOUS_FILTERED_EXCEL,
)


required = {
    "SMTP_HOST": SMTP_HOST,
    "EMAIL_USER": EMAIL_USER,
    "EMAIL_PASSWORD": EMAIL_PASSWORD,
}

missing = [
    key
    for key, value in required.items()
    if not value
]

if missing:
    raise ValueError(
        f"Missing environment variables: {', '.join(missing)}"
    )


class Mailer:

    def __init__(self, products, target_email):

        self.products = products
        self.target_email = target_email

    def _send_email(self):

        try:

            logger.info(
                "Preparing Daraz price tracking email..."
            )

            # ------------------------------------------------
            # EMAIL MESSAGE
            # ------------------------------------------------

            message = EmailMessage()

            message["Subject"] = (
                "Daraz Price Drop Alert 🔥"
                if self.products
                else "Daraz Price Tracking Report 📊"
            )

            message["From"] = EMAIL_USER
            message["To"] = self.target_email

            # ------------------------------------------------
            # EMAIL BODY
            # ------------------------------------------------

            if self.products:

                body = (
                    "Daraz Price Drop Alert 🔥\n\n"
                    "The following products have dropped "
                    "in price:\n\n"
                )

                for product in self.products:

                    body += f"""
Product: {product.get('title')}
Old Price: Rs. {product.get('oldPrice')}
New Price: Rs. {product.get('newPrice')}
Product Link: {product.get('productLink')}

----------------------------------------

"""

            else:

                body = (
                    "Daraz Price Tracking Report 📊\n\n"
                    "No price drop was detected during "
                    "this tracking cycle.\n\n"
                    "All tracked products were compared "
                    "with the previous snapshot."
                )

            body += (
                "\n📎 The latest Excel report is attached "
                "with this email."
            )

            message.set_content(body)

            # ------------------------------------------------
            # EXCEL ATTACHMENT
            # ------------------------------------------------

            excel_path = Path(
                PREVIOUS_FILTERED_EXCEL
            )

            if excel_path.exists():

                logger.info(
                    f"Attaching Excel report | {excel_path}"
                )

                with open(
                    excel_path,
                    "rb"
                ) as file:

                    excel_data = file.read()

                message.add_attachment(
                    excel_data,
                    maintype="application",
                    subtype=(
                        "vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    filename=excel_path.name,
                )

                logger.info(
                    "Excel report attached successfully."
                )

            else:

                logger.warning(
                    f"Excel report not found | {excel_path}"
                )

            # ------------------------------------------------
            # SMTP CONNECTION
            # ------------------------------------------------

            logger.info(
                "Connecting to SMTP server..."
            )

            with smtplib.SMTP(
                SMTP_HOST,
                SMTP_PORT
            ) as server:

                server.starttls()

                server.login(
                    EMAIL_USER,
                    EMAIL_PASSWORD
                )

                server.send_message(
                    message
                )

            logger.info(
                "Email sent successfully!"
            )

            # ------------------------------------------------
            # RETURN RESULT TO UI
            # ------------------------------------------------

            return {
                "status": "sent",
                "message": (
                    "Price drop email sent successfully!"
                    if self.products
                    else
                    "No price drop email sent successfully!"
                ),
            }

        except Exception as e:

            logger.error(
                f"Failed to send email | {e}"
            )

            raise