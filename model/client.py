from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Access(BaseModel):
    view: bool
    configure: bool
    manage: bool


class Attributes(BaseModel):
    pass


class Config(BaseModel):
    pass


class ProtocolMapper(BaseModel):
    id: UUID
    name: str
    protocol: str
    protocolMapper: str
    consentRequired: bool
    config: Config


class Client(BaseModel):
    id: UUID
    clientId: str
    surrogateAuthRequired: bool
    enabled: bool
    clientAuthenticatorType: str
    redirectUris: List[str]
    webOrigins: List[str]
    notBefore: int
    bearerOnly: bool
    consentRequired: bool
    standardFlowEnabled: bool
    implicitFlowEnabled: bool
    directAccessGrantsEnabled: bool
    serviceAccountsEnabled: bool
    publicClient: bool
    frontchannelLogout: bool
    protocol: str
    attributes: Attributes
    authenticationFlowBindingOverrides: Attributes
    fullScopeAllowed: bool
    nodeReRegistrationTimeout: int
    defaultClientScopes: List[str]
    optionalClientScopes: List[str]
    access: Access
    rootUrl: Optional[str] = None
    adminUrl: Optional[str] = None
    name: Optional[str] = None
    baseUrl: Optional[str] = None
    defaultRoles: Optional[List[str]] = None
    protocolMappers: Optional[List[ProtocolMapper]] = None


class ClientList(BaseModel):
    __root__: List[Client]
