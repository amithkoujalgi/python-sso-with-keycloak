from typing import List


from http_util import HttpUtil
from keycloak.kc_config import KeycloakAdminClientConfig
from model.realm import Realm, RealmList


class KeycloakClient:

    @staticmethod
    def configure(kc_host, kc_realm, kc_admin_username, kc_admin_password):
        KeycloakAdminClientConfig.build(
            kc_host=kc_host,
            kc_realm=kc_realm,
            kc_admin_username=kc_admin_username,
            kc_admin_password=kc_admin_password
        )
        return KeycloakClient

    @staticmethod
    def get_realms() -> List[Realm]:
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {KeycloakAdminClientConfig.kc_access_token}',
            'Content-Type': 'application/json'
        }
        res = HttpUtil.get(url=f'{KeycloakAdminClientConfig.kc_host}/admin/realms', headers=headers)
        realms = RealmList.parse_raw(res)
        realms.__root__: List[Realm]
        return realms.__root__

    @staticmethod
    def get_realm(realm_name) -> Realm:
        for r in KeycloakClient.get_realms():
            if r.realm == realm_name:
                return r
        raise Exception("Realm not found")

    @staticmethod
    def create_realm(realm_name):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {KeycloakAdminClientConfig.kc_access_token}',
            'Content-Type': 'application/json;charset=UTF-8'
        }
        data = dict(
            id=realm_name,
            realm=realm_name,
            enabled=True
        )
        url = f'{KeycloakAdminClientConfig.kc_host}/admin/realms'
        res = HttpUtil.post(url=url, headers=headers, data=data)
        return KeycloakClient.get_realm(realm_name)
