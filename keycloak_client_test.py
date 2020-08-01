import uuid

from keycloak.keycloak_admin_client import KeycloakClient

kc = KeycloakClient.configure(
    kc_host='http://localhost:8080/auth',
    kc_realm='master',
    kc_admin_username='admin',
    kc_admin_password='admin'
)

realm = str(uuid.uuid4())

rlm = kc.create_realm(realm)
print(f"Created realm: {rlm}")

rs = kc.get_realms()
print(rs)

r = kc.get_realm(realm)
print(r)

users = r.get_users()
print(users)

r.create_client(client_id=f'{r.realm}-auth', root_url='http://localhost:5000')

clients = r.clients()
print(f"Clients: {clients}")
