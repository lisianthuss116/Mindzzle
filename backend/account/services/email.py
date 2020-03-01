from django.shortcuts import redirect
from django.conf import settings
import smtplib
import ssl


def send_email_to(reciver_username, receiver_email, link):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg['Subject'] = '[Dj-Ecommerce] Please verify your email address.'
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = receiver_email

    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
    <body style='font-size: 1rem;'>
        <p style='margin-top: 1rem !important;margin-bottom: 1rem !important;'>Almost done, <span style="font-weight: 700;">{reciver_username}</span>! To complete your django-ecommerce sign up, we just need to verify your email address.</p>

        <p style='margin-top: 1rem !important;margin-bottom: 1rem !important;'>Once verified, you can start using all of django-ecommerce features to use. This link will be able in 24 hours. If you did not attempt to sign up, you can delete or permit the message.</p>

        <a href='{link}' style='display: inline-block;font-weight: 400;
        color: #212529;text-align: center;vertical-align: middle;cursor: pointer;
        user-select: none;background-color: transparent;border: 1px solid transparent;padding: 0.375rem 0.75rem;font-size: 1rem;line-height: 1.5;border-radius: 0.25rem;transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;color: #fff;background-color: #007bff;border-color: #007bff;text-decoration:none !important;'>Verify email address</a>

        <p style="font-size: 0.9rem;margin-top: 3rem !important;">Thanks,</p>
        <p style="font-size: 0.9rem;">The Django-Ecommerce Team</p>
    </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.send_message(msg)

    return redirect('auth:login')
