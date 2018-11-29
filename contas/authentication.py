from contas.models import User, Token


class PasswordlessAuthenticationBackend(object):

    def authenticate(self, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get_or_create(email=token.email)[0]
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
