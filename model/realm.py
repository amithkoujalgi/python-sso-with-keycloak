from typing import Optional, List, Any

from pydantic import BaseModel


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


class RealmList(BaseModel):
    __root__: List[Realm]
