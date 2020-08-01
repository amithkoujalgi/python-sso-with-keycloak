import json
from typing import List

import requests

from model.realm import Realm, RealmList
from model.token import KCAuthResponse
from model.user import User, UserList


class KeycloakAdminClient:

    def __init__(self, kc_host, kc_realm, kc_admin_username, kc_admin_password):
        self.kc_host = kc_host
        self.kc_realm = kc_realm
        self.kc_admin_username = kc_admin_username
        self.kc_admin_password = kc_admin_password

    def _client(self) -> KCAuthResponse:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            "username": self.kc_admin_username,
            "password": self.kc_admin_password,
            'grant_type': 'password',
            'client_id': 'admin-cli'
        }
        res = requests.post(
            url=f'{self.kc_host}/realms/{self.kc_realm}/protocol/openid-connect/token',
            headers=headers,
            data=data
        )
        res: KCAuthResponse
        res = KCAuthResponse.parse_raw(res.content)
        return res

    def get_realm_users(self, realm) -> List[User]:
        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self._client().access_token}'
        }
        res = requests.get(url=f'{self.kc_host}/admin/realms/{realm}/users', headers=headers)
        users = UserList.parse_raw(res.content)
        return users.__root__

    def get_realms(self) -> List[Realm]:
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self._client().access_token}',
            'Content-Type': 'application/json'
        }
        res = requests.get(url=f'{self.kc_host}/admin/realms', headers=headers)
        print(res.content)
        realms = RealmList.parse_raw(res.content)
        return realms.__root__

    def create_realm(self, realm_name):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {self._client().access_token}',
            'Content-Type': 'application/json;charset=UTF-8'
        }
        data = json.dumps(dict(
            id=realm_name,
            realm=realm_name,
            enabled=True
        ))

        url = f'{self.kc_host}/admin/realms'
        res = requests.post(url=url, headers=headers, data=data)
        if res.status_code <= 400:
            return
        raise Exception(res.content)


kc = KeycloakAdminClient(
    kc_host='http://localhost:8080/auth',
    kc_realm='master',
    kc_admin_username='admin',
    kc_admin_password='admin'
)

users = kc.get_realm_users('master')
# print(users)

rs = kc.get_realms()
print(rs)

# kc.create_realm('test12')
