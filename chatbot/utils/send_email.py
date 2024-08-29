from flask_mail import Mail, Message
from server.server import app

mail = Mail(app)

def send_email(recipients, subject, body):
    with app.app_context():
        msg = Message(subject=subject,
                      sender=("No-Reply Telle", "noreply@telle.ai"),
                      recipients=recipients,
                      body=body)
        mail.send(msg)