from app import app, mail, db
from flask import render_template
from flask_mail import Message
from threading import Thread


def async_send_mail(app, msg):
    with app.app_context():
        return mail.send(msg)

def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=async_send_mail, args=[app._get_current_object(), msg])
    thr.start()
    return thr
