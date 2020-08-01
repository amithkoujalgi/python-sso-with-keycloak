import logging
import urllib

import flask_login
from flask import Flask, request, Response
from flask_oidc import OpenIDConnect
from werkzeug.utils import redirect
from keycloak import KeycloakAdmin

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

KC_SERVER_AUTH_ENDPOINT = 'http://localhost:8080/auth'
AUTH_SERVER_ENDPOINT = 'http://localhost:5000'
REALM = 'master'
KC_SERVER_LOGOUT_ENDPOINT = f"{KC_SERVER_AUTH_ENDPOINT}/realms/{REALM}/protocol/openid-connect/logout?redirect_uri={urllib.parse.quote(AUTH_SERVER_ENDPOINT)}"

app.config.update({
    'SECRET_KEY': 'u\x91\xcf\xfa\x0c\xb9\x95\xe3t\xba2K\x7f\xfd\xca\xa3\x9f\x90\x88\xb8\xee\xa4\xd6\xe4',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_VALID_ISSUERS': [f'{KC_SERVER_AUTH_ENDPOINT}/realms/{REALM}'],
    'OIDC_OPENID_REALM': f'{AUTH_SERVER_ENDPOINT}/oidc_callback'
})
oidc = OpenIDConnect(app)

import json


def jprint(d):
    print(json.dumps(d, indent=4))


@app.route('/')
def login():
    if oidc.user_loggedin:
        return redirect('/home')
    else:
        return f"SSO Auth Server<a style='float: right' href='/home'>Login</a>"


@app.route('/home')
@oidc.require_login
def home():
    if oidc.user_loggedin:
        for c in request.cookies:
            cval = request.cookies.get(c)
            # print(f"{c} - {cval}")
        for k in oidc.credentials_store:
            cstore = oidc.credentials_store[k]
            cstore = json.loads(cstore)
            if 'access_token' in cstore:
                access_token = cstore['access_token']
                username = oidc.user_getfield('preferred_username', access_token)
                return f"Hello, {username} <a style='float: right' href='/logout'>Log out</a>"
        return redirect('/logout')
    return redirect('/')


@app.route('/logout')
def logout():
    oidc.logout()
    return redirect(KC_SERVER_LOGOUT_ENDPOINT)


@app.route('/setup')
def setup():
    # get request param
    new_realm_name = request.args.get('realm')
    if new_realm_name is None or new_realm_name == '':
        logging.info(f'Fetching realms...')
        available_realms = [r['realm'] for r in KeycloakAdminUtil.client().get_realms()]
        return Response(json.dumps(available_realms), mimetype='application/json')

    realms = KeycloakAdminUtil.client().get_realms()

    found = False
    realm = None

    for r in realms:
        if r['id'] == new_realm_name:
            found = True
            realm = r

    if not found:
        logging.info(f'Creating realm {new_realm_name}...')
        new_realm = dict(
            id=new_realm_name,
            realm=new_realm_name,
            displayName=new_realm_name
        )
        KeycloakAdminUtil.client().create_realm(payload=new_realm)

    logging.info(f'Fetching realm...')
    return Response(json.dumps(realm), mimetype='application/json')


class KeycloakAdminUtil:
    @staticmethod
    def client():
        admin = KeycloakAdmin(
            server_url='http://localhost:8080/auth/',
            username='admin',
            password='admin',
            realm_name='master',
            verify=True
        )
        return admin


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
