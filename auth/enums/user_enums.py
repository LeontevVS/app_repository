from enum import StrEnum


class PrivateUserRoles(StrEnum):
    ADMIN = 'admin'
    SELLER = 'seller'
    BUYER = 'buyer'


class PublicUserRoles(StrEnum):
    SELLER = 'seller'
    BUYER = 'buyer'
