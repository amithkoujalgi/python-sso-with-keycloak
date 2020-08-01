import requests

from http_util import HttpUtil
from model.token import KCAuthResponse


class KeycloakAdminClientConfig:
    kc_host = None
    kc_realm = None
    kc_admin_username = None
    kc_admin_password = None
    kc_access_token = None

    def build(kc_host, kc_realm, kc_admin_username, kc_admin_password):
        KeycloakAdminClientConfig.kc_host = kc_host
        KeycloakAdminClientConfig.kc_realm = kc_realm
        KeycloakAdminClientConfig.kc_admin_username = kc_admin_username
        KeycloakAdminClientConfig.kc_admin_password = kc_admin_password
        if KeycloakAdminClientConfig.kc_access_token is None:
            KeycloakAdminClientConfig.kc_access_token = KeycloakAdminClientConfig.__client().access_token

    @staticmethod
    def __client() -> KCAuthResponse:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            "username": KeycloakAdminClientConfig.kc_admin_username,
            "password": KeycloakAdminClientConfig.kc_admin_password,
            'grant_type': 'password',
            'client_id': 'admin-cli'
        }
        res = HttpUtil.post(
            url=f'{KeycloakAdminClientConfig.kc_host}/realms/{KeycloakAdminClientConfig.kc_realm}/protocol/openid-connect/token',
            headers=headers,
            data=data, convert_data_to_json_str=False
        )
        res: KCAuthResponse
        res = KCAuthResponse.parse_raw(res)
        return res
