from enum import StrEnum


class PublicUserRoles(StrEnum):
    SELLER = 'seller'
    BUYER = 'buyer'


class PrivateUserRoles(StrEnum):
    SELLER = 'seller'
    BUYER = 'buyer'
    ADMIN = 'admin'
