from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
import smtplib
import ssl

def email(request, receiver_email, message):
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    subject = 'Dj-Ecommerce Registration, Activate your account'
    message = f'''
    Please click the link below to start activate your account, this link will be able to recive under than 48 hours. if this is not your own doing, you can delete or permit the message. Thank you !

    {message}
    '''

    send_mail(
        subject,
        message,
        sender_email,
        [receiver_email],
        fail_silently=False,
    )

    return redirect('auth:login')
