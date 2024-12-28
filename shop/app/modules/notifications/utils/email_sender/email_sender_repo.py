from email.message import EmailMessage

from aiosmtplib import SMTP


class BaseEmailSender:
    def __init__(
        self,
        domain: str,
        port: int,
        sender_email: str,
        password: str,
    ):
        self._sender_email = sender_email
        self._password = password
        self._server = SMTP(
            hostname=domain,
            port=port,
            username=sender_email,
            password=password,
        )

    async def __aenter__(self) -> None:
        await self._server.connect()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self._server.close()

    async def _send_email(self, to: str, subject: str, message: str) -> None:
        email_message = EmailMessage()
        email_message["From"] = self._sender_email
        email_message["To"] = to
        email_message["Subject"] = subject
        email_message.set_content(message)
        await self._server.send_message(email_message)
