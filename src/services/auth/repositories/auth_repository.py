from redis.asyncio import Redis


class AuthRepository:
    def __init__(self, redis: Redis):
        self.redis = redis


