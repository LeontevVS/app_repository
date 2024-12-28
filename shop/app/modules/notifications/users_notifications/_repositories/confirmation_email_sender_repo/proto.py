from typing import Protocol


class ConfirmationEmailSenderRepoP(Protocol):
    async def send_confirmation_email(self, to: str, subject: str, message: str) -> None:
        pass
