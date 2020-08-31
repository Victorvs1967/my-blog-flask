from app import mail
from flask import render_template, current_app
from flask_mail import Message
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send()

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_reset_password_email(user):
    token = user.get_reset_password_token()
    send_email('[My Blog] Reset Your Password',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[user.email],
                text_body=render_template('email/reset_password.txt', user=user, token=token),
                html_body=render_template('email/reset_password.html', user=user, token=token))