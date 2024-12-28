from modules.notifications.settings import SETTINGS
from modules.notifications.utils import BaseEmailSender
from .proto import ConfirmationEmailSenderRepoP


class ConfirmationEmailSenderRepo(BaseEmailSender, ConfirmationEmailSenderRepoP):
    async def send_confirmation_email(self, to: str, subject: str, message: str) -> None:
        await self._send_email(to=to, subject=subject, message=message)


def get_confirmation_email_sender() -> ConfirmationEmailSenderRepoP:
    return ConfirmationEmailSenderRepo(
        domain=SETTINGS.email_sender.domain,
        port=SETTINGS.email_sender.port,
        sender_email=SETTINGS.email_sender.sender_email,
        password=SETTINGS.email_sender.password,
    )
