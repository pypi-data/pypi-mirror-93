from uuid import uuid4

# from django.conf import settings
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from keycloak import KeycloakAdmin


class BaseKeyCloak(object):
    def __init__(self):
        # self.server_url = getattr(settings, "KEYCLOAK_SERVER_URL", "")
        # self.realm_name = getattr(settings, "KEYCLOAK_REALM_NAME", "")
        # self.username = getattr(settings, "KEYCLOAK_ADMIN_USERNAME", "")
        # self.password = getattr(settings, "KEYCLOAK_ADMIN_PASSWORD", "")
        # self.client_id = getattr(settings, "KEYCLOAK_CLIENT_ID", "")
        # self.client_secret_key = getattr(settings, "KEYCLOAK_CLIENT_SECRET_KEY", "")

        self.server_url = "http://localhost:1000/auth"
        self.realm_name = "Auth"
        self.username = "dep.informatica@dnoticias.pt"
        self.password = "capslock"
        self.client_id = "mail"
        self.client_secret_key = "0ba3af67-5ee4-44ba-9012-212673ed99e7"

        self.keycloak_admin = KeycloakAdmin(
                                server_url=self.server_url,
                                username=self.username,
                                password=self.password,
                                realm_name=self.realm_name,
                                verify=True
                            )

        self.keycloak_openid = KeycloakOpenID(
                                server_url=self.server_url,
                                client_id=self.client_id,
                                realm_name=self.realm_name,
                                client_secret_key=self.client_secret_key,
                                verify=True
                            )

class CreateUser(BaseKeyCloak):
    def __call__(self, email):
        password = uuid4()
        new_user = keycloak_admin.create_user(
            {
                "email": email,
                "username": email,
                "enabled": True,
                "credentials": [
                    {
                        "value": password, "type": "password"
                    }
                ],
                "realmRoles": ["user_default", ],
                "attributes": {
                    "is_staff": True
                }
            }
        )
        info = get_user_info()


class UpdatePassword(BaseKeyCloak):
    def __call__(self, email, password):
        user_id_keycloack = self.keycloak_admin.get_user_id(email)
        self.keycloak_admin.set_user_password(user_id=user_id_keycloack, password=password, temporary=False)


class GetUserInfo(BaseKeyCloak):
    def __call__(self, email, password):
        return self.keycloak_openid.token(email, password)

create_user = CreateUser()
update_password = UpdatePassword()
get_user_info = GetUserInfo()
