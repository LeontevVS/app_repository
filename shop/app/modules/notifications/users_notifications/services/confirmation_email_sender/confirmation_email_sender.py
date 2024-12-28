from ._consts import EMAIL_SUBJECT, EMAIL_MESSAGE_TEMPLATE
from .proto import ConfirmationEmailSenderP
from modules.notifications.users_notifications._repositories.confirmation_email_sender_repo import (
    ConfirmationEmailSenderRepoP,
    get_confirmation_email_sender,
)


class ConfirmationEmailSender(ConfirmationEmailSenderP):
    def __init__(self, confirmation_email_sender_repo: ConfirmationEmailSenderRepoP) -> None:
        self._confirmation_email_sender_repo = confirmation_email_sender_repo

    async def send_confirmation_email(self, to: str, code: int) -> None:
        async with self._confirmation_email_sender_repo:
            await self._confirmation_email_sender_repo.send_confirmation_email(
                to=to,
                subject=EMAIL_SUBJECT,
                message=EMAIL_MESSAGE_TEMPLATE.format(code=code),
            )


def get_confirmation_email_service() -> ConfirmationEmailSenderP:
    return ConfirmationEmailSender(
        confirmation_email_sender_repo=get_confirmation_email_sender(),
    )
