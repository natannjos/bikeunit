from django.test import TestCase
from django.contrib import auth

from contas.models import Token

User = auth.get_user_model()


class UserModelTest(TestCase):

    def test_usuario_valido_apenas_com_email(self):
        user = User(email='a@b.com')
        user.full_clean()

    def test_email_eh_chave_primaria(self):
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')

    def test_linca_usuario_com_uid_auto_gerado(self):
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)

    def test_sem_problemas_com_auth_login(self):
        user= User.objects.create(email='erlon@email.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)