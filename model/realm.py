from typing import Optional, List, Any

from pydantic import BaseModel

from http_util import HttpUtil
from keycloak.keycloak_admin_client import KeycloakAdminClientConfig
from model.client import ClientList
from model.user import UserList, User


class Attributes(BaseModel):
    permanentLockout: bool
    quickLoginCheckMilliSeconds: int
    maxFailureWaitSeconds: int
    minimumQuickLoginWaitSeconds: int
    failureFactor: int
    maxDeltaTimeSeconds: int
    offlineSessionMaxLifespan: int
    bruteForceProtected: bool
    waitIncrementSeconds: int
    offlineSessionMaxLifespanEnabled: bool
    actionTokenGeneratedByUserLifespan: Optional[int] = None
    actionTokenGeneratedByAdminLifespan: Optional[int] = None
    displayName: Optional[str] = None
    displayNameHtml: Optional[str] = None


class BrowserSecurityHeaders(BaseModel):
    contentSecurityPolicyReportOnly: str
    xContentTypeOptions: str
    xRobotsTag: str
    xFrameOptions: str
    xXSSProtection: str
    contentSecurityPolicy: str
    strictTransportSecurity: str


class SMTPServer(BaseModel):
    pass


class Realm(BaseModel):
    id: str
    realm: str
    notBefore: int
    revokeRefreshToken: bool
    refreshTokenMaxReuse: int
    accessTokenLifespan: int
    accessTokenLifespanForImplicitFlow: int
    ssoSessionIdleTimeout: int
    ssoSessionMaxLifespan: int
    ssoSessionIdleTimeoutRememberMe: int
    ssoSessionMaxLifespanRememberMe: int
    offlineSessionIdleTimeout: int
    offlineSessionMaxLifespanEnabled: bool
    offlineSessionMaxLifespan: int
    accessCodeLifespan: int
    accessCodeLifespanUserAction: int
    accessCodeLifespanLogin: int
    actionTokenGeneratedByAdminLifespan: int
    actionTokenGeneratedByUserLifespan: int
    enabled: bool
    sslRequired: str
    registrationAllowed: bool
    registrationEmailAsUsername: bool
    rememberMe: bool
    verifyEmail: bool
    loginWithEmailAllowed: bool
    duplicateEmailsAllowed: bool
    resetPasswordAllowed: bool
    editUsernameAllowed: bool
    bruteForceProtected: bool
    permanentLockout: bool
    maxFailureWaitSeconds: int
    minimumQuickLoginWaitSeconds: int
    waitIncrementSeconds: int
    quickLoginCheckMilliSeconds: int
    maxDeltaTimeSeconds: int
    failureFactor: int
    defaultRoles: List[str]
    requiredCredentials: List[str]
    otpPolicyType: str
    otpPolicyAlgorithm: str
    otpPolicyInitialCounter: int
    otpPolicyDigits: int
    otpPolicyLookAheadWindow: int
    otpPolicyPeriod: int
    otpSupportedApplications: List[str]
    browserSecurityHeaders: BrowserSecurityHeaders
    smtpServer: SMTPServer
    eventsEnabled: bool
    eventsListeners: List[str]
    enabledEventTypes: List[Any]
    adminEventsEnabled: bool
    adminEventsDetailsEnabled: bool
    internationalizationEnabled: bool
    supportedLocales: List[Any]
    browserFlow: str
    registrationFlow: str
    directGrantFlow: str
    resetCredentialsFlow: str
    clientAuthenticationFlow: str
    dockerAuthenticationFlow: str
    attributes: Attributes
    userManagedAccessAllowed: bool
    displayName: Optional[str] = None
    displayNameHtml: Optional[str] = None

    def create_client(self, client_id, root_url):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {KeycloakAdminClientConfig.kc_access_token}',
            'Content-Type': 'application/json;charset=UTF-8'
        }
        data = {
            "enabled": True,
            "attributes": {},
            "redirectUris": [],
            "clientId": client_id,
            "rootUrl": root_url,
            "protocol": "openid-connect"
        }
        url = f'{KeycloakAdminClientConfig.kc_host}/admin/realms/{self.realm}/clients'
        res = HttpUtil.post(url=url, headers=headers, data=data)
        return

    def clients(self):
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {KeycloakAdminClientConfig.kc_access_token}'
        }
        url = f'{KeycloakAdminClientConfig.kc_host}/admin/realms/{self.realm}/clients'
        res = HttpUtil.get(url=url, headers=headers)
        res = res.decode()
        clients = ClientList.parse_raw(str(res))
        return clients.__root__

    def get_users(self) -> List[User]:
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {KeycloakAdminClientConfig.kc_access_token}'
        }
        url = f'{KeycloakAdminClientConfig.kc_host}/admin/realms/{self.realm}/users'
        res = HttpUtil.get(url=url, headers=headers)
        users = UserList.parse_raw(res)
        return users.__root__


class RealmList(BaseModel):
    __root__: List[Realm]
