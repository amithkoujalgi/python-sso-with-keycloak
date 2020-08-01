from typing import List

from pydantic import BaseModel


class Access(BaseModel):
    manageGroupMembership: bool
    view: bool
    mapRoles: bool
    impersonate: bool
    manage: bool


class User(BaseModel):
    id: str
    createdTimestamp: int
    username: str
    enabled: bool
    totp: bool
    emailVerified: bool
    disableableCredentialTypes: List[str]
    requiredActions: list
    notBefore: int
    access: Access


class UserList(BaseModel):
    __root__: List[User]
