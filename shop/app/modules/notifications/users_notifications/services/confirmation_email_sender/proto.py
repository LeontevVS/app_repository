from typing import Protocol


class ConfirmationEmailSenderP(Protocol):
    async def send_confirmation_email(self, to: str, code: int) -> None:
        pass
