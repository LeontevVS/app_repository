import orjson

from modules.users.depends import REDIS_POOL
from utils_backend.redis.base_redis_repo import BaseRedisRepo
from ._consts import UNCONFIRMED_EMAIL_KEY_TEMPLATE, UNCONFIRMED_EMAIL_EXPIRE_SECONDS
from .models import UnconfirmedEmailSignIn
from .proto import EmailAccessCacheP


class EmailAccessCache(BaseRedisRepo, EmailAccessCacheP):
    async def add_unconfirmed_email_signin(self, data: UnconfirmedEmailSignIn) -> None:
        await self._client.set(
            name=UNCONFIRMED_EMAIL_KEY_TEMPLATE.format(email=data.email),
            value=orjson.dumps(data.model_dump()),
            ex=UNCONFIRMED_EMAIL_EXPIRE_SECONDS,
        )

    async def get_unconfirmed_email_signin(self, email: str) -> UnconfirmedEmailSignIn | None:
        unconfirmed_email_info = await self._client.get(UNCONFIRMED_EMAIL_KEY_TEMPLATE.format(email=email))
        if unconfirmed_email_info:
            return UnconfirmedEmailSignIn.model_validate(
                obj=orjson.loads(unconfirmed_email_info),
                from_attributes=True,
            )


def get_email_access_cache() -> EmailAccessCacheP:
    return EmailAccessCache(redis_pool=REDIS_POOL)
