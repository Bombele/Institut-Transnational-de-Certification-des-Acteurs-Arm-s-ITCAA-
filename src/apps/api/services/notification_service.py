from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path

# Configuration SMTP sécurisée (exemple, à adapter)
conf = ConnectionConfig(
    MAIL_USERNAME="itcaa-sec",
    MAIL_PASSWORD="***",
    MAIL_FROM="alerts@itcaa.org",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.securemail.org",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

async def send_alert_email(recipients: list[str], subject: str, body_html: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body_html,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"status": "sent", "recipients": recipients}
