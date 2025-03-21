from fastapi_mail import (
    FastMail, MessageSchema, ConnectionConfig)

from app.core.config import setting


class SMTPMessageAsync:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=setting.mail_username,
            MAIL_PASSWORD=setting.mail_password,
            MAIL_PORT=587,
            MAIL_SERVER=setting.mail_server,
            MAIL_SSL_TLS=False,
            MAIL_STARTTLS=True,
            MAIL_FROM=setting.mail_username,
            MAIL_FROM_NAME=setting.app_title
        )

    async def send_message_order(self, email: str, pizza_name: str):
        template = f"""
            <html>
                <body>
                    <p>Hi friend!!!
                    <br>Your pizza {pizza_name} is done!</p>
                </body>
            </html>
        """
        message = MessageSchema(
            subject='You order',
            recipients=[email,],
            body=template,
            subtype='html'
        )
        fm = FastMail(self.conf)
        await fm.send_message(message)


smtp_server = SMTPMessageAsync()
