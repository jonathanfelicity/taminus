import smtplib
import ssl
import random





def token(): ...


def mailer(port: int, mail: str, password: str, ):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("my@gmail.com", password)
