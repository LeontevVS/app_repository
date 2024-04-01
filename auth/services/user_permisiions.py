# TODO: выпилить авторизацию

# from typing import Annotated
#
# from fastapi import Header
#
# from enums.user_enums import PrivateUserRoles
# from schemas.auth import AuthenticatedUserDTO
# from services.auth_users import AuthUserService
#
#
# class UserPermission:
#     def __init__(self, auth_user_service: AuthUserService):
#         self.auth_user_service = auth_user_service
#
#     async def auth_seller_permissions(self, access_token: Annotated[str | None, Header()]) -> AuthenticatedUserDTO:
#         return await self.auth_user_service.auth_user(
#             access_token=access_token,
#             roles=[PrivateUserRoles.SELLER, PrivateUserRoles.ADMIN]
#         )
#
#     async def auth_buyer_permissions(self, access_token: Annotated[str | None, Header()]) -> AuthenticatedUserDTO:
#         return await self.auth_user_service.auth_user(
#             access_token=access_token,
#             roles=[PrivateUserRoles.BUYER, PrivateUserRoles.ADMIN]
#         )
#
#     async def auth_admin_permissions(self, access_token: Annotated[str | None, Header()]) -> AuthenticatedUserDTO:
#         return await self.auth_user_service.auth_user(
#             access_token=access_token,
#             roles=[PrivateUserRoles.ADMIN]
#         )
#
#     async def auth_all_permissions(self, access_token: Annotated[str | None, Header()]) -> AuthenticatedUserDTO:
#         return await self.auth_user_service.auth_user(
#             access_token=access_token,
#             roles=[PrivateUserRoles.ADMIN, PrivateUserRoles.BUYER, PrivateUserRoles.SELLER]
#         )
