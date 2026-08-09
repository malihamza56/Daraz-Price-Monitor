from src.notifications.mailer import Mailer


products = [
    {
        "title": "TEST — Lenovo Chromebook 100E",
        "oldPrice": 12000,
        "newPrice": 9000,
        "productLink": "https://www.daraz.pk/"
    }
]


mailer = Mailer(products)

mailer._send_email()